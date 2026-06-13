"""Контроллер для работы с базой данных SQLite."""

import sqlite3
from typing import List, Dict, Optional


class CurrencyRatesCRUD:
    """
    CRUD операции для работы с валютами в SQLite.
    Использует базу данных в памяти (:memory:).
    """
    
    def __init__(self):
        """Инициализация подключения к БД и создание таблиц."""
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row
        self._init_tables()
        self._init_test_data()
    
    def _init_tables(self):
        """Создание таблиц user, currency, user_currency."""
        cursor = self.conn.cursor()
        
        # Таблица пользователей
        cursor.execute('''
            CREATE TABLE user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
        
        # Таблица валют
        cursor.execute('''
            CREATE TABLE currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                num_code TEXT NOT NULL,
                char_code TEXT NOT NULL,
                name TEXT NOT NULL,
                value FLOAT,
                nominal INTEGER
            )
        ''')
        
        # Таблица подписок (связь many-to-many)
        cursor.execute('''
            CREATE TABLE user_currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                currency_id INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES user(id),
                FOREIGN KEY(currency_id) REFERENCES currency(id)
            )
        ''')
        
        self.conn.commit()
    
    def _init_test_data(self):
        """Заполнение тестовыми данными."""
        cursor = self.conn.cursor()
        
        # Добавляем тестовых пользователей
        users = [("Иван Петров",), ("Мария Сидорова",), ("Алексей Иванов",)]
        cursor.executemany("INSERT INTO user(name) VALUES(?)", users)
        
        # Добавляем тестовые валюты
        currencies = [
            ("840", "USD", "Доллар США", 92.50, 1),
            ("978", "EUR", "Евро", 99.80, 1),
            ("156", "CNY", "Китайский юань", 12.75, 1),
        ]
        cursor.executemany(
            "INSERT INTO currency(num_code, char_code, name, value, nominal) VALUES(?,?,?,?,?)",
            currencies
        )
        
        # Добавляем подписки (user_id=1 подписан на USD и EUR)
        cursor.execute("INSERT INTO user_currency(user_id, currency_id) VALUES(1, 1)")
        cursor.execute("INSERT INTO user_currency(user_id, currency_id) VALUES(1, 2)")
        cursor.execute("INSERT INTO user_currency(user_id, currency_id) VALUES(2, 1)")
        
        self.conn.commit()
    
    # ==================== CRUD для Currency ====================
    
    def create_currency(self, num_code: str, char_code: str, name: str, value: float, nominal: int) -> int:
        """
        Создание новой валюты.
        
        Args:
            num_code: Цифровой код валюты
            char_code: Символьный код (USD, EUR)
            name: Название валюты
            value: Курс к рублю
            nominal: Номинал
            
        Returns:
            ID созданной записи
        """
        cursor = self.conn.cursor()
        sql = """
            INSERT INTO currency(num_code, char_code, name, value, nominal)
            VALUES(:num_code, :char_code, :name, :value, :nominal)
        """
        cursor.execute(sql, {
            'num_code': num_code,
            'char_code': char_code.upper(),
            'name': name,
            'value': value,
            'nominal': nominal
        })
        self.conn.commit()
        return cursor.lastrowid
    
    def read_currencies(self) -> List[Dict]:
        """
        Получение списка всех валют.
        
        Returns:
            Список словарей с данными о валютах
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM currency")
        return [dict(row) for row in cursor.fetchall()]
    
    def read_currency_by_id(self, currency_id: int) -> Optional[Dict]:
        """Получение валюты по ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM currency WHERE id = ?", (currency_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def read_currency_by_char_code(self, char_code: str) -> Optional[Dict]:
        """Получение валюты по символьному коду."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM currency WHERE char_code = ?", (char_code.upper(),))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def update_currency_value(self, currency_id: int, value: float) -> bool:
        """
        Обновление курса валюты.
        
        Args:
            currency_id: ID валюты
            value: Новый курс
            
        Returns:
            True если обновление выполнено, False если валюта не найдена
        """
        cursor = self.conn.cursor()
        cursor.execute("UPDATE currency SET value = ? WHERE id = ?", (value, currency_id))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def update_currency_by_char_code(self, char_code: str, value: float) -> bool:
        """
        Обновление курса валюты по символьному коду.
        
        Args:
            char_code: Символьный код валюты (USD, EUR)
            value: Новый курс
            
        Returns:
            True если обновление выполнено, False если валюта не найдена
        """
        cursor = self.conn.cursor()
        cursor.execute("UPDATE currency SET value = ? WHERE char_code = ?", (value, char_code.upper()))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def delete_currency(self, currency_id: int) -> bool:
        """
        Удаление валюты по ID.
        
        Args:
            currency_id: ID валюты
            
        Returns:
            True если удаление выполнено, False если валюта не найдена
        """
        cursor = self.conn.cursor()
        
        # Сначала удаляем связанные подписки (FOREIGN KEY)
        cursor.execute("DELETE FROM user_currency WHERE currency_id = ?", (currency_id,))
        # Затем удаляем саму валюту
        cursor.execute("DELETE FROM currency WHERE id = ?", (currency_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    # ==================== Методы для синхронизации с API ====================
    
    def sync_currencies_from_api(self, currencies_data: List[Dict]) -> int:
        """
        Синхронизация валют из API с БД.
        Обновляет курсы существующих валют, добавляет новые.
        
        Args:
            currencies_data: Список валют из API
            
        Returns:
            Количество обновлённых/добавленных записей
        """
        count = 0
        for data in currencies_data:
            existing = self.read_currency_by_char_code(data['char_code'])
            
            if existing:
                # Обновляем курс существующей валюты
                self.update_currency_value(existing['id'], data['value'])
            else:
                # Добавляем новую валюту
                self.create_currency(
                    num_code=str(data.get('num_code', '')),
                    char_code=data['char_code'],
                    name=data['name'],
                    value=data['value'],
                    nominal=data['nominal']
                )
            count += 1
        return count
    
    def show_currencies_in_console(self):
        """Вывод всех валют в консоль (для отладки)."""
        currencies = self.read_currencies()
        print("\n=== Текущие валюты в БД ===")
        for c in currencies:
            print(f"ID: {c['id']}, {c['char_code']} - {c['name']}: {c['value']} ₽ (номинал: {c['nominal']})")
        print("=" * 30)
    
    def close(self):
        """Закрытие соединения с БД."""
        self.conn.close()