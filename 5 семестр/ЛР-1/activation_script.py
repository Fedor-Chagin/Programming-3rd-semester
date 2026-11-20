import sys
import re
import requests
from importlib.abc import PathEntryFinder
from importlib.util import spec_from_loader

# 1. Загрузчик: скачивает код по URL и выполняет его
class URLLoader:
    def create_module(self, spec):
        return None  # тандартный механизм создания модуля

    def exec_module(self, module):
        # Скачиваем исходный код модуля по адресу origin
        response = requests.get(module.__spec__.origin) # строчка выполняет HTTP GET-запрос по адресу модуля, скачивает исходный код файла и сохраняет его в переменную response
        response.raise_for_status()  # Проверка на ошибки от сервера
        source_code = response.text
        
        code = compile(source_code, module.__spec__.origin, mode="exec") # содержит байт-код скачанного модуля myremotemodule.py (функцию myfoo()).Функция compile() принимает текст кода и возвращает объект байт-кода, который затем можно выполнить через exec(). Режим exec указывает, что код должен выполняться как скрипт (последовательность инструкций), а не как выражение.
        exec(code, module.__dict__)

# 2. Поиск спецификации: решает, может ли он загрузить запрошенный модуль
class URLFinder(PathEntryFinder):
    def __init__(self, url, available_modules):
        self.url = url # Запоминаем базовый адрес сервера (напр., "http://.../Python_programming")
        self.available = available_modules # Запоминаем список имён модулей, найденных на сервере

    def find_spec(self, fullname, target=None):
        if fullname in self.available: # Проверяем: запрошенное имя модуля есть в нашем списке? # Если да, склеиваем полный путь к файлу (базовый URL + имя + ".py")
            origin = f"{self.url}/{fullname}.py"
            loader = URLLoader() # Создаём экземпляр нашего загрузчика
            return spec_from_loader(fullname, loader, origin=origin) # Возвращаем Python'у готовую "инструкцию": что грузить, чем грузить и откуда
        return None # Если модуля нет в списке, говорим Python'у "я не нашел, ищи дальше"

# 3. Хук: перехватывает пути, начинающиеся с http:// или https://
def url_hook(path):
    if not path.startswith(("http://", "https://")): # Если путь не начинается с http, говорим "это не моя работа" и вызываем ошибку
        raise ImportError
    
    # Скачиваем HTML-страницу с содержимым директории (это делает python -m http.server)
    # Делаем HTTP-запрос к базовому URL, чтобы получить HTML-страницу со списком файлов
    response = requests.get(path)
    response.raise_for_status() # Проверяем, что страница успешно загрузилась
    html_content = response.text
    
    # Ищем имена .py файлов в HTML-коде (в атрибутах href="...")
    # С помощью регулярного выражения ищем в HTML все ссылки на файлы, заканчивающиеся на .py
    filenames = re.findall(r'href="([a-zA-Z_][a-zA-Z0-9_]*\.py)"', html_content)
    
    modnames = {name[:-3] for name in filenames} # Преобразуем имена файлов в имена модулей (отрезаем ".py")
    
    return URLFinder(path, modnames) # Создаем и возвращаем объект Поисковика, передавая ему URL и список найденных модулей

# 4. Регистрируем наш хук в системе импорта Python (добавляем нашу функцию-перехватчик в стандартный механизм импорта Python)
sys.path_hooks.append(url_hook) 

# Очищаем кэш импортеров, чтобы Python гарантированно проверил новые хуки
sys.path_importer_cache.clear()

print("✅ Механизм удаленного импорта активирован!")

sys.path.append("http://lr1.fedorchagin.ru/study/Python_programming") # Добавляем адрес нашего сервера в список мест, где Python будет искать модули
print("✅ Добавлен путь к внешнему серверу")

import myremotemodule
print("✅ Модуль успешно импортирован!")
myremotemodule.myfoo()
