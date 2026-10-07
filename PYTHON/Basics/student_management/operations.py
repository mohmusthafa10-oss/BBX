from models import Student


PASS_MARK = 40


def add(students, student):
    """Add a student if the ID is unique."""
    if student.id in students:
        raise ValueError(f"Student ID '{student.id}' already exists.")

    updated_students = students.copy()
    updated_students[student.id] = student
    return updated_students


def search_by_id(students, student_id):
    """Find a student by ID."""
    return students.get(student_id)


def search_by_name(students, name):
    """Find students whose names match the search text."""
    search_name = name.strip().lower()

    return [
        student
        for student in students.values()
        if search_name in student.name.lower()
    ]


def update(students, student_id, name=None, marks=None):
    """Update an existing student's name and/or marks."""
    if student_id not in students:
        raise KeyError(f"Student ID '{student_id}' not found.")

    old_student = students[student_id]

    updated_name = old_student.name if name is None else name
    updated_marks = old_student.marks if marks is None else marks

    updated_student = Student(
        student_id,
        updated_name,
        updated_marks
    )

    updated_students = students.copy()
    updated_students[student_id] = updated_student

    return updated_students


def delete(students, student_id):
    """Delete a student by ID."""
    if student_id not in students:
        raise KeyError(f"Student ID '{student_id}' not found.")

    updated_students = students.copy()
    del updated_students[student_id]

    return updated_students


def statistics(students):
    """Return statistics about student marks."""
    if not students:
        return {
            "average": 0,
            "highest": 0,
            "lowest": 0,
            "pass": 0,
            "fail": 0,
        }

    marks = [student.marks for student in students.values()]

    passed = sum(mark >= PASS_MARK for mark in marks)
    failed = len(marks) - passed

    return {
        "average": sum(marks) / len(marks),
        "highest": max(marks),
        "lowest": min(marks),
        "pass": passed,
        "fail": failed,
    }

def list_students(students):
    """Return all students."""
    return list(students.values())