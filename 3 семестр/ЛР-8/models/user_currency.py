"""Модель UserCurrency - связь пользователя с валютой (подписка)."""

class UserCurrency:
    """Класс для хранения подписок пользователей на валюты."""
    
    def __init__(self, subscription_id: int, user_id: int, currency_id: str) -> None:
        """
        Инициализация подписки.
        
        Args:
            subscription_id: Уникальный идентификатор подписки
            user_id: ID пользователя
            currency_id: ID валюты
        """
        self._id = subscription_id
        self._user_id = user_id
        self._currency_id = currency_id
    
    @property
    def id(self) -> int:
        """Get subscription ID."""
        return self._id
    
    @property
    def user_id(self) -> int:
        """Get user ID."""
        return self._user_id
    
    @property
    def currency_id(self) -> str:
        """Get currency ID."""
        return self._currency_id
