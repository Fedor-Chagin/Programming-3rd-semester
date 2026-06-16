from abc import ABC, abstractmethod

# Разделяем ответственность на интерфейсы
class Sendable(ABC):
    @abstractmethod
    def send(self, message: str, recipient: str) -> bool:
        pass

class Schedulable(ABC):
    @abstractmethod
    def schedule(self, message: str, recipient: str, delay_hours: int) -> bool:
        pass

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
            message = message[:self.MAX_LENGTH]
        print(f"SMS to {recipient}: {message}")
        return True
    
    def schedule(self, message: str, recipient: str, delay_hours: int) -> bool:
        print(f"SMS scheduled in {delay_hours}h")
        return True

class PushNotification(Sendable):
    def send(self, message: str, recipient: str) -> bool:
        print(f"Push to {recipient}: {message}")
        return True

def send_campaign(sendables: list[Sendable], schedulables: list[Schedulable], message: str):
    """Отправляем кампанию: планируем, где можно, и отправляем всем"""
    
    for schedulable in schedulables:
        schedulable.schedule(message, "user@example.com", 2)
    
    for sendable in sendables:
        sendable.send(message, "user@example.com")