# Student Management System — Defense Answers

## 1. Explain the project in one sentence

This is a CLI-based Student Management System built with Python that manages student records, validates data, stores it in JSON, and provides search and statistics features.

---

## 2. Explain the architecture and why you split it

I split the project into four modules so each file has one clear responsibility.

* **`main.py`** – Handles the menu, user input, and output.
* **`models.py`** – Contains the `Student` class and validates student data using `@property`.
* **`operations.py`** – Contains the business logic such as add, search, update, delete, and statistics.
* **`storage.py`** – Handles reading and writing `data.json`.

This separation makes the code easier to understand, test, maintain, and modify.

---

## 3. Why use a dictionary keyed by ID instead of a list?

I used a dictionary because the student ID is unique.

```python
students = {
    "S001": student_object,
    "S002": student_object
}
```

The main benefits are:

* Student IDs naturally become the **keys**.
* Duplicate IDs are easy to detect.
* Searching by ID is efficient because dictionary lookup is approximately **O(1)** on average.
* It is easier to update or delete a student using the ID.

With a list, I would have to iterate through the students to find a particular ID.

---

## 4. What was the hardest bug and how did you diagnose it?

One bug I faced was related to the `@property` implementation for the student ID.

I initially returned `self.id` from the `id` getter. Since `self.id` calls the getter again, it caused recursive calls.

I diagnosed it by looking at the traceback and understanding that the property was calling itself repeatedly.

I fixed it by using the internal attribute:

```python
@property
def id(self):
    return self._id
```

This also helped me understand the difference between a public property and the internal `_id` attribute.

---

## 5. What happens if `data.json` is corrupt?

The `load_data()` function uses exception handling for problems such as invalid JSON.

For example:

```python
except json.JSONDecodeError:
    return {}
```

It also handles malformed data using other relevant exceptions.

Instead of crashing, the application starts with an empty student dictionary.

In a real production system, I would also log the error and possibly create a backup or recovery mechanism instead of silently starting with empty data.

---

## 6. How would you handle 100,000 students?

For 100,000 students, I would move away from storing all data in a JSON file.

I would use a database such as **SQLite or PostgreSQL**.

The main reasons are:

* Better querying and indexing.
* Faster searches.
* Better handling of large datasets.
* Data integrity and transactions.
* Multiple operations can be performed without loading the entire dataset into memory.

I would also add an index on the student ID and use pagination when listing large numbers of students.

---

## 7. If you had another week, what specific technical change would you make?

I would replace the JSON storage layer with **SQLite** while keeping the existing `operations.py` interface as much as possible.

This would be a useful improvement because the current application is tightly connected to file-based persistence.

I would create a database table for students, add a primary key for the student ID, and update `storage.py` to perform database operations.

This would make the project more scalable while keeping the rest of the architecture mostly unchanged.
