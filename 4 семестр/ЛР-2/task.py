"""
Лабораторная работа 2. Паттерн «Декоратор»
Модуль для получения курсов валют с API Центробанка и преобразования в разные форматы.
"""

import csv
import json
import yaml
from abc import ABC, abstractmethod
from datetime import datetime
from io import StringIO
from typing import Dict, Any, Union, Optional, List
import urllib.request
import urllib.error


class Component(ABC):
    """Базовый интерфейс Компонента."""
    
    @abstractmethod
    def operation(self) -> Dict[str, Any]:
        """
        Базовый метод, возвращающий данные.
        
        Returns:
            Dict[str, Any]: Словарь с курсами валют и метаданными
        """
        pass


class ConcreteComponent(Component):
    """Конкретный компонент для получения курсов валют от API Центробанка."""
    
    def __init__(self, currency_codes: Optional[List[str]] = None) -> None:
        self.currency_codes: List[str] = currency_codes or ['USD', 'EUR']
        self.api_url: str = "https://www.cbr-xml-daily.ru/daily_json.js"
    
    def operation(self) -> Dict[str, Any]:
        try:
            with urllib.request.urlopen(self.api_url, timeout=10) as response:
                data = json.loads(response.read().decode())
            
            rates = {}
            for currency in self.currency_codes:
                if currency in data['Valute']:
                    rates[currency] = data['Valute'][currency]['Value']
            
            return {
                'date': data['Date'].split('T')[0],
                'rates': rates,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return self._get_mock_data()  # ← вызов метода внутри класса
    
    def _get_mock_data(self) -> Dict[str, Any]:  # ← ВНУТРИ класса, с отступом
        """
        Возвращает нулевые данные при ошибке сети.
        """
        return {
            'date': '0000-00-00',
            'rates': {code: 0 for code in self.currency_codes},
            'timestamp': datetime.now().isoformat(),
            'error': 'Нет соединения с API Центробанка'
        }


class Decorator(Component):
    """Базовый класс Декоратора."""
    
    def __init__(self, component: Component) -> None:
        """
        Инициализация декоратора.
        
        Args:
            component: Обёрнутый компонент
        """
        self._component: Component = component
    
    def operation(self) -> Dict[str, Any]:
        """Делегирует вызов обёрнутому компоненту."""
        return self._component.operation()


class ToYAMLDecorator(Decorator):
    """Декоратор для преобразования данных в YAML формат (с использованием PyYAML)."""
    
    def operation(self) -> str:
        """
        Возвращает данные в YAML формате.
        
        Returns:
            str: Данные в YAML-формате
        """
        data = self._component.operation()
        return yaml.dump(data, allow_unicode=True, sort_keys=False)
    
    def save_to_file(self, filename: Optional[str] = None) -> str:
        """
        Сохраняет данные в YAML файл.
        
        Args:
            filename: Имя файла (если None, генерируется автоматически)
        
        Returns:
            str: Путь к сохранённому файлу
        """
        if filename is None:
            filename = f"currencies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.operation())
        
        return filename


class ToCSVDecorator(Decorator):
    """Декоратор для преобразования данных в CSV формат (с использованием библиотеки csv)."""
    
    def operation(self) -> str:
        """
        Возвращает данные в CSV формате.
        
        Returns:
            str: Данные в CSV-формате
        """
        data = self._component.operation()
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Заголовки
        writer.writerow(['date', 'currency', 'rate'])
        
        # Данные по валютам
        for currency, rate in data['rates'].items():
            writer.writerow([data['date'], currency, rate])
        
        return output.getvalue()
    
    def save_to_file(self, filename: Optional[str] = None) -> str:
        """
        Сохраняет данные в CSV файл.
        
        Args:
            filename: Имя файла (если None, генерируется автоматически)
        
        Returns:
            str: Путь к сохранённому файлу
        """
        if filename is None:
            filename = f"currencies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            f.write(self.operation())
        
        return filename


def client_code(component: Component) -> None:
    """
    Клиентский код для демонстрации работы.
    
    Args:
        component: компонент (обычный или декорированный)
    """
    result = component.operation()
    
    if isinstance(result, dict):
        print(f"  Тип результата: dict")
        print(f"  Курсы: {result.get('rates', {})}")
    else:
        print(f"  Тип результата: {type(result).__name__}")
        print(f"  Первые 150 символов:\n{result[:150]}")
    print("-" * 50)


def main() -> None:
    """Демонстрация работы паттерна Декоратор."""
    
    print("=" * 60)
    print("Демонстрация работы паттерна «Декоратор»")
    print("=" * 60)
    
    # 1. Базовый компонент (возвращает dict)
    print("\n1. Базовый компонент (получение курсов валют):")
    simple = ConcreteComponent(['USD', 'EUR'])
    client_code(simple)
    
    # 2. YAML декоратор
    print("\n2. YAML декоратор (с библиотекой PyYAML):")
    yaml_decorator = ToYAMLDecorator(simple)
    client_code(yaml_decorator)
    yaml_file = yaml_decorator.save_to_file()
    print(f" Сохранено в файл: {yaml_file}")
    
    # 3. CSV декоратор
    print("\n3. CSV декоратор (с библиотекой csv):")
    csv_decorator = ToCSVDecorator(simple)
    client_code(csv_decorator)
    csv_file = csv_decorator.save_to_file()
    print(f" Сохранено в файл: {csv_file}")
    
    print("\n" + "=" * 60)
    print("Демонстрация завершена.")
    print("=" * 60)


if __name__ == "__main__":
    main()