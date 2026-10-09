import functools

def fact_recursive(n):
    """Вычисляет факториал числа n рекурсивным методом.
    Args:
        n (int): Неотрицательное целое число.
    Returns:
        int: Факториал числа n.
    Raises:
        RecursionError: Если n превышает максимальную глубину рекурсии.
    """
    return 1 if n <= 1 else n * fact_recursive(n - 1)


def fact_iterative(n):
    """Вычисляет факториал числа n итеративным методом.
    Args:
        n (int): Неотрицательное целое число.
    Returns:
        int: Факториал числа n.
    """
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


cache = {0: 1, 1: 1}

def fact_recursive_memo(n):
    """Вычисляет факториал числа n рекурсивным методом с мемоизацией.
    Использует глобальный словарь cache для хранения ранее вычисленных значений.
    Args:
        n (int): Неотрицательное целое число.
    Returns:
        int: Факториал числа n.
    """
    if n not in cache:
        cache[n] = n * fact_recursive_memo(n - 1)
    return cache[n]


@functools.lru_cache(maxsize=None)
def fact_iterative_memo(n):
    """Вычисляет факториал числа n итеративным методом с кешированием.
    Использует декоратор lru_cache для автоматического кеширования результатов.
    Args:
        n (int): Неотрицательное целое число.
    Returns:
        int: Факториал числа n.
    """
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result