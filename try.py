class Test:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(Test, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.i = 1
        self.j = 2


object1 = Test()
obj2 = Test()

print(object1 is obj2)

print(obj2.j)

obj2.j = 123
print(object1.j)
