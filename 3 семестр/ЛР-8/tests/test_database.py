"""Тесты для databaseController."""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers.databaseController import CurrencyRatesCRUD


class TestDatabaseController(unittest.TestCase):
    
    def setUp(self):
        """Создаём чистую БД перед каждым тестом."""
        self.db = CurrencyRatesCRUD()
    
    def test_create_currency(self):
        """Тест добавления валюты."""
        new_id = self.db.create_currency("826", "GBP", "Фунт стерлингов", 120.50, 1)
        self.assertIsNotNone(new_id)
        
        currency = self.db.read_currency_by_id(new_id)
        self.assertEqual(currency['char_code'], "GBP")
        self.assertEqual(currency['value'], 120.50)
    
    def test_read_currencies(self):
        """Тест чтения всех валют."""
        currencies = self.db.read_currencies()
        self.assertGreater(len(currencies), 0)
    
    def test_update_currency(self):
        """Тест обновления курса."""
        # Получаем USD (id=1)
        success = self.db.update_currency_value(1, 95.00)
        self.assertTrue(success)
        
        updated = self.db.read_currency_by_id(1)
        self.assertEqual(updated['value'], 95.00)
    
    def test_delete_currency(self):
        """Тест удаления валюты."""
        # Сначала создаём
        new_id = self.db.create_currency("999", "XXX", "Тест", 100, 1)
        
        # Проверяем, что создалась
        self.assertIsNotNone(self.db.read_currency_by_id(new_id))
        
        # Удаляем
        success = self.db.delete_currency(new_id)
        self.assertTrue(success)
        
        # Проверяем, что исчезла
        self.assertIsNone(self.db.read_currency_by_id(new_id))


if __name__ == "__main__":
    unittest.main()