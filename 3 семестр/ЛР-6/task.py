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