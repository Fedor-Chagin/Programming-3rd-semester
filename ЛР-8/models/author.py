"""Модель Author - представляет автора приложения."""

class Author:
    """Класс для хранения информации об авторе."""
    
    def __init__(self, name: str, group: str) -> None:
        """
        Инициализация автора.
        
        Args:
            name: Имя автора
            group: Учебная группа
        """
        self._name = name
        self._group = group
    
    @property
    def name(self) -> str:
        """Геттер для имени."""
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        """Сеттер для имени с проверкой."""
        if not value or not isinstance(value, str):
            raise ValueError("Имя не может быть пустым")
        self._name = value
    
    @property
    def group(self) -> str:
        """Геттер для группы."""
        return self._group
    
    @group.setter
    def group(self, value: str) -> None:
        """Сеттер для группы с проверкой."""
        if not value or not isinstance(value, str):
            raise ValueError("Группа не может быть пустой")
        self._group = value