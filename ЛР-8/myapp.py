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
from controllers.databaseController import CurrencyRatesCRUD  # НОВЫЙ импорт


class CurrencyHandler(BaseHTTPRequestHandler):
    """Обработчик HTTP запросов."""
    
    # Классовые переменные для контроллеров (инициализируются при запуске)
    author_controller = None
    user_controller = None
    currencies_controller = None
    db_controller = None  # НОВОЕ: контроллер БД
    
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
        
        # ==================== НОВЫЕ МАРШРУТЫ ДЛЯ CRUD ====================
        
        elif path == "/currency/delete":
            currency_id_str = query_params.get('id', [''])[0]
            if currency_id_str and currency_id_str.isdigit():
                self.currencies_controller.handle_delete_currency(self, int(currency_id_str))
            else:
                self.send_error(400, "Bad Request: missing or invalid id")
        
        elif path == "/currency/update":
            char_code = query_params.get('char_code', [''])[0]
            value_str = query_params.get('value', [''])[0]
            
            if char_code and value_str:
                try:
                    value = float(value_str)
                    self.currencies_controller.handle_update_currency(self, char_code, value)
                except ValueError:
                    self.send_error(400, "Bad Request: invalid value")
            else:
                self.send_error(400, "Bad Request: missing char_code or value")
        
        elif path == "/currency/create":
            char_code = query_params.get('char_code', [''])[0]
            num_code = query_params.get('num_code', [''])[0]
            name = query_params.get('name', [''])[0]
            value_str = query_params.get('value', [''])[0]
            nominal_str = query_params.get('nominal', ['1'])[0]
            
            if char_code and name and value_str:
                try:
                    value = float(value_str)
                    nominal = int(nominal_str)
                    self.db_controller.create_currency(num_code, char_code, name, value, nominal)
                    # Перенаправляем обратно на страницу валют
                    self.send_response(302)
                    self.send_header('Location', '/currencies')
                    self.end_headers()
                except ValueError:
                    self.send_error(400, "Bad Request: invalid value or nominal")
            else:
                self.send_error(400, "Bad Request: missing required fields (char_code, name, value)")
        
        elif path == "/currency/show":
            self.currencies_controller.handle_show_currencies_console(self)
        
        elif path.startswith("/static/"):
            self.handle_static(path)
        
        else:
            self.send_error(404, "Not Found")
    
    def do_POST(self):
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
    # НОВОЕ: инициализация БД
    db_controller = CurrencyRatesCRUD()
    
    # Создаем данные об авторе и приложении
    author = Author("Чагин Фёдор Сергеевич", "ИВТ-2")
    app = App("LR-8", "1.0.0", author)
    
    app_info = {
        'name': app.name,
        'version': app.version,
        'author': app.author
    }
    
    # Инициализируем контроллеры (передаём db_controller в CurrenciesController)
    CurrencyHandler.author_controller = AuthorController(app_info)
    CurrencyHandler.user_controller = UserController()
    CurrencyHandler.currencies_controller = CurrenciesController(db_controller)
    CurrencyHandler.db_controller = db_controller
    
    # Запускаем сервер
    server_address = (host, port)
    httpd = HTTPServer(server_address, CurrencyHandler)
    
    print(f"""
    ╔════════════════════════════════════════════════════════════════════════════╗
    ║                    LR-8 - Сервер запущен!                                  ║
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
    ║  ✨ Новый функционал (CRUD):                                                ║
    ║     • Удалить валюту:   /currency/delete?id=X                              ║
    ║     • Обновить курс:    /currency/update?USD=92.50                         ║
    ║     • Добавить валюту:  /currency/create?char_code=USD&name=...            ║
    ║     • Вывод в консоль:   /currency/show                                     ║
    ║                                                                            ║
    ║  ⚠️  Для остановки сервера нажмите Ctrl+C                                   ║
    ╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n Сервер остановлен")
        httpd.server_close()
        db_controller.close()  # Закрываем соединение с БД


if __name__ == "__main__":
    run_server()