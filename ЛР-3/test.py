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