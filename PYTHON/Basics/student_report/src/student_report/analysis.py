def clean_students(students):
    for student in students:
        student["score"] = int(student["score"])

    return students


def calculate_average(students):
    total = sum(student["score"] for student in students)
    return total / len(students)


def find_highest(students):
    return max(students, key=lambda student: student["score"])


def find_lowest(students):
    return min(students, key=lambda student: student["score"])


def count_passed(students, pass_mark=50):
    return sum(student["score"] >= pass_mark for student in students)