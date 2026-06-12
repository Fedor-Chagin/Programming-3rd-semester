"""Модель App - представляет приложение."""

from models.author import Author

class App:
    """Класс для хранения информации о приложении."""
    
    def __init__(self, name: str, version: str, author: Author) -> None:
        """
        Инициализация приложения.
        
        Args:
            name: Название приложения
            version: Версия
            author: Объект Author
        """
        self._name = name
        self._version = version
        self._author = author
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def version(self) -> str:
        return self._version
    
    @property
    def author(self) -> Author:
        return self._author