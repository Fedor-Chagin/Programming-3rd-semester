
ЛР-1
---
### Структура проекта
```
.
├── protos/
│   └── recommendations.proto
├── recommendations/
│   ├── Dockerfile
│   ├── recommendations.py
│   ├── requirements.txt
│   └── test_recommendations.py
└── marketplace/
    ├── Dockerfile
    ├── marketplace.py
    ├── requirements.txt
    └── test_marketplace_integration.py
```

### Код
```python
"""Marketplace: веб-приложение на FastAPI"""
import html
import os
from contextlib import asynccontextmanager
from typing import Annotated, Literal

import grpc
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from recommendations_pb2 import BookCategory, RecommendationRequest
from recommendations_pb2_grpc import RecommendationsStub

RECOMMENDATIONS_HOST = os.getenv("RECOMMENDATIONS_HOST", "localhost")
RECOMMENDATIONS_PORT = os.getenv("RECOMMENDATIONS_PORT", "50051")

CategoryName = Literal["mystery", "science_fiction", "self_help"]
CATEGORIES = {
    "mystery": BookCategory.BOOK_CATEGORY_MYSTERY,
    "science_fiction": BookCategory.BOOK_CATEGORY_SCIENCE_FICTION,
    "self_help": BookCategory.BOOK_CATEGORY_SELF_HELP,
}


class BookOut(BaseModel):
    id: int
    title: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    channel = grpc.aio.insecure_channel(f"{RECOMMENDATIONS_HOST}:{RECOMMENDATIONS_PORT}")
    app.state.recommendations = RecommendationsStub(channel)
    yield
    await channel.close()


app = FastAPI(title="Marketplace", version="1.0.0", lifespan=lifespan)


async def fetch_recommendations(
    stub: RecommendationsStub, user_id: int, category: CategoryName, max_results: int
) -> list[BookOut]:
    request = RecommendationRequest(
        user_id=user_id, category=CATEGORIES[category], max_results=max_results
    )
    try:
        response = await stub.Recommend(request, timeout=2.0)
    except grpc.aio.AioRpcError as error:
        if error.code() == grpc.StatusCode.INVALID_ARGUMENT:
            raise HTTPException(status_code=400, detail=error.details()) from error
        raise HTTPException(status_code=503, detail="Recommendations service is unavailable") from error
    return [BookOut(id=book.id, title=book.title) for book in response.recommendations]


@app.get("/api/v1/recommendations", tags=["recommendations"])
async def get_recommendations(
    request: Request,
    user_id: int,
    category: CategoryName = "mystery",
    max_results: Annotated[int, Query(ge=1, le=10)] = 3,
) -> list[BookOut]:
    """Рекомендации книг выбранной категории."""
    return await fetch_recommendations(
        request.app.state.recommendations, user_id, category, max_results
    )


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def homepage(request: Request) -> str:
    books = await fetch_recommendations(
        request.app.state.recommendations, user_id=1, category="mystery", max_results=3
    )
    items = "\n".join(f"      <li>{html.escape(book.title)}</li>" for book in books)
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Online Books For You</title>
  </head>
  <body>
    <h1>Mystery books you may like</h1>
    <ul>
{items}
    </ul>
  </body>
</html>
"""
```

![alt text](<ЛР-3 поднятие докера-1.png>)

![alt text](<ЛР-3 запросы-1.png>)

![alt text](<ЛР-3 тесты-1.png>)

![alt text](<ЛР-3 выключение контейнеров-1.png>)


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

## запуск

#### source venv/bin/activate
#### python activation_script.py
---