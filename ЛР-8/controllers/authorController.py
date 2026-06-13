"""Контроллер для обработки маршрутов / и /author."""

from jinja2 import Environment, FileSystemLoader
import os

class AuthorController:
    """Контроллер для страниц об авторе и главной."""
    
    def __init__(self, app_info: dict):
        """
        Инициализация контроллера.
        
        Args:
            app_info: Словарь с информацией о приложении
        """
        self.app_info = app_info
        # Настраиваем Jinja2 для поиска шаблонов в папке templates
        template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
        self.env = Environment(loader=FileSystemLoader(template_dir))
    
    def handle_index(self, handler) -> None:
        """
        Обрабатывает GET запрос к главной странице (/).
        
        Args:
            handler: HTTP обработчик (будет передан из сервера)
        """
        template = self.env.get_template('index.html')
        
        html_content = template.render(
            app_name=self.app_info['name'],
            app_version=self.app_info['version'],
            author=self.app_info['author']
        )
        
        handler.send_response(200)
        handler.send_header('Content-type', 'text/html; charset=utf-8')
        handler.end_headers()
        handler.wfile.write(html_content.encode('utf-8'))
    
    def handle_author(self, handler) -> None:
        """
        Обрабатывает GET запрос к /author.
        
        Args:
            handler: HTTP обработчик
        """
        template = self.env.get_template('author.html')
        
        html_content = template.render(
            author=self.app_info['author']
        )
        
        handler.send_response(200)
        handler.send_header('Content-type', 'text/html; charset=utf-8')
        handler.end_headers()
        handler.wfile.write(html_content.encode('utf-8'))