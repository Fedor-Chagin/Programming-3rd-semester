ЛР-1
---
### Задание
```python
import sys
import re
import requests
from importlib.abc import PathEntryFinder
from importlib.util import spec_from_loader

class URLLoader:
    def create_module(self, spec):
        return None

    def exec_module(self, module):
        response = requests.get(module.__spec__.origin)
        response.raise_for_status()
        source_code = response.text
        
        code = compile(source_code, module.__spec__.origin, mode="exec")
        exec(code, module.__dict__)

class URLFinder(PathEntryFinder):
    def __init__(self, url, available_modules):
        self.url = url
        self.available = available_modules

    def find_spec(self, fullname, target=None):
        if fullname in self.available:
            origin = f"{self.url}/{fullname}.py"
            loader = URLLoader()
            return spec_from_loader(fullname, loader, origin=origin)
        return None

def url_hook(path):
    if not path.startswith(("http://", "https://")):
        raise ImportError
    
    response = requests.get(path)
    response.raise_for_status()
    html_content = response.text
    
    filenames = re.findall(r'href="([a-zA-Z_][a-zA-Z0-9_]*\.py)"', html_content)
    
    modnames = {name[:-3] for name in filenames}
    
    return URLFinder(path, modnames)

sys.path_hooks.append(url_hook)

sys.path_importer_cache.clear()

print("✅ Механизм удаленного импорта активирован!")

sys.path.append("http://lr1.fedorchagin.ru/study/Python_programming")
print("✅ Добавлен путь к внешнему серверу")

import myremotemodule
print("✅ Модуль успешно импортирован!")
myremotemodule.myfoo()
```
##### Результат

![alt text](<Снимок экрана 2026-10-01 в 23.37.57.png>)



---