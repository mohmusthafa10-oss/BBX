class Student:

    def __init__(self,id,name,marks):
        self.id=id
        self.name=name
        self.marks=marks

    @property
    def marks(self):
       return self._marks

    @marks.setter
    def marks(self, value):
        if value < 0 or value > 100:
            raise ValueError("Marks must be between 0 and 100")
        self._marks = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value.strip():
            raise ValueError("Enter a valid name")
        self._name = value.strip()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not value.strip():
            raise TypeError("Enter a valid ID")
        self._id = value.strip()

    def __str__(self):
     return f"{self._id} - {self._name} - {self._marks}"

    def __repr__(self):
        return f"Student(id = '{self._id}' , name = '{self._name}' , marks = '{self._marks}')"