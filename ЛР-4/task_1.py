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