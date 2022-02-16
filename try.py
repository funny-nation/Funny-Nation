class Test:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(Test, cls).__new__(cls)
            cls.instance.i = 1
            cls.instance.j = 2
        return cls.instance



object1 = Test()
obj2 = Test()

print(object1 is obj2)

print(obj2.j)

obj2.j = 123
obj3 = Test()
print(obj3.j)
