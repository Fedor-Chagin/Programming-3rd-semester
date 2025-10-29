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