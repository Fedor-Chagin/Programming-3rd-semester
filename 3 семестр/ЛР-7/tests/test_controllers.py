"""Модульные тесты для контроллеров."""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers.userController import UserController


class MockHandler:
    """Мок-объект для HTTP handler."""
    def send_response(self, code):
        self.response_code = code
    
    def send_header(self, key, value):
        pass
    
    def end_headers(self):
        pass
    
    def wfile_write(self, data):
        pass


class TestUserController(unittest.TestCase):
    """Тесты для UserController."""
    
    def setUp(self):
        """Подготовка тестового окружения."""
        self.controller = UserController()
        self.mock_handler = MockHandler()
    
    def test_users_list_not_empty(self):
        """Тест: список пользователей не пуст."""
        self.assertGreater(len(self.controller.users), 0)
    
    def test_user_exists(self):
        """Тест: пользователь с ID=1 существует."""
        self.assertIn(1, self.controller.users)
    
    def test_user_has_correct_name(self):
        """Тест: проверка имени пользователя."""
        user = self.controller.users.get(1)
        self.assertIsNotNone(user)
        self.assertEqual(user.name, "Иван Петров")
    
    def test_user_count(self):
        """Тест: количество пользователей."""
        self.assertEqual(len(self.controller.users), 3)
    
    def test_subscriptions_exist(self):
        """Тест: подписки существуют."""
        self.assertGreater(len(self.controller.subscriptions), 0)
    
    def test_user_1_has_subscriptions(self):
        """Тест: пользователь 1 имеет подписки."""
        user_subs = [s for s in self.controller.subscriptions if s.user_id == 1]
        self.assertGreater(len(user_subs), 0)


if __name__ == "__main__":
    unittest.main()