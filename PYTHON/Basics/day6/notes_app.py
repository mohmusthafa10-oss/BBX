from datetime import datetime


def add_note(note):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("notes.txt", "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {note}\n")


def read_notes():
    try:
        with open("notes.txt", "r", encoding="utf-8") as file:
            for line in file:
                print(line, end="")

    except FileNotFoundError:
        print("No notes found.")


def main():
    note = input("Enter a note: ")
    add_note(note)

    print("\nYour notes:")
    read_notes()


if __name__ == "__main__":
    main()