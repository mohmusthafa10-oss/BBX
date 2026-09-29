# Student Management System

A simple **CLI-based Student Management System** built with Python. It allows users to add, view, search, update, and delete student records, with data stored persistently in a JSON file.

## Features

* Add students with ID, name, and marks
* List all students
* Search students by ID
* Search students by name
* Update student details
* Delete students
* Calculate statistics:

  * Average marks
  * Highest marks
  * Lowest marks
  * Pass count
  * Fail count
* Validate names and marks
* Prevent duplicate student IDs
* Persist data using `data.json`
* Handle missing or invalid input without crashing

## Project Structure

```text
student_management/
│
├── main.py
├── models.py
├── operations.py
├── storage.py
├── data.json
├── README.md
└── .gitignore
```

### File Responsibilities

* **`main.py`** – Menu loop and all user input/output
* **`models.py`** – `Student` class and field validation
* **`operations.py`** – Add, search, update, delete, and statistics operations
* **`storage.py`** – Loading and saving data to `data.json`
* **`data.json`** – Stores student records

## How to Run

Make sure Python is installed.

Run the program from the project directory:

```bash
python main.py
```

On the first run, if `data.json` does not exist, the program starts with an empty student database.

## Usage Example

```text
Student Management System
1. Add student
2. List students
3. Search by ID
4. Search by name
5. Update student
6. Delete student
7. Statistics
8. Exit

Enter your choice: 1
Enter ID: S001
Enter name: Muhammed
Enter marks: 85

Student added successfully.
```

The student is saved to `data.json`, so the record remains available when the program is run again.

## Validation

* Student ID cannot be empty.
* Student IDs must be unique.
* Student name cannot be empty.
* Marks must be between `0` and `100`.
* Invalid input is handled using exceptions instead of crashing the program.
