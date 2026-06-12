# ЛР-7

---
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python myapp.py


(venv) fedorcagin@MacBook-Pro13 ЛР-7 % python myapp.py

    ╔════════════════════════════════════════════════════════════════════════════╗
    ║                    LR-7 - Сервер запущен!                  ║
    ╠════════════════════════════════════════════════════════════════════════════╣
    ║  🌐 Адрес: http://localhost:8080                                              ║
    ║                                                                            ║
    ║  📋 Доступные страницы:                                                     ║
    ║     • Главная:        http://localhost:8080/                                 ║
    ║     • Об авторе:      http://localhost:8080/author                           ║
    ║     • Пользователи:   http://localhost:8080/users                            ║
    ║     • Детали user 1:  http://localhost:8080/user?id=1                        ║
    ║     • Курсы валют:    http://localhost:8080/currencies                       ║
    ║                                                                            ║
    ║  ✨ Функционал:                                                             ║
    ║     • Просмотр реальных курсов валют с сайта ЦБ РФ                          ║
    ║     • Добавление и удаление подписок пользователей                          ║
    ╚════════════════════════════════════════════════════════════════════════════╝
```
* ### Цель работы
Создать простое клиент-серверное приложение на Python без серверных фреймворков. 
Освоить работу с HTTPServer и маршрутизацию запросов. 
Применять шаблонизатор Jinja2 для отображения данных. 
Реализовать модели предметной области (User, Currency, UserCurrency, App, Author) с геттерами и сеттерами. Структурировать код в соответствии с архитектурой MVC. 
Получать данные о курсах валют через функцию get_currencies и отображать их пользователям. 
Реализовать функциональность подписки пользователей на валюты и отображение динамики их изменения. 
Научиться создавать тесты для моделей и серверной логики.

* ### Описание предметной области
Приложение предназначено для мониторинга курсов валют и управления подписками пользователей.
### Модели предметной области:

Author — автор приложения. Содержит поля: имя (name) и учебная группа (group).
App — приложение. Содержит название (name), версию (version) и ссылку на автора (author).
User — пользователь системы. Содержит уникальный идентификатор (id) и имя (name).
Currency — валюта. Содержит уникальный идентификатор (id), цифровой код (num_code), символьный код (char_code), название (name), курс к рублю (value), номинал (nominal).
UserCurrency — подписка пользователя на валюту. Содержит идентификатор подписки (id), идентификатор пользователя (user_id) и идентификатор валюты (currency_id). Реализует связь "многие ко многим" между User и Currency.
Связи между моделями:

User и Currency связаны через UserCurrency (многие ко многим)
App содержит ссылку на Author (один к одному)
Функциональность:

Получение актуальных курсов валют с сайта ЦБ РФ
Просмотр списка пользователей
Добавление и удаление подписок пользователей на валюты
Отображение графиков динамики курсов за 3 месяца


* ### Примеры работы приложения:

![alt text](<Снимок экрана 2026-06-12 в 22.09.26.png>)

![alt text](<Снимок экрана 2026-06-12 в 22.09.35.png>)

![alt text](<Снимок экрана 2026-06-12 в 22.09.42.png>)

![alt text](<Снимок экрана 2026-06-12 в 22.10.57.png>)

![alt text](<Снимок экрана 2026-06-12 в 22.11.14.png>)
* ### Результат прохождения тестов:

(venv) fedorcagin@MacBook-Pro13 ЛР-7 % python -m unittest discover tests -v
test_get_currencies_contains_valid_structure (test_api.TestCurrenciesAPI.test_get_currencies_contains_valid_structure)
Тест: каждый элемент списка содержит необходимые ключи. ... [API] Запрашиваем свежие курсы с сайта ЦБ РФ...
[API] Получено 54 валют, кеш обновлён
ok
test_get_currencies_returns_list (test_api.TestCurrenciesAPI.test_get_currencies_returns_list)
Тест: функция возвращает список. ... [КЕШ] Используем кешированные курсы (возраст: 0 сек.)
ok
test_mock_currencies_have_usd (test_api.TestCurrenciesAPI.test_mock_currencies_have_usd)
Тест: в мок-данных есть USD. ... ok
test_mock_currencies_returns_list (test_api.TestCurrenciesAPI.test_mock_currencies_returns_list)
Тест: мок-данные возвращают список. ... ok
test_subscriptions_exist (test_controllers.TestUserController.test_subscriptions_exist)
Тест: подписки существуют. ... ok
test_user_1_has_subscriptions (test_controllers.TestUserController.test_user_1_has_subscriptions)
Тест: пользователь 1 имеет подписки. ... ok
test_user_count (test_controllers.TestUserController.test_user_count)
Тест: количество пользователей. ... ok
test_user_exists (test_controllers.TestUserController.test_user_exists)
Тест: пользователь с ID=1 существует. ... ok
test_user_has_correct_name (test_controllers.TestUserController.test_user_has_correct_name)
Тест: проверка имени пользователя. ... ok
test_users_list_not_empty (test_controllers.TestUserController.test_users_list_not_empty)
Тест: список пользователей не пуст. ... ok
test_app_creation (test_models.TestApp.test_app_creation)
Тест создания приложения с корректными данными. ... ok
test_author_creation (test_models.TestAuthor.test_author_creation)
Тест создания автора с корректными данными. ... ok
test_author_group_setter (test_models.TestAuthor.test_author_group_setter)
Тест сеттера группы. ... ok
test_author_name_setter (test_models.TestAuthor.test_author_name_setter)
Тест сеттера имени. ... ok
test_currency_creation (test_models.TestCurrency.test_currency_creation)
Тест создания валюты с корректными данными. ... ok
test_currency_rate_per_unit (test_models.TestCurrency.test_currency_rate_per_unit)
Тест расчёта курса за единицу валюты. ... ok
test_currency_rate_per_unit_with_nominal (test_models.TestCurrency.test_currency_rate_per_unit_with_nominal)
Тест расчёта курса с учётом номинала. ... ok
test_currency_to_dict (test_models.TestCurrency.test_currency_to_dict)
Тест преобразования валюты в словарь. ... ok
test_user_creation (test_models.TestUser.test_user_creation)
Тест создания пользователя с корректными данными. ... ok
test_user_to_dict (test_models.TestUser.test_user_to_dict)
Тест преобразования пользователя в словарь. ... ok
test_user_currency_creation (test_models.TestUserCurrency.test_user_currency_creation)
Тест создания подписки с корректными данными. ... ok

----------------------------------------------------------------------
Ran 21 tests in 0.206s

OK
(venv) fedorcagin@MacBook-Pro13 ЛР-7 %

* ### Структура проекта 
```
myapp/
├── controllers/               # Контроллеры - обрабатывают запросы и связывают модели с шаблонами
│   ├── __init__.py           # Делает папку Python-пакетом (может быть пустым)
│   ├── authorController.py   # Отвечает за главную страницу / и страницу /author
│   ├── userController.py     # Отвечает за список пользователей /users и детали /user?id=
│   └── currenciesController.py # Отвечает за страницу с курсами валют /currencies
│
├── models/                    # Модели - хранят данные и бизнес-логику
│   ├── __init__.py           # Делает папку Python-пакетом
│   ├── author.py             # Класс Author: имя и группа автора
│   ├── app.py                # Класс App: название и версия приложения
│   ├── user.py               # Класс User: id и имя пользователя
│   ├── currency.py           # Класс Currency: код, курс, номинал валюты
│   └── user_currency.py      # Класс UserCurrency: связь пользователя с валютой (подписка)
│
├── templates/                 # Шаблоны HTML для отображения данных пользователю
│   ├── index.html            # Главная страница с информацией о приложении
│   ├── users.html            # Список всех пользователей
│   ├── user_detail.html      # Детальная страница пользователя с подписками и графиками
│   └── currencies.html       # Таблица с актуальными курсами валют
│
├── static/
│   └── css/                  # Стили оформления страниц
│       └── style.css
│
├── utils/                     # Утилиты - вспомогательные функции
│   ├── __init__.py           # Делает папку Python-пакетом
│   └── currencies_api.py     # Функция get_currencies(): запрос к API ЦБ РФ и парсинг курсов
│
└── myapp.py                   # Точка входа: запуск HTTP-сервера и маршрутизация запросов
```

* ### Выводы

В ходе выполнения лабораторной работы было разработано клиент-серверное приложение для мониторинга курсов валют. 

Реализованы все требования:
- Модели User, Currency, UserCurrency, App, Author с геттерами/сеттерами
- HTTP-сервер на HTTPServer с маршрутизацией
- Шаблоны Jinja2
- Интеграция с API ЦБ РФ
- Подписки пользователей на валюты
- Графики динамики курсов (доп. задание)
- Тесты для моделей и API

Архитектура MVC соблюдена. Все тесты проходят успешно. Приложение работает стабильно.
