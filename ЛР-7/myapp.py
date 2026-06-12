#!/usr/bin/env python3
"""
Запускает HTTP сервер и маршрутизирует запросы к соответствующим контроллерам.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from models.author import Author
from models.app import App
from controllers.authorController import AuthorController
from controllers.userController import UserController
from controllers.currenciesController import CurrenciesController


class CurrencyHandler(BaseHTTPRequestHandler):
    """Обработчик HTTP запросов."""
    
    # Классовые переменные для контроллеров (инициализируются при запуске)
    author_controller = None
    user_controller = None
    currencies_controller = None
    
    def do_GET(self):
        """
        Обрабатывает GET запросы.
        Определяет маршрут и вызывает соответствующий контроллер.
        """
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        
        print(f"[GET] Запрос: {path}")
        
        # Маршрутизация
        if path == "/" or path == "/index.html":
            self.author_controller.handle_index(self)
        
        elif path == "/author":
            self.author_controller.handle_author(self)
        
        elif path == "/users":
            self.user_controller.handle_users_list(self)
        
        elif path == "/user":
            user_id_str = query_params.get('id', [''])[0]
            if user_id_str and user_id_str.isdigit():
                self.user_controller.handle_user_detail(self, int(user_id_str))
            else:
                self.send_error(400, "Bad Request")
        
        elif path == "/currencies":
            self.currencies_controller.handle_currencies(self)
        
        elif path.startswith("/static/"):
            self.handle_static(path)
        
        else:
            self.send_error(404, "Not Found")
    
    def do_POST(self):  # ← 4 пробела внутри класса
        """Обрабатывает POST запросы (добавление/удаление подписок)."""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        print(f"[POST] Запрос: {path}")
        
        # Читаем данные из формы
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = parse_qs(post_data)
        
        if path == "/subscribe":
            user_id_str = params.get('user_id', [''])[0]
            currency_id = params.get('currency_id', [''])[0]
            
            if not user_id_str or not currency_id:
                self.send_error(400, "Bad Request")
                return
            
            try:
                user_id = int(user_id_str)
            except ValueError:
                self.send_error(400, "Bad Request")
                return
            
            self.user_controller.handle_add_subscription(self, user_id, currency_id)
        
        elif path == "/unsubscribe":
            user_id_str = params.get('user_id', [''])[0]
            currency_id = params.get('currency_id', [''])[0]
            
            if not user_id_str or not currency_id:
                self.send_error(400, "Bad Request")
                return
            
            try:
                user_id = int(user_id_str)
            except ValueError:
                self.send_error(400, "Bad Request")
                return
            
            self.user_controller.handle_remove_subscription(self, user_id, currency_id)
        
        else:
            self.send_error(404, "Not Found")
    
    def handle_static(self, path: str):
        """
        Отдает статические файлы (CSS, JS, изображения).
        
        Args:
            path: Путь к статическому файлу
        """
        try:
            # Убираем /static/ из пути
            file_path = path.replace('/static/', '', 1)
            
            # Безопасность: запрещаем выход из папки static
            if '..' in file_path:
                self.send_error(403, "Forbidden")
                return
            
            with open(f'static/{file_path}', 'rb') as file:
                content = file.read()
            
            if file_path.endswith('.css'):
                content_type = 'text/css'
            elif file_path.endswith('.js'):
                content_type = 'application/javascript'
            elif file_path.endswith('.png'):
                content_type = 'image/png'
            elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
                content_type = 'image/jpeg'
            elif file_path.endswith('.svg'):
                content_type = 'image/svg+xml'
            else:
                content_type = 'text/plain'
            
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()
            self.wfile.write(content)
            
        except FileNotFoundError:
            self.send_error(404, "File not found")
        except Exception as e:
            self.send_error(500, f"Internal error: {str(e)}")
    
    def log_message(self, format: str, *args):
        """
        Переопределяем формат логов для удобства чтения.
        """
        print(f"[{self.address_string()}] {format % args}")


def run_server(host='localhost', port=8080):
    """
    Запускает HTTP сервер.
    
    Args:
        host: Хост для запуска (по умолчанию localhost)
        port: Порт для запуска (по умолчанию 8080)
    """
    # Создаем данные об авторе и приложении
    author = Author("Чагин Фёдор Сергеевич", "ИВТ-2")
    app = App("LR-7", "1.0.0", author)
    
    app_info = {
        'name': app.name,
        'version': app.version,
        'author': app.author
    }
    
    # Инициализируем контроллеры
    CurrencyHandler.author_controller = AuthorController(app_info)
    CurrencyHandler.user_controller = UserController()
    CurrencyHandler.currencies_controller = CurrenciesController()
    
    # Запускаем сервер
    server_address = (host, port)
    httpd = HTTPServer(server_address, CurrencyHandler)
    
    print(f"""
    ╔════════════════════════════════════════════════════════════════════════════╗
    ║                    LR-7 - Сервер запущен!                  ║
    ╠════════════════════════════════════════════════════════════════════════════╣
    ║  🌐 Адрес: http://{host}:{port}                                              ║
    ║                                                                            ║
    ║  📋 Доступные страницы:                                                     ║
    ║     • Главная:        http://{host}:{port}/                                 ║
    ║     • Об авторе:      http://{host}:{port}/author                           ║
    ║     • Пользователи:   http://{host}:{port}/users                            ║
    ║     • Детали user 1:  http://{host}:{port}/user?id=1                        ║
    ║     • Курсы валют:    http://{host}:{port}/currencies                       ║
    ║                                                                            ║
    ║  ✨ Функционал:                                                             ║
    ║     • Просмотр реальных курсов валют с сайта ЦБ РФ                          ║
    ║     • Добавление и удаление подписок пользователей                          ║
    ╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n Сервер остановлен")
        httpd.server_close()


if __name__ == "__main__":
    run_server()