from student_report.analysis import (
    calculate_average,
    find_highest,
    count_passed,
)

def test_calculate_average():
    students = [
        {"name": "Alice", "score": 80},
        {"name": "Bob", "score": 60},
    ]

    assert calculate_average(students) == 70

def test_find_highest():
    students = [
        {"name": "Alice", "score": 80},
        {"name": "Bob", "score": 95},
        {"name": "Charlie", "score": 70},
    ]

    result = find_highest(students)

    assert result["name"] == "Bob"
    assert result["score"] == 95

def test_count_passed():
    students = [
        {"name": "Alice", "score": 80},
        {"name": "Bob", "score": 45},
        {"name": "Charlie", "score": 50},
        {"name": "David", "score": 30},
    ]

    assert count_passed(students) == 2