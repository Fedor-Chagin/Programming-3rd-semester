
## ЛР-4

### Задание
0. Напишите на языке Python нерекурсивную функцию gen_bin_tree, которая будет строить бинарное дерево.

Алгоритм построения дерева должен учитывать параметры height, root, left_leaf и right_leaf, переданные в качестве аргументов функции.

Если для указанных параметров были переданы значения, то используются они.
В противном случае должны использоваться значения, указанные в варианте.
Базовый вариант решения задачи должен представлять результат в виде словаря с ключами value, left, right.

Построенное дерево должно обладать следующими свойствами:

В корне дерева (root) находится число, которое задает пользователь.
Высота дерева (height) задается пользователем.
Левый (left) и правый потомок (right) вычисляется с использованием алгоритмов (left_leaf и right_leaf).
Алгоритмы по умолчанию нужно задать с использованием lambda-функций.

Далее - исследовать другие структуры, в том числе доступные в модуле collections в качестве контейнеров для хранения структуры бинарного дерева. 

1. Код программы:

```py
from typing import Callable, Dict, Any
from collections import deque


def gen_bin_tree(
    height: int = 3, 
    root: int = 11, 
    left_leaf: Callable[[int], int] = lambda x: x ** 2, 
    right_leaf: Callable[[int], int] = lambda x: 2 + x ** 2
) -> Dict[str, Any]:
    """
    Генерирует бинарное дерево в виде словаря используя итеративный подход.
    
    Args:
        height: Высота дерева (количество уровней). По умолчанию 3.
        root: Значение корневого узла. По умолчанию 11.
        left_leaf: Функция для левого потомка. По умолчанию lambda x: x**2.
        right_leaf: Функция для правого потомка. По умолчанию lambda x: 2 + x**2.
    
    Returns:
        Словарь, представляющий бинарное дерево.
    
    Raises:
        ValueError: Если высота отрицательная.
    """
    if height < 0:
        raise ValueError("Высота дерева не может быть отрицательной")
    
    if height == 0:
        return {'value': root, 'left': None, 'right': None}
    
    root_node = {'value': root, 'left': None, 'right': None}
    
    queue = deque([(root_node, 1)])
    
    while queue:
        current_node, current_depth = queue.popleft()
        
        if current_depth < height:
            # Левый потомок
            left_value = left_leaf(current_node['value'])
            left_node = {'value': left_value, 'left': None, 'right': None}
            current_node['left'] = left_node
            queue.append((left_node, current_depth + 1))
            
            #Правый потомок
            right_value = right_leaf(current_node['value'])
            right_node = {'value': right_value, 'left': None, 'right': None}
            current_node['right'] = right_node
            queue.append((right_node, current_depth + 1))
    
    return root_node
```
---
### Тест
0. Поставленная задача:  
Напишите тесты с помощью unittest и удостоверьтесь, что ваше решение их проходит. 
1. Код программы:

```py
import unittest
from task_1 import gen_bin_tree

class TestBinTree(unittest.TestCase):
    
    def test_default(self):
        """Тест с параметрами по умолчанию из задания"""
        tree = gen_bin_tree()
        self.assertEqual(tree['value'], 11)
        self.assertEqual(tree['left']['value'], 121)  # 11^2
        self.assertEqual(tree['right']['value'], 123) # 2 + 11^2
    
    def test_custom_root_height(self):
        """Пользовательские root и height"""
        tree = gen_bin_tree(height=2, root=5)
        self.assertEqual(tree['value'], 5)
        self.assertEqual(tree['left']['value'], 25)  # 5^2
        self.assertEqual(tree['right']['value'], 27) # 2 + 5^2
    
    def test_height_zero(self):
        """height=0: только корень"""
        tree = gen_bin_tree(height=0, root=11)
        self.assertEqual(tree['value'], 11)
        self.assertIsNone(tree['left'])
        self.assertIsNone(tree['right'])
    
    def test_negative_height(self):
        """Отрицательная высота → ошибка"""
        with self.assertRaises(ValueError):
            gen_bin_tree(height=-1)

if __name__ == '__main__':
    unittest.main()
```

2. Результат выполненной работы:  
....
----------------------------------------------------------------------
Ran 4 tests in 0.000s

OK

---