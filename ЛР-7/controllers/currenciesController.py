"""Контроллер для обработки маршрута /currencies."""

from jinja2 import Environment, FileSystemLoader
import os
from utils.currencies_api import get_currencies
from models.currency import Currency


class CurrenciesController:  # ← С БОЛЬШОЙ БУКВЫ!
    """Контроллер для отображения курсов валют."""
    
    def __init__(self):
        """Инициализация контроллера."""
        template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
        self.env = Environment(loader=FileSystemLoader(template_dir))
    
    def handle_currencies(self, handler) -> None:
        """Обрабатывает GET запрос к /currencies."""
        try:
            currencies_data = get_currencies()
            
            currencies = []
            for data in currencies_data:
                currency = Currency(
                    currency_id=data['id'],
                    char_code=data['char_code'],
                    name=data['name'],
                    value=data['value'],
                    nominal=data['nominal']
                )
                currencies.append(currency)
            
            template = self.env.get_template('currencies.html')
            
            html_content = template.render(
                currencies=[c.to_dict() for c in currencies],
                title="Курсы валют ЦБ РФ"
            )
            
            handler.send_response(200)
            handler.send_header('Content-type', 'text/html; charset=utf-8')
            handler.end_headers()
            handler.wfile.write(html_content.encode('utf-8'))
            
        except Exception as e:
            handler.send_response(500)
            handler.send_header('Content-type', 'text/html; charset=utf-8')
            handler.end_headers()
            handler.wfile.write(f"<h1>Ошибка загрузки курсов</h1><p>{str(e)}</p>".encode('utf-8'))