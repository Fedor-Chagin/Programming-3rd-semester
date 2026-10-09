import unittest #Импорт библиотеки
from task_1 import task_1  # Импорт функции

class TestTwoSum(unittest.TestCase): #создание набора проверок
    
    def test_example1(self): #создание теста с названием test_example1
        self.assertEqual(task_1([2, 7, 11, 15], 9), [0, 1]) #проверка результата
    
    def test_example2(self):
        self.assertEqual(task_1([3, 2, 4], 6), [1, 2])
    
    def test_example3(self):
        self.assertEqual(task_1([3, 3], 6), [0, 1])
    
    def test_no_solution(self):
        self.assertEqual(task_1([1, 2, 3], 10), [])

if __name__ == '__main__':
    unittest.main()