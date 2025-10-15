
## ЛР-1

### Задание
0. Разработайте программу на языке Python, которая будет строить бинарное дерево (дерево, в каждом узле которого может быть только два потомка). Отображение результата в виде словаря (как базовый вариант решения задания). Далее исследовать другие структуры, в том числе доступные в модуле collections в качестве контейнеров для хранения структуры бинарного дерева. 

1. Код программы:

```py
import json # импорт модуля для работы с JSON
def gen_bin_tree(height=3, root=1, left_func=None, right_func=None): #создание функции gen_bin_tree, которая принимает высоту, корень дерева (по умолчанию будет 1)
    """Универсальная функция с поддержкой любых формул"""
    if height == 0: #Если высота дерева = 0, то ветки дальше не строятся
        return None #Возврат None в конце ветки, когда условие верно
    
    if left_func is None: #Если не дано другой формулы для левой функции, то использовать имеющуюся
        left_func = lambda x: x * 2
    if right_func is None: #Если не дано другой формулы для правой функции, то использовать имеющуюся
        right_func = lambda x: x * 3
    
    return { #Возврат узла дерева в виде словаря
        'value': root,
        'left': gen_bin_tree(height-1, left_func(root), left_func, right_func),
        'right': gen_bin_tree(height-1, right_func(root), left_func, right_func)
    }

# ПРИМЕР ДЛЯ №11:
if __name__ == "__main__":
    # Вариант 11: left = root^2, right = 2 + root^2
    tree = gen_bin_tree(
        height=3, 
        root=11,
        left_func=lambda x: x ** 2,      # x^2
        right_func=lambda x: 2 + x ** 2  # 2 + x^2
    )
    print(json.dumps(tree, indent=2)) #Вывод (преобразованного в JSON строку с нужными отступами) результата
```

2. Результат выполненной работы:  
```json
{
  "value": 11,
  "left": {
    "value": 121,
    "left": {
      "value": 14641,
      "left": null,
      "right": null
    },
    "right": {
      "value": 14643,
      "left": null,
      "right": null
    }
  },
  "right": {
    "value": 123,
    "left": {
      "value": 15129,
      "left": null,
      "right": null
    },
    "right": {
      "value": 15131,
      "left": null,
      "right": null
    }
  }
}

---
### Тест
0. Поставленная задача:  
Удостоверьтесь, что решение проходит тесты
1. Код программы:

```py
import unittest
from task_1 import gen_bin_tree #импорт функции gen_bin_tree из файла task_1

class test(unittest.TestCase): #создание набора проверок
    
    def test_basic(self): #тест с конкретными значениями
        """Базовый тест"""
        tree = gen_bin_tree(height=2, root=1) #вызов функции, создающей дерево (создание дерева с корнем 1 и высотой 2)
        self.assertEqual(tree['value'], 1) #проверка равенства
        self.assertEqual(tree['left']['value'], 2)
        self.assertEqual(tree['right']['value'], 3)
    
    def test_student_11(self):
        """Тест для №11"""
        tree = gen_bin_tree(height=2, root=11, 
                           left_func=lambda x: x**2, 
                           right_func=lambda x: 2 + x**2)
        self.assertEqual(tree['value'], 11)
        self.assertEqual(tree['left']['value'], 121)  # 11²
        self.assertEqual(tree['right']['value'], 123) # 2 + 11²
    
    def test_height_1(self):
        """Тест с высотой 1"""
        tree = gen_bin_tree(height=1, root=5)
        self.assertEqual(tree['value'], 5)
        self.assertIsNone(tree['left'])
        self.assertIsNone(tree['right'])
    
    def test_zero_height(self):
        """Тест с высотой 0"""
        self.assertIsNone(gen_bin_tree(height=0))

if __name__ == '__main__': #запуск тестов
    unittest.main()
```

2. Результат выполненной работы:  
....
----------------------------------------------------------------------
Ran 4 tests in 0.000s

OK

---