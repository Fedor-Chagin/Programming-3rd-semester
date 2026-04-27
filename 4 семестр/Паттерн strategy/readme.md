# Паттерн "Стратегия"

## Типы паттернов

| Тип | Назначение |
|-----|-----------|
| **Порождающие** | Как создавать объекты |
| **Структурные** | Как строить связи между объектами |
| **Поведенческие** | Как распределить обязанности и алгоритмы |

**→ Паттерн "Стратегия" относится к ПОВЕДЕНЧЕСКИМ**

---

## Суть паттерна "Стратегия" (простыми словами)

> **Стратегия** – выносим алгоритмы в отдельные классы/функции, а основной код просто хранит ссылку на один из них и делегирует работу.

**Ключевая особенность:** Стратегию можно менять на лету, даже во время выполнения программы.

**Главное отличие от if/else:** Выбор алгоритма происходит ЗА ПРЕДЕЛАМИ основного кода, а не внутри него через условия.

---

## Без паттерна

```python
# Без паттерна
class PaymentProcessor:
    def pay_card(self, amount):
        print(f"Оплата картой: {amount} руб")
    
    def pay_paypal(self, amount):
        print(f"Оплата PayPal: {amount} руб")
    
    def pay_crypto(self, amount):
        print(f"Оплата криптой: {amount} руб")
    
    def pay(self, method, amount):  # ❌ метод меняется при добавлении новых способов
        if method == "card":
            self.pay_card(amount)
        elif method == "paypal":
            self.pay_paypal(amount)
        elif method == "crypto":  # ❌ пришлось добавлять новую ветку
            self.pay_crypto(amount)
        else:
            print("Неизвестный метод")

# Использование
processor = PaymentProcessor()
processor.pay("card", 1000)     # Оплата картой: 1000 руб
processor.pay("paypal", 500)    # Оплата PayPal: 500 руб
processor.pay("crypto", 2000)   # Оплата криптой: 2000 руб
```

**Проблема:** При добавлении нового способа оплаты приходится менять код класса.

---

## С паттерном "Стратегия"

```python
# С паттерном 
# 1. Интерфейс стратегии (не обязателен в Python)
class PaymentStrategy:
    def pay(self, amount):
        pass

# 2. Конкретные стратегии
class CardPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Оплата картой: {amount} руб")

class PayPalPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Оплата PayPal: {amount} руб")

# ✅ Добавляем новую стратегию БЕЗ изменения существующего кода
class CryptoPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Оплата криптой: {amount} руб")

# 3. Контекст (НЕ МЕНЯЕТСЯ НИКОГДА)
class PaymentProcessor:
    def __init__(self, strategy: PaymentStrategy):
        self.strategy = strategy
    
    def pay(self, amount):
        self.strategy.pay(amount)  # просто делегирование
    
    # ✅ Можно менять стратегию на лету
    def set_strategy(self, strategy: PaymentStrategy):
        self.strategy = strategy

# Использование
processor = PaymentProcessor(CardPayment())  # передаём стратегию в конструктор
processor.pay(1000)   # Оплата картой: 1000 руб

# Меняем стратегию
processor.set_strategy(PayPalPayment())
processor.pay(500)    # Оплата PayPal: 500 руб

# ✅ Используем новую стратегию без изменения PaymentProcessor
processor.set_strategy(CryptoPayment())
processor.pay(2000)   # Оплата криптой: 2000 руб
```

---

## UML-схема паттерна "Стратегия"

## Реалистичный пример – обработка событий мыши (Python + pygame)

```python
from enum import Enum
import pygame

# 1. Интерфейс стратегии
class EventHandler:
    def handle(self, event):
        pass

# 2. Конкретные стратегии
class MouseButtonDownHandler(EventHandler):
    def handle(self, event):
        print(f"Клик мыши в ({event.pos[0]}, {event.pos[1]})")

class MouseWheelHandler(EventHandler):
    def handle(self, event):
        print(f"Колёсико: {event.y}")

class MouseMotionHandler(EventHandler):
    def handle(self, event):
        print(f"Движение мыши в ({event.pos[0]}, {event.pos[1]})")

class MouseButtonUpHandler(EventHandler):
    def handle(self, event):
        print(f"Отпускание кнопки в ({event.pos[0]}, {event.pos[1]})")

# 3. Контекст
class EventDispatcher: 
    def __init__(self): 
        # Таблица стратегий
        self.handlers = {}
    
    def register(self, event_type, handler):
        self.handlers[event_type] = handler
    
    def dispatch(self, event):
        handler = self.handlers.get(event.type)
        if handler:
            handler.handle(event)

# 4. Использование
def main():
    pygame.init()
    screen = pygame.display.set_mode((480, 480))
    
    # Создаём диспетчер
    dispatcher = EventDispatcher()
    
    dispatcher.register(pygame.MOUSEBUTTONDOWN, MouseButtonDownHandler())
    dispatcher.register(pygame.MOUSEBUTTONUP, MouseButtonUpHandler())
    dispatcher.register(pygame.MOUSEMOTION, MouseMotionHandler())
    dispatcher.register(pygame.MOUSEWHEEL, MouseWheelHandler())
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Диспетчер сам выбирает стратегию по типу события
            dispatcher.dispatch(event)
    
    pygame.quit()

if __name__ == "__main__":
    main()
```

---

## Пример реализации того же кода на C

```c
#include <stdio.h>
#include <SDL3/SDL.h>

typedef void (*EventHandler)(SDL_Event*);

void handle_mousebuttondown(SDL_Event* event) {
    printf("Клик мыши в (%f, %f)\n", event->button.x, event->button.y);
}

void handle_mousebuttonup(SDL_Event* event) {
    printf("Отпускание кнопки в (%f, %f)\n", event->button.x, event->button.y);
}

void handle_mousewheel(SDL_Event* event) {
    const char* direction = (event->wheel.y > 0) ? "вверх" : "вниз";
    printf("Колёсико %s\n", direction);
}

void handle_mousemotion(SDL_Event* event) {
    printf("Движение мыши в (%f, %f)\n", event->motion.x, event->motion.y);
}

static EventHandler event_handlers[SDL_EVENT_LAST] = {
    [SDL_EVENT_MOUSE_BUTTON_DOWN] = handle_mousebuttondown,
    [SDL_EVENT_MOUSE_BUTTON_UP]   = handle_mousebuttonup,
    [SDL_EVENT_MOUSE_WHEEL]       = handle_mousewheel,
    [SDL_EVENT_MOUSE_MOTION]      = handle_mousemotion
};

void dispatch_event(SDL_Event* event) {
    if (event->type >= 0 && event->type < SDL_EVENT_LAST && event_handlers[event->type]) {
        event_handlers[event->type](event);
    }
}

int main() {
    SDL_Init(SDL_INIT_VIDEO);
    
    SDL_Window* window = SDL_CreateWindow("Strategy in C", 480, 480, SDL_WINDOW_RESIZABLE);
    SDL_Renderer* renderer = SDL_CreateRenderer(window, NULL);
    
    int running = 1;
    while (running) {
        SDL_Event event;
        
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_EVENT_QUIT) {
                running = 0;
            }
            if (event.type == SDL_EVENT_KEY_DOWN && event.key.key == SDLK_ESCAPE) {
                running = 0;
            }
            
            dispatch_event(&event);
        }
        
        SDL_SetRenderDrawColor(renderer, 30, 30, 40, 255);
        SDL_RenderClear(renderer);
        SDL_RenderPresent(renderer);
        
        SDL_Delay(16);
    }
    
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    
    return 0;
}
```

**Суть:** Диспетчер не знает, что делают обработчики. Он просто находит нужный и делегирует.

---

## UML-схема для примера с обработкой событий

![UML-схема паттерна Стратегия](https://volosoft.com/api/blogging/files/www/43f86cd30a55a515430739f4f23b2a99.png)

---

## Важное уточнение

> **Это не чистый паттерн "Стратегия", а его вариация**

| Чистая Стратегия | Данный пример (диспетчер событий) |
|------------------|-----------------------------------|
| Стратегию можно менять на лету | Стратегия привязана к типу события НАВСЕГДА |
| Стратегия передаётся извне (в конструктор или setter) | Стратегия выбирается автоматически по типу события |
| Контекст не знает, какая стратегия используется | Диспетчер знает все стратегии заранее |

**Однако механизм инкапсуляции алгоритмов в отдельные функции и делегирования остаётся тем же.**

---

## Плюсы и минусы паттерна "Стратегия"

| Плюсы | Минусы |
|-----------|------------|
| Уход от огромных условных операторов | Классов становится больше |
| Код открыт для расширения, закрыт для изменения | Для простых задач (1-2 варианта) паттерн избыточен |
| Алгоритмы легко заменять и переиспользовать | Усложнение структуры программы |
| Легко тестировать каждую стратегию отдельно | |

---

## Где применяется паттерн "Стратегия"
| | |
|---------|---------|
| **Платёжные системы** | Карта, PayPal, Криптовалюта |
| **Сжатие данных** | ZIP, RAR, 7z |
| **Маршрутизация** | построение пути путь |
| **Игры** | Разные стратегии ИИ противника |
| **Обработка событий** | Диспетчеры событий (как в примере) |

---

## Итог

> **Стратегия** – определяет семейство алгоритмов, инкапсулирует каждый из них и делает их взаимозаменяемыми.

**Главная идея:** вынести различные алгоритмы в отдельные классы или функции и передавать их в основной код, чтобы можно было менять поведение программы без изменения самого кода.

```
Context ── содержит ссылку ──▶ Strategy (интерфейс)
                                    △
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
              Concrete          Concrete        Concrete
              Strategy A        Strategy B      Strategy C
```
