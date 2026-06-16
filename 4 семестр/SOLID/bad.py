from abc import ABC, abstractmethod

class Notification(ABC):
    @abstractmethod
    def send(self, message: str, recipient: str) -> bool:
        """Отправить уведомление"""
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
        print(f"Email scheduled in {delay_hours}h to {recipient}")
        return True

class SMSNotification(Notification):
    def send(self, message: str, recipient: str) -> bool:
        # SMS имеет ограничение по длине
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
        # ПРОБЛЕМА: Push-уведомления НЕ поддерживают отложенную отправку!
        # Но метод есть в родительском классе
        print(f"ERROR: Push doesn't support scheduling!")
        return False

# Функция массовой рассылки
def send_campaign(notifications: list[Notification], message: str):
    """Отправить кампанию через разные каналы"""
    for notification in notifications:
        # ВСЁ ЛОМАЕТСЯ на Push-уведомлениях
        notification.schedule(message, "user@example.com", 2)
        notification.send(message, "user@example.com")