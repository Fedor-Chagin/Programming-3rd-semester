# SOLID

---
#### на примере системы отправки уведомлений клиентам через разные каналы: Email, SMS и Push-уведомления. Все каналы должны работать через единый интерфейс.

SOLID – пять принципов объектно-ориентированного проектирования, которые помогают делать код гибким, понятным и легко расширяемым:

S – Single Responsibility (принцип единственной ответственности)
O – Open/Closed (принцип открытости/закрытости)
L – Liskov Substitution (принцип подстановки Лисков)
I – Interface Segregation (принцип разделения интерфейсов)
D – Dependency Inversion (принцип инверсии зависимостей)

LSP – один из пяти принципов SOLID. Он говорит о правильном наследовании: наследник должен полностью заменять родителя без изменения логики программы.

## Пример нарушения LSP

```python
from abc import ABC, abstractmethod

class Notification(ABC):
    @abstractmethod
    def send(self, message: str, recipient: str) -> bool:
        pass
    
    @abstractmethod
    def schedule(self, message: str, recipient: str, delay_hours: int) -> bool:
        """Запланировать отправку с задержкой"""
        pass

class EmailNotification(Notification):
    def send(self, message: str, recipient: str) -> bool:
        print(f"Email to {recipient}: {message}")
        return True
    
    def schedule(self, message: str, recipient: str, delay_hours: int) -> bool:
        print(f"Email scheduled in {delay_hours}h")
        return True

class SMSNotification(Notification):
    def send(self, message: str, recipient: str) -> bool:
        if len(message) > 160:
            print("ERROR: SMS too long!")
            return False
        print(f"SMS to {recipient}: {message}")
        return True
    
    def schedule(self, message: str, recipient: str, delay_hours: int) -> bool:
        print(f"SMS scheduled in {delay_hours}h")
        return True

class PushNotification(Notification):
    def send(self, message: str, recipient: str) -> bool:
        print(f"Push to device {recipient}: {message}")
        return True
    
    def schedule(self, message: str, recipient: str, delay_hours: int) -> bool:
        # ПРОБЛЕМА: Push не поддерживает отложенную отправку!
        print("ERROR: Push doesn't support scheduling!")
        return False

def send_campaign(notifications: list[Notification], message: str):
    for notification in notifications:
        notification.schedule(message, "user@example.com", 2)  # Здесь падает Push
        notification.send(message, "user@example.com")
```

### почему это плохо

**Наследник (Push) не может выполнить контракт родителя (Notification).** Родитель требует метод `schedule()`, но Push не умеет планировать уведомления. При замене родителя на наследника программа ломается.

---

## Пример правильной соблюдения принципов SOLID (исправление LSP)

```python
from abc import ABC, abstractmethod

# Разделяем интерфейсы
class Sendable(ABC):
    @abstractmethod
    def send(self, message: str, recipient: str) -> bool:
        pass

class Schedulable(ABC):
    @abstractmethod
    def schedule(self, message: str, recipient: str, delay_hours: int) -> bool:
        pass

# Каждый класс реализует только то, что реально умеет
class EmailNotification(Sendable, Schedulable):
    def send(self, message: str, recipient: str) -> bool:
        print(f"Email to {recipient}: {message}")
        return True
    
    def schedule(self, message: str, recipient: str, delay_hours: int) -> bool:
        print(f"Email scheduled in {delay_hours}h")
        return True

class SMSNotification(Sendable, Schedulable):
    MAX_LENGTH = 160
    
    def send(self, message: str, recipient: str) -> bool:
        if len(message) > self.MAX_LENGTH:
            message = message[:self.MAX_LENGTH]  # Обрезаем, а не падаем
        print(f"SMS to {recipient}: {message}")
        return True
    
    def schedule(self, message: str, recipient: str, delay_hours: int) -> bool:
        print(f"SMS scheduled in {delay_hours}h")
        return True

class PushNotification(Sendable):  # НЕ реализует Schedulable
    def send(self, message: str, recipient: str) -> bool:
        print(f"Push to device {recipient}: {message}")
        return True

def send_campaign(sendables: list[Sendable], schedulables: list[Schedulable], message: str):
    # Планируем только те, кто это поддерживает
    for schedulable in schedulables:
        schedulable.schedule(message, "user@example.com", 2)
    
    # Отправляем всем
    for sendable in sendables:
        sendable.send(message, "user@example.com")
```

### почему это лучше:

**Классы реализуют только те интерфейсы, которые соответствуют их реальным возможностям.** Push не умеет планировать – он просто не реализует `Schedulable`. Клиентский код никогда не вызовет `schedule()` для Push, потому что работает с разными списками.

---

## Итог

Обе программы делают одно и то же – отправляют уведомления через Email, SMS и Push. Но первая реализация плохая, потому что:
- Наследник (Push) не может реализовать метод родителя (`schedule`)
- Это приводит к ошибкам во время выполнения
- Нарушен принцип LSP

Вторая реализация **правильная**, потому что:
- Интерфейсы разделены на `Sendable` и `Schedulable`
- Каждый класс реализует только то, что реально умеет
- Клиентский код безопасно работает с разными типами объектов
- Принцип LSP соблюдается

**Главный вывод:** Нельзя заставлять наследников реализовывать методы, которые они не могут выполнить. Если наследник не поддерживает какую-то операцию – значит, этой операции не должно быть в родительском интерфейсе (и наоборот).