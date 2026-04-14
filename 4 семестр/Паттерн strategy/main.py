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
        # Таблица стратегий (как массив указателей в C)
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
    
    # Регистрируем стратегии (как заполнение массива в C)
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