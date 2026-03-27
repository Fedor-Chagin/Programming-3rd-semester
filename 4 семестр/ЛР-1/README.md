ЛР-1
---
##### Ссылка на задание
https://gist.github.com/nzhukov/1f7316912714cdb80e3e2ff2b346af96#file-even_numbers_iterator-py

#### Задача: 
изучить Итераторы и генераторы

---
### Задание 1
```python
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
```

##### Тесты

```python
from gen_fib import my_genn
def test_fib_1():
    gen = my_genn()
    assert gen.send(3) == [0, 1, 1]

def test_fib_2():
    gen = my_genn()
    assert gen.send(5) == [0, 1, 1, 2, 3]

def test_fib_3():
    gen = my_genn()
    assert gen.send(0) == []

def test_fib_4():
    gen = my_genn()
    assert gen.send(1) == [0]

def test_fib_5():
    gen = my_genn()
    assert gen.send(2) == [0, 1]

if __name__ == "__main__":
    test_fib_1()
    test_fib_2()
    test_fib_3()
    test_fib_4()
    test_fib_5()
    print("Все тесты пройдены")
```
##### Результат

```
MacBook-Pro13:ЛР-1 fedorcagin$ /Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -u "/Users/fedorcagin/Documents/Учёба/Программирование/4 семестр/ЛР-1/test_fib.py"
0
1
1
2
3
5
8
13
[0, 1, 1, 2, 3]
Все тесты пройдены
MacBook-Pro13:ЛР-1 fedorcagin$ 
```
---
### Задание 2
```python
class EvenNumbersIterator():
    
    def __init__(self, instance):
        self.instance = instance   
        self.idx = 0 # инициализируем индекс для перебора элементов
        
        
    def __iter__(self):
        return self # возвращает экземпляр класса, реализующего протокол итераторов
    
    
    def __next__(self): # возвращает следующий по порядку элемент итератора
        while True:
            try:
                res = self.instance[self.idx] # получаем очередной элемент из iterable
                
            except IndexError:
                raise StopIteration

            if res % 2 == 0: # проверяем на четность элемента
                self.idx += 1 # если четный, возвращаем значение и увеличиваем индекс
                return res

            self.idx += 1 # если нечетный, то просто увеличиваем индекс

    
list(EvenNumbersIterator(range(10))) # [0, 2, 4, 6, 8]

# result = list(EvenNumbersIterator(range(10)))
# print(result)
```
##### Тесты

```python
import unittest

class FibonacchiLst:
    def __init__(self, instance):
        self.instance = instance
        self.idx = 0
        
        max_val = max(instance) if instance else 0
        self.fib_set = set()
        a, b = 0, 1
        while a <= max_val:
            self.fib_set.add(a)
            a, b = b, a + b
    
    def __iter__(self):
        return self
    
    def __next__(self):
        while self.idx < len(self.instance):
            val = self.instance[self.idx]
            self.idx += 1
            if val in self.fib_set:
                return val
        raise StopIteration
    
class TestFibIterator(unittest.TestCase):

    def test_normal(self):
        result = list(FibonacchiLst(list(range(10))))
        self.assertEqual(result, [0, 1, 2, 3, 5, 8])

    def test_corner_0(self):
        result = list(FibonacchiLst(list(range(0))))
        self.assertEqual(result, [])

    def test_corner_1(self):
        result = list(FibonacchiLst(list(range(1))))
        self.assertEqual(result, [0])

    def test_corner_2(self):
        result = list(FibonacchiLst(list(range(2))))
        self.assertEqual(result, [0, 1])

    def test_corner_3(self):
        result = list(FibonacchiLst([1, 1]))
        self.assertEqual(result, [1, 1])

if __name__ == "__main__":
    unittest.main()
```
##### Результат
```
MacBook-Pro13:ЛР-1 fedorcagin$ /Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -u "/Users/fedorcagin/Documents/Учёба/Программирование/4 семестр/ЛР-1/test_fib_it.py"
.....
----------------------------------------------------------------------
Ran 5 tests in 0.000s

OK
MacBook-Pro13:ЛР-1 fedorcagin$ 
```




- **Генератор** – функция, которая может остановить своё выполнение с помощью слова yield и вернуть значение в этот момент. 
- **Сопрограмма** — генератор, который после использования yield может через строчку funct.send(5) продолжить выполнение функции (где funct это название функции которая была остановлена с помощью yield, а 5 это значение с которым функция продолжит работу)
- **Итераторы** – классы с методами __iter__() и __next__()
- **next()** – это встроенная функция Python, которая запускает или возобновляет работу генератора до следующего yield

---