ЛР-2
---
##### Ссылка на задание
https://gist.github.com/nzhukov/2837967726ee0dd1a374d871936891d8

#### Задача: 
изучить Декоратор

---
### Задание
```python
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
```
##### Результат

```
MacBook-Pro13:ЛР-2 fedorcagin$ /Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -u "/Users/fedorcagin/Documents/Учёба/Программирование/4 семестр/ЛР-2/task.py"
============================================================
Демонстрация работы паттерна «Декоратор»
============================================================

1. Базовый компонент (получение курсов валют):
  Тип результата: dict
  Курсы: {'USD': 71.209, 'EUR': 82.5445}
--------------------------------------------------

2. YAML декоратор (с библиотекой PyYAML):
  Тип результата: str
  Первые 150 символов:
date: '2026-05-23'
rates:
  USD: 71.209
  EUR: 82.5445
timestamp: '2026-05-25T04:03:08.555374'

--------------------------------------------------
 Сохранено в файл: currencies_20260525_040308.yaml

3. CSV декоратор (с библиотекой csv):
  Тип результата: str
  Первые 150 символов:
date,currency,rate
2026-05-23,USD,71.209
2026-05-23,EUR,82.5445

--------------------------------------------------
 Сохранено в файл: currencies_20260525_040309.csv

============================================================
Демонстрация завершена.
============================================================
MacBook-Pro13:ЛР-2 fedorcagin$ 
```
##### Тесты

```python
import unittest
import json
import tempfile
import os
from unittest.mock import patch, MagicMock
from task import ConcreteComponent, ToYAMLDecorator, ToCSVDecorator


class TestDecorators(unittest.TestCase):
    
    def setUp(self):
        self.component = ConcreteComponent(['USD'])
    
    @patch('urllib.request.urlopen')
    def test_concrete_component_returns_dict(self, mock_urlopen):
        mock_data = {
            'Date': '2024-01-15T00:00:00',
            'Valute': {'USD': {'Value': 75.5}}
        }
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(mock_data).encode()
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        result = self.component.operation()
        self.assertIsInstance(result, dict)
        self.assertIn('rates', result)
    
    @patch('urllib.request.urlopen')
    def test_concrete_component_has_usd(self, mock_urlopen):
        mock_data = {
            'Date': '2024-01-15T00:00:00',
            'Valute': {'USD': {'Value': 75.5}}
        }
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(mock_data).encode()
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        result = self.component.operation()
        self.assertIn('USD', result['rates'])
    
    @patch('urllib.request.urlopen')
    def test_network_error_returns_zeros(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("No internet")
        
        result = self.component.operation()
        self.assertEqual(result['date'], '0000-00-00')
        self.assertEqual(result['rates']['USD'], 0)
        self.assertIn('error', result)
    
    @patch('urllib.request.urlopen')
    def test_yaml_decorator_returns_str(self, mock_urlopen):
        mock_data = {
            'Date': '2024-01-15T00:00:00',
            'Valute': {'USD': {'Value': 75.5}}
        }
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(mock_data).encode()
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        decorator = ToYAMLDecorator(self.component)
        result = decorator.operation()
        self.assertIsInstance(result, str)
        self.assertIn('USD', result)
    
    @patch('urllib.request.urlopen')
    def test_yaml_decorator_saves_file(self, mock_urlopen):
        mock_data = {
            'Date': '2024-01-15T00:00:00',
            'Valute': {'USD': {'Value': 75.5}}
        }
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(mock_data).encode()
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        decorator = ToYAMLDecorator(self.component)
        
        with tempfile.NamedTemporaryFile(suffix='.yaml', delete=False) as tmp:
            filename = tmp.name
        
        try:
            saved_file = decorator.save_to_file(filename)
            self.assertTrue(os.path.exists(saved_file))
            with open(saved_file, 'r') as f:
                content = f.read()
                self.assertIn('USD', content)
        finally:
            if os.path.exists(filename):
                os.remove(filename)
    
    @patch('urllib.request.urlopen')
    def test_csv_decorator_returns_str(self, mock_urlopen):
        mock_data = {
            'Date': '2024-01-15T00:00:00',
            'Valute': {'USD': {'Value': 75.5}}
        }
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(mock_data).encode()
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        decorator = ToCSVDecorator(self.component)
        result = decorator.operation()
        self.assertIsInstance(result, str)
        self.assertIn('USD', result)
    
    @patch('urllib.request.urlopen')
    def test_csv_decorator_has_csv_format(self, mock_urlopen):
        mock_data = {
            'Date': '2024-01-15T00:00:00',
            'Valute': {'USD': {'Value': 75.5}}
        }
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(mock_data).encode()
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        decorator = ToCSVDecorator(self.component)
        result = decorator.operation()
        self.assertIn('date,currency,rate', result)
    
    @patch('urllib.request.urlopen')
    def test_csv_decorator_saves_file(self, mock_urlopen):
        mock_data = {
            'Date': '2024-01-15T00:00:00',
            'Valute': {'USD': {'Value': 75.5}}
        }
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(mock_data).encode()
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        decorator = ToCSVDecorator(self.component)
        
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
            filename = tmp.name
        
        try:
            saved_file = decorator.save_to_file(filename)
            self.assertTrue(os.path.exists(saved_file))
        finally:
            if os.path.exists(filename):
                os.remove(filename)


if __name__ == '__main__':
    unittest.main()
```
##### Результат

```
MacBook-Pro13:ЛР-2 fedorcagin$ /Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -u "/Users/fedorcagin/Documents/Учёба/Программирование/4 семестр/ЛР-2/test.py"
........
----------------------------------------------------------------------
Ran 8 tests in 0.005s

OK
MacBook-Pro13:ЛР-2 fedorcagin$ 
```

- **Декоратор** – это структурный паттерн, который позволяет динамически добавлять новое поведение объекту, оборачивая его в другой объект-обёртку. Вместо того чтобы плодить классы-наследники на каждый случай, можно создавать классы-декораторы которые принимают исходный объект, добавляют ему функционал и делегируют остальное на исходный класс

- **Чем декоратор лучше наследования:**
Наследование добавляет поведение навсегда и ко всем экземплярам. Декоратор позволяет обернуть конкретный объект на лету, не меняя его класс. Это соблюдает принцип открытости/закрытости (OCP) – класс `ConcreteComponent` остаётся неизменным при добавлении YAML и CSV

- **Как работает базовый `Decorator`:**
Decorator служит указателем на интерфейс Component и operation, которые потом используются в ToYAMLDecorator и ToCSVDecorator

- **Вывод:** Паттерн Декоратор позволяет гибко расширять функциональность объектов без изменения их исходного кода, соблюдая принципы SOLID. Код легко тестируется (8 тестов покрывают основные сценарии) и готов к добавлению новых форматов вывода
---