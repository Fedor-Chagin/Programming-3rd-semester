
## ЛР-3

### Задание
0. Разработайте программу на языке Python, которая будет строить бинарное дерево (дерево, в каждом узле которого может быть только два потомка). Отображение результата в виде словаря (как базовый вариант решения задания). Далее исследовать другие структуры, в том числе доступные в модуле collections в качестве контейнеров для хранения структуры бинарного дерева. 

1. Код программы:

```py
import json

def gen_bin_tree(height=3, root=1, left_func=None, right_func=None):
    """
    Рекурсивно генерирует бинарное дерево в виде словаря.
    
    Для варианта 11 используются формулы: left = root², right = 2 + root²
    
    Args:
        height: Высота дерева
        root: Значение корневого узла
        left_func: Функция для левого потомка
        right_func: Функция для правого потомка
    
    Returns:
        Словарь, представляющий бинарное дерево
    
    Raises:
        ValueError: Если высота отрицательная
    """
    if height < 0:
        raise ValueError("Высота дерева не может быть отрицательной")
    
    if height == 0:
        return {'value': root, 'left': None, 'right': None}
    
    # Формулы по умолчанию для варианта 11
    if left_func is None:
        left_func = lambda x: x ** 2
    if right_func is None:
        right_func = lambda x: 2 + x ** 2
    
    return {
        'value': root,
        'left': gen_bin_tree(height-1, left_func(root), left_func, right_func),
        'right': gen_bin_tree(height-1, right_func(root), left_func, right_func)
    }
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
```
---
### Тест
0. Поставленная задача:  
Удостоверьтесь, что решение проходит тесты
1. Код программы:

```py
import unittest
from task_1 import gen_bin_tree

class test(unittest.TestCase):
    
    def test_basic(self):
        "Базовый тест с новыми формулами"
        tree = gen_bin_tree(height=2, root=1)
        self.assertEqual(tree['value'], 1)
        self.assertEqual(tree['left']['value'], 1)
        self.assertEqual(tree['right']['value'], 3)
    
    def test_student_11(self):
        """Тест для №11"""
        tree = gen_bin_tree(height=2, root=11)
        self.assertEqual(tree['value'], 11)
        self.assertEqual(tree['left']['value'], 121)
        self.assertEqual(tree['right']['value'], 123)
    
    def test_height_1(self):
        """Тест с высотой 1"""
        tree = gen_bin_tree(height=1, root=5)
        self.assertEqual(tree['value'], 5)
        self.assertEqual(tree['left']['value'], 25)
        self.assertEqual(tree['right']['value'], 27)
    
    def test_zero_height(self):
        """Тест с высотой 0"""
        tree = gen_bin_tree(height=0)
        self.assertEqual(tree, {'value': 1, 'left': None, 'right': None})

if __name__ == '__main__':
    unittest.main()
```

2. Результат выполненной работы:  
....
----------------------------------------------------------------------
Ran 4 tests in 0.000s

OK

---