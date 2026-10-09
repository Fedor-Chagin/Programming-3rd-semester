
## ЛР-6

### Задание
0. Написать функцию get_currencies(currency_codes, url), которая обращается к API по url (по умолчанию - https://www.cbr-xml-daily.ru/daily_json.js) и возвращает словарь курсов валют для валют из списка currency_codes.

В возвращаемом словаре ключи - символьные коды валют, а значения - их курсы.

В случае ошибки запроса функция должна вернуть None.

Для обращения к API использовать функцию get модуля requests.

Для установки requests можно использовать команду:

pip install requests.
Итерация 1

Предусмотреть в функции логирование ошибок с использованием стандартного потока вывода (sys.stdout).

Функция должна обрабатывать следующие исключения:

в ответе не содержатся курсы валют;
в словаре курсов валют нет валюты из списка currency_codes;
ошибка выполнения запроса к API.
Итерация 2.

Вынести логирование ошибок из функции get_currencies(currency_codes, url) в декоратор.

Итерация 3.

Оформить логирование ошибок с использованием модуля logging.

Документация по logging: https://docs.python.org/3/library/logging.html

Туториал по logging: https://docs.python.org/3/howto/logging.html

Тестирование функций должно содержать:

проверку ключей и значений возвращаемого словаря;
проверку обработки исключений;
проверку записей логов в поток вывода.

1. Код программы:

```py
import requests
import logging
import sys
from functools import wraps

# =============== ИТЕРАЦИЯ 1 ===============
def get_currencies_v1(currency_codes, url="https://www.cbr-xml-daily.ru/daily_json.js"):
    """
    Возвращает курсы валют для указанных кодов
    
    Итерация 1: Базовая реализация с обработкой ошибок внутри функции.
    Логирование осуществляется через sys.stdout.write
    
    Args:
        currency_codes (list): Список кодов валют (например, ['USD', 'EUR'])
        url (str, optional): URL API ЦБ РФ. По умолчанию используется официальный.
        
    Returns:
        dict or None: Словарь вида {'USD': 92.5, 'EUR': 99.8} или None при ошибке.
        
    Raises:
        Ошибки не пробрасываются наружу, а обрабатываются внутри функции.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if 'Valute' not in data:
            sys.stdout.write("Ошибка\n") 
            return None
        
        result = {}
        for code in currency_codes:
            if code not in data['Valute']:
                sys.stdout.write(f"Нет валюты {code}\n")
                return None
            result[code] = data['Valute'][code]['Value']
        return result
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stdout)
        return None

# =============== ИТЕРАЦИЯ 2 ===============
def log_errors_print(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Ошибка: {e}", file=sys.stdout)
            return None
    return wrapper

@log_errors_print
def get_currencies_v2(currency_codes, url="https://www.cbr-xml-daily.ru/daily_json.js"):
    """
    Возвращает курсы валют для указанных кодов (версия 2).
    
    Итерация 2: Чистая функция без обработки ошибок и побочных действий (только ищет курсы валют).
    Обработка ошибок делегирована декоратору log_errors_print.
    
    Args:
        currency_codes (list): Список кодов валют.
        url (str, optional): URL API ЦБ РФ.
        
    Returns:
        dict: Словарь с курсами валют.
        
    Raises:
        KeyError: Если в ответе API нет ключа 'Valute' или запрошенной валюты.
        Exception: При ошибках HTTP-запроса или парсинга JSON.
    """

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    if 'Valute' not in data:
        raise KeyError("Нет ключа 'Valute'")
    
    result = {}
    for code in currency_codes:
        if code not in data['Valute']:
            raise KeyError(f"Нет валюты {code}")
        result[code] = data['Valute'][code]['Value']
    return result

# =============== ИТЕРАЦИЯ 3 ===============
logging.basicConfig(
    level=logging.ERROR,
    format='ERROR: %(message)s',
    stream=sys.stdout
)

def log_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Ошибка: {e}")
            return None
    return wrapper

@log_errors
def get_currencies(currency_codes, url="https://www.cbr-xml-daily.ru/daily_json.js"):
    """
    Возвращает курсы валют для указанных кодов (3 версия).
    
    Итерация 3: версия с использованием модуля logging.
    Обработка ошибок делегирована декоратору log_errors.
    
    Args:
        currency_codes (list): Список кодов валют (например, ['USD', 'EUR'])
        url (str, optional): URL API ЦБ РФ. По умолчанию используется официальный.
        
    Returns:
        dict or None: Словарь вида {'USD': 92.5, 'EUR': 99.8} или None при ошибке.
        
    Notes:
        При ошибке функция возвращает None, а ошибка логируется через модуль logging
        в стандартный поток вывода (sys.stdout).
    """
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    if 'Valute' not in data:
        raise KeyError("Нет ключа 'Valute'")
    
    result = {}
    for code in currency_codes:
        if code not in data['Valute']:
            raise KeyError(f"Нет валюты {code}")
        result[code] = data['Valute'][code]['Value']
    return result
```
---
### Тест
0. Поставленная задача:  
Удостоверьтесь, что решение проходит тесты
1. Код программы:

```py
import unittest
from unittest.mock import patch, Mock
from io import StringIO
import sys

from task import get_currencies_v1, get_currencies_v2, get_currencies

class TestTaskSimple(unittest.TestCase):
    
    def test_all_versions_return_dict(self):
        for func in [get_currencies_v1, get_currencies_v2, get_currencies]:
            result = func(['USD', 'EUR'])
            self.assertIsInstance(result, dict)
            self.assertIn('USD', result)
            self.assertIn('EUR', result)
    
    def test_all_versions_return_none_on_error(self):
        for func in [get_currencies_v1, get_currencies_v2, get_currencies]:
            result = func(['XXX'])
            self.assertIsNone(result)
    
    def test_v1_prints_error(self):
        captured = StringIO()
        sys.stdout = captured
        get_currencies_v1(['XXX'])
        sys.stdout = sys.__stdout__
        self.assertIn('XXX', captured.getvalue())
    
    def test_v2_prints_error(self):
        captured = StringIO()
        sys.stdout = captured
        get_currencies_v2(['XXX'])
        sys.stdout = sys.__stdout__
        self.assertIn('XXX', captured.getvalue())
    
    def test_mocked_api_error(self):
        mock_response = Mock()
        mock_response.json.return_value = {"foo": "bar"}
        mock_response.raise_for_status = Mock()
        
        with patch('task.requests.get', return_value=mock_response):
            for func in [get_currencies_v1, get_currencies_v2, get_currencies]:
                result = func(['USD'])
                self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
```

2. Результат выполненной работы:  
.Нет валюты XXX
Ошибка: 'Нет валюты XXX'
ERROR: Ошибка: 'Нет валюты XXX'
.Ошибка
Ошибка: "Нет ключа 'Valute'"
ERROR: Ошибка: "Нет ключа 'Valute'"
...
----------------------------------------------------------------------
Ran 5 tests in 0.846s

OK
---