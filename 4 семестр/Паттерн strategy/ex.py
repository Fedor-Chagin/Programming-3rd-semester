# Без паттерна
class PaymentProcessor:
    def pay_card(self, amount):
        print(f"Оплата картой: {amount} руб")
    
    def pay_paypal(self, amount):
        print(f"Оплата PayPal: {amount} руб")
    
    def pay_crypto(self, amount):
        print(f"Оплата криптой: {amount} руб")
    
    def pay(self, method, amount):  # ❌ метод меняется при добавлении новых способов
        if method == "card":
            self.pay_card(amount)
        elif method == "paypal":
            self.pay_paypal(amount)
        elif method == "crypto":  # ❌ пришлось добавлять новую ветку
            self.pay_crypto(amount)
        else:
            print("Неизвестный метод")

# Использование
processor = PaymentProcessor()
processor.pay("card", 1000)     # Оплата картой: 1000 руб
processor.pay("paypal", 500)    # Оплата PayPal: 500 руб
processor.pay("crypto", 2000)   # Оплата криптой: 2000 руб


# С паттерном 
# 1. Интерфейс стратегии (не обязателен в Python)
class PaymentStrategy:
    def pay(self, amount):
        pass

# 2. Конкретные стратегии
class CardPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Оплата картой: {amount} руб")

class PayPalPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Оплата PayPal: {amount} руб")

# ✅ Добавляем новую стратегию БЕЗ изменения существующего кода
class CryptoPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Оплата криптой: {amount} руб")

# 3. Контекст (НЕ МЕНЯЕТСЯ НИКОГДА)
class PaymentProcessor:
    def __init__(self, strategy: PaymentStrategy):
        self.strategy = strategy
    
    def pay(self, amount):
        self.strategy.pay(amount)  # просто делегирование
    
    # ✅ Можно менять стратегию на лету
    def set_strategy(self, strategy: PaymentStrategy):
        self.strategy = strategy

# Использование
processor = PaymentProcessor(CardPayment())  # передаём стратегию в конструктор
processor.pay(1000)   # Оплата картой: 1000 руб

# Меняем стратегию
processor.set_strategy(PayPalPayment())
processor.pay(500)    # Оплата PayPal: 500 руб

# ✅ Используем новую стратегию без изменения PaymentProcessor
processor.set_strategy(CryptoPayment())
processor.pay(2000)   # Оплата криптой: 2000 руб