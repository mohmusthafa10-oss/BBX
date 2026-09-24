* **Strings are immutable:** In Python, once a string is created, its contents cannot be changed directly.

* **What happens when we modify a string:** If we write something like `result = result + text`, Python creates a **new string** instead of changing the existing one.

* **Why this matters in loops:** When string concatenation is repeated inside a loop, Python may repeatedly create new strings and copy the old contents into them.

* **Performance problem:** As the string becomes larger, more characters need to be copied each time. This can make repeated concatenation **slow and inefficient**, especially with large strings or many iterations.

* **Better approach:** We can store the individual pieces in a **list** and combine them at the end using `join()`. This avoids repeatedly creating larger strings and is generally more efficient.
