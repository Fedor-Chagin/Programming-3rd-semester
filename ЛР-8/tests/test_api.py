"""Модульные тесты для API получения курсов валют."""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.currencies_api import get_currencies, get_mock_currencies


class TestCurrenciesAPI(unittest.TestCase):
    """Тесты для функций получения курсов валют."""
    
    def test_get_currencies_returns_list(self):
        """Тест: функция возвращает список."""
        result = get_currencies()
        self.assertIsInstance(result, list)
    
    def test_get_currencies_contains_valid_structure(self):
        """Тест: каждый элемент списка содержит необходимые ключи."""
        result = get_currencies()
        if result:
            first = result[0]
            required_keys = ['id', 'char_code', 'name', 'value', 'nominal']
            for key in required_keys:
                self.assertIn(key, first)
    
    def test_mock_currencies_returns_list(self):
        """Тест: мок-данные возвращают список."""
        result = get_mock_currencies()
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
    
    def test_mock_currencies_have_usd(self):
        """Тест: в мок-данных есть USD."""
        result = get_mock_currencies()
        usd = [c for c in result if c['char_code'] == 'USD']
        self.assertGreater(len(usd), 0)


if __name__ == "__main__":
    unittest.main()