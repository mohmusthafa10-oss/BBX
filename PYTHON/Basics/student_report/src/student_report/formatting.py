def format_report(students, average, highest, lowest, passed):
    return (
        "Student Report\n"
        + "-" * 30
        + "\n"
        + f"Total students: {len(students)}\n"
        + f"Average score: {average:.2f}\n"
        + f"Highest: {highest['name']} ({highest['score']})\n"
        + f"Lowest: {lowest['name']} ({lowest['score']})\n"
        + f"Passed: {passed}"
    )