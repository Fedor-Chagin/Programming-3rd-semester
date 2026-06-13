"""Модель User - представляет пользователя."""

class User:
    """Класс для хранения информации о пользователе."""
    
    def __init__(self, user_id: int, name: str) -> None:
        """
        Инициализация пользователя.
        
        Args:
            user_id: Уникальный идентификатор
            name: Имя пользователя
        """
        self._id = user_id
        self._name = name
    
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def name(self) -> str:
        return self._name
    
    def to_dict(self) -> dict:
        """Преобразует объект в словарь для шаблонов."""
        return {'id': self._id, 'name': self._name}