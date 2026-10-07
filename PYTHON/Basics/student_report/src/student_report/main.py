from student_report.loader import load_students
from student_report.analysis import (
    clean_students,
    calculate_average,
    find_highest,
    find_lowest,
    count_passed,
)
from student_report.formatting import format_report


def main():
    students = load_students("students.csv")
    students = clean_students(students)

    average = calculate_average(students)
    highest = find_highest(students)
    lowest = find_lowest(students)
    passed = count_passed(students)

    report = format_report(
        students,
        average,
        highest,
        lowest,
        passed,
    )

    print(report)


if __name__ == "__main__":
    main()