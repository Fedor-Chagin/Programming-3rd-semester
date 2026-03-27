from gen_fib import my_genn
def test_fib_1():
    gen = my_genn()
    assert gen.send(3) == [0, 1, 1]

def test_fib_2():
    gen = my_genn()
    assert gen.send(5) == [0, 1, 1, 2, 3]

def test_fib_3():
    gen = my_genn()
    assert gen.send(0) == []

def test_fib_4():
    gen = my_genn()
    assert gen.send(1) == [0]

def test_fib_5():
    gen = my_genn()
    assert gen.send(2) == [0, 1]

if __name__ == "__main__":
    test_fib_1()
    test_fib_2()
    test_fib_3()
    test_fib_4()
    test_fib_5()
    print("Все тесты пройдены")