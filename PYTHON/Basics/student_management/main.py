from models import Student
from storage import load_data, save_data
from operations import (
    add,
    list_students,
    search_by_id,
    search_by_name,
    update,
    delete,
    statistics,
)

def main():
    students = load_data()

    while True:
        print("\nStudent Management System")
        print("1. Add student")
        print("2. List students")
        print("3. Search by ID")
        print("4. Search by name")
        print("5. Update student")
        print("6. Delete student")
        print("7. Statistics")
        print("8. Exit")

        choice = input("Enter your choice: ").strip()

        # Add student
        if choice == "1":
            try:
                student_id = input("Enter ID: ").strip()
                name = input("Enter name: ").strip()
                marks = int(input("Enter marks: "))

                student = Student(student_id, name, marks)
                students = add(students, student)
                save_data(students)

                print("Student added successfully.")

            except ValueError as error:
                print(f"Error: {error}")

        # List students
        elif choice == "2":
            students_list = list_students(students)

            if not students_list:
              print("No students found.")
            else:
                for student in students_list:
                    print(student)

        # Search by ID
        elif choice == "3":
            student_id = input("Enter student ID: ").strip()
            student = search_by_id(students, student_id)

            if student:
                print(student)
            else:
                print("Student not found.")

        # Search by name
        elif choice == "4":
            name = input("Enter name: ").strip()
            results = search_by_name(students, name)

            if results:
                for student in results:
                    print(student)
            else:
                print("No students found.")

        # Update student
        elif choice == "5":
            try:
                student_id = input("Enter student ID: ").strip()
                name = input("Enter new name: ").strip()
                marks = int(input("Enter new marks: "))

                students = update(
                    students,
                    student_id,
                    name,
                    marks
                )
                save_data(students)

                print("Student updated successfully.")

            except (ValueError, KeyError) as error:
                print(f"Error: {error}")

        # Delete student
        elif choice == "6":
            try:
                student_id = input("Enter student ID: ").strip()

                students = delete(students, student_id)
                save_data(students)

                print("Student deleted successfully.")

            except KeyError as error:
                print(f"Error: {error}")

        # Statistics
        elif choice == "7":
            result = statistics(students)

            print(f"Average: {result['average']:.2f}")
            print(f"Highest: {result['highest']}")
            print(f"Lowest: {result['lowest']}")
            print(f"Pass: {result['pass']}")
            print(f"Fail: {result['fail']}")

        # Exit
        elif choice == "8":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1-8.")


if __name__ == "__main__":
    main()