
## ЛР-1

### Задание
0. Поставленная задача:  
Дан массив целых чисел nums и целочисленное значение переменной target , верните индексы двух чисел таким образом, чтобы они в сумме давали target. У каждого входного набора может не быть решений и может быть только одно решение, если есть элементы дающие в сумме target. Вы не можете  использовать один и тот же элемент дважды (и соответственно индекс тоже). Вы можете вернуть ответ в любом порядке нахождения индексов.

1. Код программы:

```py
def task_1(nums, target): #создание функции task_1
    for i in range(len(nums)): #перебор индексов с помощью циклов
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return [] # возврат пустого списка

if __name__ == "__main__": #Проверка, как выполняется программа (из теста или вручную)
    # Чтение входных данных
    nums = list(map(int, input().split())) #преобразование ввода в список чисел и их сохранение в переменную nums
    target = int(input())
    
    result = task_1(nums, target) #вызов функции task_1 и сохранение её вывода в result
    
    # Вывод результата
    if result: # если список result не пустой
        print(result[0], result[1])
    else:
        print("Решение не найдено")
```

2. Результат выполненной работы:  
1 2 3 6 7 8 3 4 7 3 2 12 4 8
5
0 7  

---
### Тест
0. Поставленная задача:  
Удостоверьтесь, что решение проходит следующие тесты: 

Example 1:

Input: nums = [2,7,11,15], target = 9

Output: [0,1]

Example 2:

Input: nums = [3,2,4], target = 6

Output: [1,2]

Example 3:

Input: nums = [3,3], target = 6

Output: [0,1]

1. Код программы:

```py
import unittest #Импорт библиотеки
from task_1 import task_1  # Импорт функции

class TestTwoSum(unittest.TestCase): #создание набора проверок
    
    def test_example1(self): #создание теста с названием test_example1
        self.assertEqual(task_1([2, 7, 11, 15], 9), [0, 1]) #проверка результата
    
    def test_example2(self):
        self.assertEqual(task_1([3, 2, 4], 6), [1, 2])
    
    def test_example3(self):
        self.assertEqual(task_1([3, 3], 6), [0, 1])
    
    def test_no_solution(self):
        self.assertEqual(task_1([1, 2, 3], 10), [])

if __name__ == '__main__':
    unittest.main()
```

2. Результат выполненной работы:  
....
----------------------------------------------------------------------
Ran 4 tests in 0.000s

OK

---