class EvenNumbersIterator():
    
    def __init__(self, instance):
        self.instance = instance   
        self.idx = 0 # инициализируем индекс для перебора элементов
        
        
    def __iter__(self):
        return self # возвращает экземпляр класса, реализующего протокол итераторов
    
    
    def __next__(self): # возвращает следующий по порядку элемент итератора
        while True:
            try:
                res = self.instance[self.idx] # получаем очередной элемент из iterable
                
            except IndexError:
                raise StopIteration

            if res % 2 == 0: # проверяем на четность элемента
                self.idx += 1 # если четный, возвращаем значение и увеличиваем индекс
                return res

            self.idx += 1 # если нечетный, то просто увеличиваем индекс

    
list(EvenNumbersIterator(range(10))) # [0, 2, 4, 6, 8]

# result = list(EvenNumbersIterator(range(10)))
# print(result)