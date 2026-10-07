class Dog:
    tricks = []

    def __init__(self, name):
        self.name = name


a = Dog("Rex")
b = Dog("Bo")

a.tricks.append("roll")

print(b.tricks)

# tricks is a class attribute, so the same list is shared by every Dog instance. The fix is to create self.tricks = [] inside __init__, giving each instance its own list.