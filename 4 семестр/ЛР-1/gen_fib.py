import functools

def fib_elem_gen():
    """Генератор, возвращающий элементы ряда Фибоначчи"""
    a = 0
    b = 1

    while True:
        yield a
        res = a + b
        a = b
        b = res

g = fib_elem_gen()

while True:
    el = next(g)
    print(el)
    if el > 10:
        break

def my_genn():
    """Сопрограмма"""
    while True:
        number_of_fib_elem = yield
        l = []
        fib_gen = fib_elem_gen()
        for _ in range(number_of_fib_elem):
            l.append(next(fib_gen))
        yield l

def fib_coroutine(g):
    @functools.wraps(g)
    def inner(*args, **kwargs):
        gen = g(*args, **kwargs)
        gen.send(None)
        return gen
    return inner


my_genn = fib_coroutine(my_genn)
gen = my_genn()
print(gen.send(5))