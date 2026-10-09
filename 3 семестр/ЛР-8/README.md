# ЛР-8

---
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python myapp.py


(venv) fedorcagin@MacBook-Pro13 LR-8 % python myapp.py

    ╔════════════════════════════════════════════════════════════════════════════╗
    ║                    LR-8 - Сервер запущен!                                  ║
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
    ║  ✨ Новый функционал (CRUD):                                                ║
    ║     • Удалить валюту:   /currency/delete?id=X                              ║
    ║     • Обновить курс:    /currency/update?USD=92.50                         ║
    ║     • Добавить валюту:  /currency/create?char_code=USD&name=...            ║
    ║     • Вывод в консоль:   /currency/show                                     ║
    ║                                                                            ║
    ║  ⚠️  Для остановки сервера нажмите Ctrl+C                                   ║
    ╚════════════════════════════════════════════════════════════════════════════╝

```
* ### Цель работы
Реализовать CRUD (Create, Read, Update, Delete) для сущностей бизнес-логики приложения.
Освоить работу с SQLite в памяти (:memory:) через модуль sqlite3.
Понять принципы первичных и внешних ключей и их роль в связях между таблицами.
Выделить контроллеры для работы с БД и для рендеринга страниц в отдельные модули.
Использовать архитектуру MVC и соблюдать разделение ответственности.
Отображать пользователям таблицу с валютами, на которые они подписаны.
Реализовать полноценный роутер, который обрабатывает GET-запросы и выполняет сохранение/обновление данных и рендеринг страниц.
Научиться тестировать функционал на примере сущностей currency и user с использованием unittest.mock.

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
* ### Функциональность:

Получение актуальных курсов валют с сайта ЦБ РФ
Просмотр списка пользователей
Добавление и удаление подписок пользователей на валюты
Отображение графиков динамики курсов за 3 месяца
CRUD операции для валют (создание, чтение, обновление, удаление)

Реализация CRUD операций

1. Create (Создание) — добавление новой валюты

Пользователь заполняет форму на странице /currencies:

Код валюты (например, GBP)
Название (Фунт стерлингов)
Курс (120.50)
Номинал (1)
SQL-запрос:

```sql
INSERT INTO currency(char_code, name, value, nominal) 
VALUES ('GBP', 'Фунт стерлингов', 120.50, 1)
```
2. Read (Чтение) — отображение всех валют

При загрузке страницы /currencies сервер читает все записи из таблицы currency.

SQL-запрос:

```sql
SELECT * FROM currency
```
3. Update (Обновление) — изменение курса валюты

Пользователь выбирает валюту (например, USD) и вводит новый курс (95.00).

SQL-запрос:

```sql
UPDATE currency SET value = 95.00 WHERE char_code = 'USD'
```
4. Delete (Удаление) — удаление валюты

Пользователь нажимает кнопку "Удалить" рядом с валютой.

SQL-запросы:

```sql
-- Сначала удаляем связанные подписки
DELETE FROM user_currency WHERE currency_id = 3
-- Затем удаляем саму валюту
DELETE FROM currency WHERE id = 3
```

* База данных подключена в режиме :memory::

```python
self.conn = sqlite3.connect(':memory:')
```
Это означает, что все данные хранятся в оперативной памяти и существуют только во время работы сервера. При каждом запуске БД инициализируется заново тестовыми данными и синхронизируется с API ЦБ РФ.

* ### Примеры работы приложения:

![alt text](<Снимок экрана 2026-06-13 в 13.11.36.png>)

![alt text](<Снимок экрана 2026-06-13 в 13.07.58.png>)

![alt text](<Снимок экрана 2026-06-12 в 22.09.42.png>)

![alt text](<Снимок экрана 2026-06-13 в 13.09.00.png>)

![alt text](<Снимок экрана 2026-06-12 в 22.11.14.png>)
* ### Результат прохождения тестов:

(venv) fedorcagin@MacBook-Pro13 ЛР-8 % python -m unittest discover tests -v
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
test_create_currency (test_database.TestDatabaseController.test_create_currency)
Тест добавления валюты. ... ok
test_delete_currency (test_database.TestDatabaseController.test_delete_currency)
Тест удаления валюты. ... ok
test_read_currencies (test_database.TestDatabaseController.test_read_currencies)
Тест чтения всех валют. ... ok
test_update_currency (test_database.TestDatabaseController.test_update_currency)
Тест обновления курса. ... ok
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
Ran 25 tests in 0.211s

OK
(venv) fedorcagin@MacBook-Pro13 ЛР-8 %

* ### Структура проекта 
```
myapp/
├── controllers/               # Контроллеры - обрабатывают запросы
│   ├── __init__.py           
│   ├── authorController.py   # Маршруты / и /author
│   ├── userController.py     # Маршруты /users и /user?id=
│   ├── currenciesController.py # Маршрут /currencies + CRUD
│   └── databaseController.py # Работа с SQLite (CRUD)
│
├── models/                    # Модели - данные и бизнес-логика
│   ├── __init__.py
│   ├── author.py             # Author: имя, группа
│   ├── app.py                # App: название, версия
│   ├── user.py               # User: id, имя
│   ├── currency.py           # Currency: код, курс, номинал
│   └── user_currency.py      # UserCurrency: подписки
│
├── templates/                 # HTML-шаблоны
│   ├── index.html            # Главная страница
│   ├── users.html            # Список пользователей
│   ├── user_detail.html      # Профиль пользователя с графиками
│   └── currencies.html       # Таблица валют с CRUD
│
├── static/
│   └── css/
│       └── style.css         # Стили оформления
│
├── utils/
│   ├── __init__.py
│   └── currencies_api.py     # get_currencies() - API ЦБ РФ
│
├── tests/                     # Модульные тесты
│   ├── test_models.py
│   ├── test_api.py
│   ├── test_controllers.py
│   └── test_database.py
│
└── myapp.py                   # Точка входа: сервер и маршрутизация
```

* ### Выводы

В ходе выполнения лабораторной работы было усовершенствовано клиент-серверное приложение для мониторинга курсов валют. 

**Реализованный функционал:**
- Просмотр актуальных курсов валют с сайта ЦБ РФ
- Управление подписками пользователей на валюты
- Полный CRUD для валют (создание, чтение, обновление, удаление)
- Графики динамики курсов за 3 месяца

**Технические результаты:**
- Работа с SQLite и параметризованными запросами для защиты от SQL-инъекций
- Применение первичных и внешних ключей в реляционной БД
- Организация CRUD операций через веб-интерфейс
- Тестирование с использованием unittest.mock
- Разделение контроллеров на бизнес-логику и работу с БД

Архитектура MVC соблюдена. Все тесты проходят успешно. Приложение работает стабильно.
