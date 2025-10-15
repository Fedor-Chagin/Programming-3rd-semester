import json 
def gen_bin_tree(height=3, root=1, left_func=None, right_func=None): 
    """Универсальная функция с поддержкой любых формул"""
    if height == 0: 
        return None 
    
    if left_func is None: 
        left_func = lambda x: x * 2
    if right_func is None: 
        right_func = lambda x: x * 3
    
    return { #Возврат узла дерева в виде словаря
        'value': root,
        'left': gen_bin_tree(height-1, left_func(root), left_func, right_func),
        'right': gen_bin_tree(height-1, right_func(root), left_func, right_func)
    }

# ПРИМЕР ДЛЯ №11:
if __name__ == "__main__":

    tree = gen_bin_tree(
        height=3, 
        root=11,
        left_func=lambda x: x ** 2,
        right_func=lambda x: 2 + x ** 2 
    )
    print(json.dumps(tree, indent=2)) 