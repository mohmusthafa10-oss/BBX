# Written Answers

## 1. What does `if __name__ == "__main__"` do and why is it needed?

* `__name__` is a special Python variable that tells us how a module is being used.
* When a file is run directly, Python sets `__name__` to `"__main__"`.
* When the file is imported, `__name__` contains the module's name instead.
* Therefore, `if __name__ == "__main__":` ensures that the `main()` function runs **only when the file is executed directly**.
* It prevents execution code from running automatically when the module is imported.
* This makes the code easier to **reuse, test, and organize**.
* In our project, it allows `main.py` to work as the **entry point** without executing `main()` during imports.

---

## 2. How does Python decide where to find an imported module?

* When Python sees an import, it searches for the module in its **module search path** (`sys.path`).
* The search path includes the **current directory**, standard library locations, installed packages, and paths configured through `PYTHONPATH`.
* Python searches these locations in order until it finds the requested module.
* In our project, the package is inside the `src` directory.
* We used `PYTHONPATH=src` so Python knows that `src` is an import location.
* Therefore, this absolute import works:

  ```python
  from student_report.loader import load_students
  ```
* If Python cannot find the module anywhere in `sys.path`, it raises **`ModuleNotFoundError`**.
