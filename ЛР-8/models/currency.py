"""Модель Currency - представляет валюту."""

class Currency:
    """Класс для хранения информации о валюте."""
    
    def __init__(self, currency_id: str, char_code: str, name: str, value: float, nominal: int) -> None:
        """
        Инициализация валюты.
        
        Args:
            currency_id: Уникальный ID валюты (из XML)
            char_code: Буквенный код (USD, EUR)
            name: Название валюты
            value: Курс к рублю
            nominal: Номинал
        """
        self._id = currency_id
        self._char_code = char_code
        self._name = name
        self._value = value
        self._nominal = nominal
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def char_code(self) -> str:
        return self._char_code
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def value(self) -> float:
        return self._value
    
    @property
    def nominal(self) -> int:
        return self._nominal
    
    def get_rate_per_unit(self) -> float:
        """Возвращает курс за 1 единицу валюты."""
        return self._value / self._nominal
    
    def to_dict(self) -> dict:
        """Преобразует объект в словарь."""
        return {
            'id': self._id,
            'char_code': self._char_code,
            'name': self._name,
            'value': self._value,
            'nominal': self._nominal,
            'rate_per_unit': self.get_rate_per_unit()
        }