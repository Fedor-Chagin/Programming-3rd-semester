"""Контроллер для обработки маршрутов /users и /user."""

from jinja2 import Environment, FileSystemLoader
import os
import random
from datetime import datetime, timedelta
from models.user import User
from models.user_currency import UserCurrency


class UserController:
    """Контроллер для работы с пользователями."""
    
    def __init__(self):
        """Инициализация с тестовыми данными."""
        template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
        self.env = Environment(loader=FileSystemLoader(template_dir))
        
        # Тестовые данные
        self.users = {
            1: User(1, "Иван Петров"),
            2: User(2, "Мария Сидорова"),
            3: User(3, "Алексей Иванов")
        }
        
        # Подписки пользователей (subscription_id, user_id, currency_id)
        self.subscriptions = [
            UserCurrency(1, 1, "R01235"),  # Иван подписан на USD
            UserCurrency(2, 1, "R01239"),  # Иван подписан на EUR
            UserCurrency(3, 2, "R01235"),  # Мария подписана на USD
        ]
    
    def _generate_history(self, char_code: str) -> list:
        """Генерирует историю курса валюты за последние 3 месяца."""
        # Расширенные базовые курсы для разных валют
        base_rates = {
            "USD": 92.50, "EUR": 99.80, "CNY": 12.75,
            "GBP": 118.50, "JPY": 0.58, "CHF": 102.30,
            "CAD": 67.80, "AUD": 61.20, "TRY": 2.85
        }
        base = base_rates.get(char_code, 70.0)
        
        history = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)
        
        current_date = start_date
        while current_date <= end_date:
            days_passed = (current_date - start_date).days
            trend = (days_passed / 90) * random.uniform(-5, 5)
            variation = random.uniform(-1, 1)
            rate = round(base + trend + variation, 2)
            
            history.append({
                'date': current_date.strftime('%d.%m'),
                'rate': rate
            })
            current_date += timedelta(days=7)
        
        return history
    
    def handle_users_list(self, handler) -> None:
        """Обрабатывает GET запрос к /users - список пользователей."""
        template = self.env.get_template('users.html')
        users_list = [user.to_dict() for user in self.users.values()]
        
        html_content = template.render(users=users_list, title="Список пользователей")
        
        handler.send_response(200)
        handler.send_header('Content-type', 'text/html; charset=utf-8')
        handler.end_headers()
        handler.wfile.write(html_content.encode('utf-8'))
    
    def handle_user_detail(self, handler, user_id: int) -> None:
        """Обрабатывает GET запрос к /user?id=X."""
        if user_id not in self.users:
            handler.send_response(404)
            handler.send_header('Content-type', 'text/html; charset=utf-8')
            handler.end_headers()
            handler.wfile.write("<h1>Пользователь не найден</h1>".encode('utf-8'))
            return
        
        user = self.users[user_id]
        
        # Получаем все доступные валюты
        from utils.currencies_api import get_currencies
        all_currencies_data = get_currencies()
        
        all_currencies = []
        for currency in all_currencies_data:
            all_currencies.append({
                'id': currency['id'],
                'char_code': currency['char_code'],
                'name': currency['name']
            })
        
        # Находим подписки пользователя
        user_currency_ids = []
        for sub in self.subscriptions:
            if sub.user_id == user_id:
                user_currency_ids.append(sub.currency_id)
        
        # Названия валют (теперь из API)
        currency_names = {}
        for currency in all_currencies_data:
            currency_names[currency['id']] = {
                'char_code': currency['char_code'],
                'name': currency['name']
            }
        
        # Формируем данные с историей для графиков
        subscriptions_with_data = []
        for currency_id in user_currency_ids:
            if currency_id in currency_names:
                currency = currency_names[currency_id]
                history = self._generate_history(currency['char_code'])
                subscriptions_with_data.append({
                    'id': currency_id,
                    'char_code': currency['char_code'],
                    'name': currency['name'],
                    'history': history
                })
        
        template = self.env.get_template('user_detail.html')
        html_content = template.render(
            user=user.to_dict(),
            subscriptions=subscriptions_with_data,
            all_currencies=all_currencies,  # ← передаём все валюты
            title=f"Пользователь: {user.name}"
        )
        
        handler.send_response(200)
        handler.send_header('Content-type', 'text/html; charset=utf-8')
        handler.end_headers()
        handler.wfile.write(html_content.encode('utf-8'))
    
    def handle_add_subscription(self, handler, user_id: int, currency_id: str) -> None:
        """Добавляет подписку пользователя на валюту."""
        if user_id not in self.users:
            handler.send_response(404)
            handler.wfile.write("User not found".encode('utf-8'))
            return
        
        # Проверяем, нет ли уже такой подписки
        for sub in self.subscriptions:
            if sub.user_id == user_id and sub.currency_id == currency_id:
                handler.send_response(302)
                handler.send_header('Location', f'/user?id={user_id}')
                handler.end_headers()
                return
        
        # Создаём новую подписку
        new_id = max([s.id for s in self.subscriptions], default=0) + 1
        self.subscriptions.append(UserCurrency(new_id, user_id, currency_id))
        
        handler.send_response(302)
        handler.send_header('Location', f'/user?id={user_id}')
        handler.end_headers()
    
    def handle_remove_subscription(self, handler, user_id: int, currency_id: str) -> None:
        """Удаляет подписку пользователя."""
        self.subscriptions = [s for s in self.subscriptions 
                              if not (s.user_id == user_id and s.currency_id == currency_id)]
        
        handler.send_response(302)
        handler.send_header('Location', f'/user?id={user_id}')
        handler.end_headers()