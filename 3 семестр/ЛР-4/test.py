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