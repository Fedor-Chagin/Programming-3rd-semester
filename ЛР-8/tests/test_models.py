"""Модульные тесты для моделей данных."""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.author import Author
from models.user import User
from models.currency import Currency
from models.user_currency import UserCurrency
from models.app import App


class TestAuthor(unittest.TestCase):
    """Тесты для модели Author."""
    
    def test_author_creation(self):
        """Тест создания автора с корректными данными."""
        author = Author("Чагин Ф.С.", "ИВТ-2")
        self.assertEqual(author.name, "Чагин Ф.С.")
        self.assertEqual(author.group, "ИВТ-2")
    
    def test_author_name_setter(self):
        """Тест сеттера имени."""
        author = Author("Чагин Ф.С.", "ИВТ-2")
        author.name = "Новое имя"
        self.assertEqual(author.name, "Новое имя")
    
    def test_author_group_setter(self):
        """Тест сеттера группы."""
        author = Author("Чагин Ф.С.", "ИВТ-2")
        author.group = "Новая группа"
        self.assertEqual(author.group, "Новая группа")


class TestUser(unittest.TestCase):
    """Тесты для модели User."""
    
    def test_user_creation(self):
        """Тест создания пользователя с корректными данными."""
        user = User(1, "Тестовый пользователь")
        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, "Тестовый пользователь")
    
    def test_user_to_dict(self):
        """Тест преобразования пользователя в словарь."""
        user = User(5, "Тест")
        self.assertEqual(user.to_dict(), {'id': 5, 'name': 'Тест'})


class TestCurrency(unittest.TestCase):
    """Тесты для модели Currency."""
    
    def test_currency_creation(self):
        """Тест создания валюты с корректными данными."""
        currency = Currency("R01235", "USD", "Доллар США", 92.50, 1)
        self.assertEqual(currency.char_code, "USD")
        self.assertEqual(currency.value, 92.50)
        self.assertEqual(currency.nominal, 1)
    
    def test_currency_rate_per_unit(self):
        """Тест расчёта курса за единицу валюты."""
        currency = Currency("R01235", "USD", "Доллар США", 92.50, 1)
        self.assertEqual(currency.get_rate_per_unit(), 92.50)
    
    def test_currency_rate_per_unit_with_nominal(self):
        """Тест расчёта курса с учётом номинала."""
        currency = Currency("R01820", "JPY", "Японская иена", 58.30, 100)
        self.assertAlmostEqual(currency.get_rate_per_unit(), 0.583, places=3)
    
    def test_currency_to_dict(self):
        """Тест преобразования валюты в словарь."""
        currency = Currency("R01235", "USD", "Доллар США", 92.50, 1)
        result = currency.to_dict()
        self.assertEqual(result['char_code'], "USD")
        self.assertIn('rate_per_unit', result)


class TestUserCurrency(unittest.TestCase):
    """Тесты для модели UserCurrency."""
    
    def test_user_currency_creation(self):
        """Тест создания подписки с корректными данными."""
        sub = UserCurrency(1, 5, "R01235")
        self.assertEqual(sub.id, 1)
        self.assertEqual(sub.user_id, 5)
        self.assertEqual(sub.currency_id, "R01235")


class TestApp(unittest.TestCase):
    """Тесты для модели App."""
    
    def test_app_creation(self):
        """Тест создания приложения с корректными данными."""
        author = Author("Чагин Ф.С.", "ИВТ-2")
        app = App("LR-7", "1.0.0", author)
        self.assertEqual(app.name, "LR-7")
        self.assertEqual(app.version, "1.0.0")
        self.assertEqual(app.author.name, "Чагин Ф.С.")


if __name__ == "__main__":
    unittest.main()