import csv


def load_students(filename):
    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        students = list(reader)

    return students