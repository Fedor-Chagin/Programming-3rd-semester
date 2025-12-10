
## ЛР-3

### Задание
0. Разработайте программу на языке Python, которая будет строить бинарное дерево (дерево, в каждом узле которого может быть только два потомка). Отображение результата в виде словаря (как базовый вариант решения задания). Далее исследовать другие структуры, в том числе доступные в модуле collections в качестве контейнеров для хранения структуры бинарного дерева. 

1. Код программы:

```py
def gen_bin_tree(height=3, root=1, left_func=lambda x: x ** 2, right_func=lambda x: 2 + x ** 2):
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

class TestGenBinTree(unittest.TestCase):
    
    def test_basic(self):
        """Базовый тест с новыми формулами"""
        expected = {
            'value': 1,
            'left': {
                'value': 1,
                'left': {'value': 1, 'left': None, 'right': None},
                'right': {'value': 3, 'left': None, 'right': None}
            },
            'right': {
                'value': 3,
                'left': {'value': 9, 'left': None, 'right': None},
                'right': {'value': 11, 'left': None, 'right': None}
            }
        }
        self.assertEqual(gen_bin_tree(height=2, root=1), expected)
    
    def test_student_11(self):
        """Тест для №11"""
        expected = {
            'value': 11,
            'left': {
                'value': 121,
                'left': {'value': 14641, 'left': None, 'right': None},
                'right': {'value': 14643, 'left': None, 'right': None}
            },
            'right': {
                'value': 123,
                'left': {'value': 15129, 'left': None, 'right': None},
                'right': {'value': 15131, 'left': None, 'right': None}
            }
        }
        self.assertEqual(gen_bin_tree(height=2, root=11), expected)
    
    def test_height_1(self):
        """Тест с высотой 1"""
        expected = {
            'value': 5,
            'left': {'value': 25, 'left': None, 'right': None},
            'right': {'value': 27, 'left': None, 'right': None}
        }
        self.assertEqual(gen_bin_tree(height=1, root=5), expected)
    
    def test_zero_height(self):
        """Тест с высотой 0"""
        expected = {'value': 1, 'left': None, 'right': None}
        self.assertEqual(gen_bin_tree(height=0), expected)
    
    def test_negative_height(self):
        """Тест с отрицательной высотой"""
        with self.assertRaises(ValueError):
            gen_bin_tree(height=-1)
    
    def test_custom_functions(self):
        """Тест с кастомными функциями"""
        tree = gen_bin_tree(
            height=1, 
            root=2,
            left_func=lambda x: x * 2,
            right_func=lambda x: x * 3
        )
        expected = {
            'value': 2,
            'left': {'value': 4, 'left': None, 'right': None},
            'right': {'value': 6, 'left': None, 'right': None}
        }
        self.assertEqual(tree, expected)

if __name__ == '__main__':
    unittest.main()
```

2. Результат выполненной работы:  
....
----------------------------------------------------------------------
Ran 4 tests in 0.000s

OK

---