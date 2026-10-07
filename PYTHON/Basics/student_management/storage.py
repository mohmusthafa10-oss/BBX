import json

from models import Student


FILE_NAME = "data.json"


def load_data():
    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            return {}

        students = {}

        for student_id, student_data in data.items():
            if not isinstance(student_data, dict):
                return {}

            students[student_id] = Student(
                student_id,
                student_data["name"],
                student_data["marks"]
            )

        return students

    except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError, ValueError):
        return {}

def save_data(students):
    data = {}

    for student_id, student in students.items():
        data[student_id] = {
            "name": student.name,
            "marks": student.marks
        }

    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)