"""Контроллер для обработки маршрута /currencies."""

from jinja2 import Environment, FileSystemLoader
import os
from utils.currencies_api import get_currencies
from models.currency import Currency


class CurrenciesController:
    """Контроллер для отображения курсов валют и CRUD операций."""
    
    def __init__(self, db_controller=None):
        """
        Инициализация контроллера.
        
        Args:
            db_controller: Контроллер базы данных (CurrencyRatesCRUD)
        """
        template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.db = db_controller  # Добавляем БД-контроллер
    
    def handle_currencies(self, handler) -> None:
        """Обрабатывает GET запрос к /currencies - отображение таблицы валют."""
        try:
            # Получаем курсы из API и синхронизируем с БД
            currencies_data = get_currencies()
            
            # Если есть БД, синхронизируем
            if self.db:
                self.db.sync_currencies_from_api(currencies_data)
                # Получаем валюты уже из БД
                db_currencies = self.db.read_currencies()
                currencies = []
                for data in db_currencies:
                    currency = Currency(
                        currency_id=str(data['id']),
                        char_code=data['char_code'],
                        name=data['name'],
                        value=data['value'],
                        nominal=data['nominal']
                    )
                    currencies.append(currency)
            else:
                # Fallback на старую логику (без БД)
                currencies = []
                for data in currencies_data:
                    currency = Currency(
                        currency_id=data['id'],
                        char_code=data['char_code'],
                        name=data['name'],
                        value=data['value'],
                        nominal=data['nominal']
                    )
                    currencies.append(currency)
            
            template = self.env.get_template('currencies.html')
            
            html_content = template.render(
                currencies=[c.to_dict() for c in currencies],
                title="Курсы валют ЦБ РФ"
            )
            
            handler.send_response(200)
            handler.send_header('Content-type', 'text/html; charset=utf-8')
            handler.end_headers()
            handler.wfile.write(html_content.encode('utf-8'))
            
        except Exception as e:
            handler.send_response(500)
            handler.send_header('Content-type', 'text/html; charset=utf-8')
            handler.end_headers()
            handler.wfile.write(f"<h1>Ошибка загрузки курсов</h1><p>{str(e)}</p>".encode('utf-8'))
    
    # ==================== НОВЫЕ МЕТОДЫ ДЛЯ CRUD ====================
    
    def handle_delete_currency(self, handler, currency_id: int) -> None:
        """
        Обрабатывает GET запрос к /currency/delete?id=X - удаление валюты.
        
        Args:
            handler: HTTP обработчик
            currency_id: ID валюты для удаления
        """
        if not self.db:
            handler.send_error(500, "Database not available")
            return
        
        success = self.db.delete_currency(currency_id)
        
        if success:
            # Перенаправляем обратно на страницу валют
            handler.send_response(302)
            handler.send_header('Location', '/currencies')
            handler.end_headers()
        else:
            handler.send_error(404, f"Currency with id={currency_id} not found")
    
    def handle_update_currency(self, handler, char_code: str, value: float) -> None:
        """
        Обрабатывает GET запрос к /currency/update?USD=92.50 - обновление курса.
        
        Args:
            handler: HTTP обработчик
            char_code: Символьный код валюты (USD, EUR)
            value: Новый курс
        """
        if not self.db:
            handler.send_error(500, "Database not available")
            return
        
        success = self.db.update_currency_by_char_code(char_code, value)
        
        if success:
            handler.send_response(302)
            handler.send_header('Location', '/currencies')
            handler.end_headers()
        else:
            handler.send_error(404, f"Currency with code {char_code} not found")
    
    def handle_show_currencies_console(self, handler) -> None:
        """
        Обрабатывает GET запрос к /currency/show - вывод валют в консоль (для отладки).
        
        Args:
            handler: HTTP обработчик
        """
        if not self.db:
            handler.send_error(500, "Database not available")
            return
        
        self.db.show_currencies_in_console()
        
        handler.send_response(200)
        handler.send_header('Content-type', 'text/html; charset=utf-8')
        handler.end_headers()
        handler.wfile.write(b"<h1>Check console for currency list</h1><a href='/currencies'>Back</a>")