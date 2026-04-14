from enum import Enum
import pygame

# 1. Интерфейс стратегии
class EventHandler:
    def handle(self, event):
        pass

# 2. Конкретные стратегии (обработчики событий). Т.е. мы создаём класс MouseButtonDownHandler, который наследует EventHandler
class MouseButtonDownHandler(EventHandler): # Обработчик клика
    def handle(self, event): # В методе handle мы получаем объект event
        print(f"Клик мыши в ({event.pos[0]}, {event.pos[1]})") # event.pos это координаты мыши по x и y

class MouseWheelHandler(EventHandler): # Обработчик прокрутки колёсика мыши
    def handle(self, event):
        print(f"Колёсико: {event.y}") # event.y это направление прокрутки колёсика

class MouseMotionHandler(EventHandler): # Обработчик координат курсора
    def handle(self, event):
        print(f"Движение мыши в ({event.pos[0]}, {event.pos[1]})")

class MouseButtonUpHandler(EventHandler): # Обработчик отпускания мыши
    def handle(self, event):
        print(f"Отпускание кнопки в ({event.pos[0]}, {event.pos[1]})")

# 3. Контекст (диспетчер событий)
class EventDispatcher: 
    def __init__(self): # __init__ вызывается при создании объекта
        # Таблица стратегий
        self.handlers = {} # пустой словарь
    
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