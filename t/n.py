class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        return "B"

class C(B, A):
    pass

obj = C()
print(obj.method())