A class attribute belongs to the class and is shared by all instances created from that class. It is useful for data that is common to every object, such as a class-wide configuration or a constant. An instance attribute belongs to a specific object and is usually defined using self inside __init__. Each instance has its own copy and can have a different value. For example, Student.school could be a class attribute shared by all students, while student.name is an instance attribute because each student can have a different name.

I would choose composition when one class needs to use or contain an object of another class, representing a has-a relationship, rather than an is-a relationship. Composition keeps classes more independent and allows behavior to be combined without creating a rigid inheritance hierarchy. For example, a Car has an Engine, so Car can contain an Engine object instead of inheriting from Engine.

__init__ is technically an initializer, not the constructor. Python uses __new__() to create the object, and then __init__() initializes that already-created object with the required attributes.

MRO (Method Resolution Order) is the order Python follows when searching for methods and attributes in an inheritance hierarchy. Python calculates this order using C3 Linearization, which maintains a consistent ordering, respects the declared parent order, and avoids inconsistent inheritance paths. super() follows this MRO rather than simply calling the immediate parent.

<!-- Part D -->

class A:
    pass


class B(A):
    pass


class C(A):
    pass


class D(B, C):
    pass

print(D.__mro__)
<!-- (<class '__main__.D'>,
 <class '__main__.B'>,
 <class '__main__.C'>,
 <class '__main__.A'>,
 <class 'object'>) -->

 MRO is: D → B → C → A → object