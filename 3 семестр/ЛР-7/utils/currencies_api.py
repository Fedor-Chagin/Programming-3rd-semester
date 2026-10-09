"""Утилита для получения курсов валют с сайта ЦБ РФ."""

import requests
import logging
import sys
import time
from typing import List, Dict, Optional
from functools import wraps

# Настройка логирования
logging.basicConfig(
    level=logging.ERROR,
    format='ERROR: %(message)s',
    stream=sys.stdout
)

# Кеш для курсов валют
_cache = {
    'data': None,
    'timestamp': 0
}
CACHE_TTL = 300  # Время жизни кеша в секундах (5 минут)

def log_errors(func):
    """Декоратор для логирования ошибок."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Ошибка в {func.__name__}: {e}")
            return None
    return wrapper


def get_currencies_from_api(currency_codes=None, url="https://www.cbr-xml-daily.ru/daily_json.js"):
    """
    Возвращает курсы валют для указанных кодов.
    
    Args:
        currency_codes (list, optional): Список кодов валют (например, ['USD', 'EUR'])
            Если None, возвращает все доступные валюты.
        url (str, optional): URL API ЦБ РФ.
        
    Returns:
        dict or None: Словарь с курсами валют или None при ошибке.
    """
    response = requests.get(url, timeout=10)  # Добавлен timeout
    response.raise_for_status()
    data = response.json()
    
    if 'Valute' not in data:
        raise KeyError("Нет ключа 'Valute' в ответе API")
    
    if currency_codes is None:
        # Возвращаем все валюты
        result = {}
        for code, info in data['Valute'].items():
            result[code] = {
                'char_code': code,
                'name': info['Name'],
                'value': info['Value'],
                'nominal': info['Nominal'],
                'num_code': info['NumCode']
            }
        return result
    else:
        # Возвращаем только запрошенные валюты
        result = {}
        for code in currency_codes:
            if code not in data['Valute']:
                raise KeyError(f"Нет валюты {code}")
            result[code] = data['Valute'][code]['Value']
        return result


def get_all_currencies(force_refresh: bool = False) -> List[Dict]:
    """
    Получает все валюты с кешированием.
    
    Args:
        force_refresh: Если True, игнорирует кеш и запрашивает новые данные
        
    Returns:
        List[Dict]: Список словарей с данными о валютах для создания объектов Currency
    """
    global _cache
    
    current_time = time.time()
    
    # Если кеш валиден и не требуется принудительное обновление
    if not force_refresh and _cache['data'] is not None and (current_time - _cache['timestamp']) < CACHE_TTL:
        print(f"[КЕШ] Используем кешированные курсы (возраст: {int(current_time - _cache['timestamp'])} сек.)")
        return _cache['data']
    
    print("[API] Запрашиваем свежие курсы с сайта ЦБ РФ...")
    
    # Проверяем интернет-соединение
    try:
        requests.get("https://www.cbr.ru", timeout=5)
    except requests.RequestException:
        print("[ОШИБКА] Нет соединения с интернетом, используем кеш")
        if _cache['data'] is not None:
            return _cache['data']
    
    data = get_currencies_from_api()
    
    if data is None:
        print("[ОШИБКА] Не удалось получить курсы, используем кеш")
        if _cache['data'] is not None:
            return _cache['data']
        # Возвращаем тестовые данные при первой ошибке
        return get_mock_currencies()
    
    currencies = []
    for char_code, info in data.items():
        currency = {
            'id': f"ID_{char_code}",
            'num_code': info.get('num_code', 0),
            'char_code': char_code,
            'name': info['name'],
            'value': info['value'],
            'nominal': info['nominal']
        }
        currencies.append(currency)
    
    # Сохраняем в кеш
    _cache['data'] = currencies
    _cache['timestamp'] = current_time
    
    print(f"[API] Получено {len(currencies)} валют, кеш обновлён")
    
    return currencies


def get_mock_currencies() -> List[Dict]:
    """Возвращает тестовые данные при отсутствии интернета."""
    return [
        {
            'id': 'R01235',
            'num_code': 840,
            'char_code': 'USD',
            'name': 'Доллар США',
            'value': 92.50,
            'nominal': 1
        },
        {
            'id': 'R01239',
            'num_code': 978,
            'char_code': 'EUR',
            'name': 'Евро',
            'value': 99.80,
            'nominal': 1
        },
        {
            'id': 'R01375',
            'num_code': 156,
            'char_code': 'CNY',
            'name': 'Китайский юань',
            'value': 12.75,
            'nominal': 1
        },
        {
            'id': 'R01820',
            'num_code': 392,
            'char_code': 'JPY',
            'name': 'Японская иена',
            'value': 58.30,
            'nominal': 100
        }
    ]


# Для обратной совместимости с текущим кодом
def get_currencies(force_refresh: bool = False) -> List[Dict]:
    """Обёртка для get_all_currencies."""
    return get_all_currencies(force_refresh)