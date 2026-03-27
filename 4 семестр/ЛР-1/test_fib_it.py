import unittest

class FibonacchiLst:
    def __init__(self, instance):
        self.instance = instance
        self.idx = 0
        
        max_val = max(instance) if instance else 0
        self.fib_set = set()
        a, b = 0, 1
        while a <= max_val:
            self.fib_set.add(a)
            a, b = b, a + b
    
    def __iter__(self):
        return self
    
    def __next__(self):
        while self.idx < len(self.instance):
            val = self.instance[self.idx]
            self.idx += 1
            if val in self.fib_set:
                return val
        raise StopIteration
    
class TestFibIterator(unittest.TestCase):

    def test_normal(self):
        result = list(FibonacchiLst(list(range(10))))
        self.assertEqual(result, [0, 1, 2, 3, 5, 8])

    def test_corner_0(self):
        result = list(FibonacchiLst(list(range(0))))
        self.assertEqual(result, [])

    def test_corner_1(self):
        result = list(FibonacchiLst(list(range(1))))
        self.assertEqual(result, [0])

    def test_corner_2(self):
        result = list(FibonacchiLst(list(range(2))))
        self.assertEqual(result, [0, 1])

    def test_corner_3(self):
        result = list(FibonacchiLst([1, 1]))
        self.assertEqual(result, [1, 1])

if __name__ == "__main__":
    unittest.main()
