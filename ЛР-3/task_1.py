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