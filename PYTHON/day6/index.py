# Part A 

def f(lst):
    lst.append(4)

a = [1, 2, 3]
f(a)
print(a)

# My prediction:
# [1, 2, 3, 4]

# Explanation:
# lst and a refer to the same list.append() mutates the original list.


def g(lst):
    lst = [9, 9]

b = [1, 2, 3]
g(b)
print(b)

# My prediction:
# [1, 2, 3]

# Reassigning lst creates a new list and only changes the local variable. The original b is unchanged.

count = 0

def inc():
    count += 1

# My prediction/reasoning:
# count is a global variable, but inside the function
# Python treats count as a local variable because
# count += 1 is an assignment.

# Error: UnboundLocalError

# Fix 1:
# Use the global keyword:
# def inc():
#     global count
#     count += 1

# Fix 2:
# Pass the value into the function and return the new value:

# def inc(count):
#     return count + 1

# count = inc(count)


def add(x, target=[]):
    target.append(x)
    return target

print(add(1))
print(add(2))

# My prediction:
# [1]
# [1, 2]

# Explanation:
# The default list [] is created only once when the function is defined. The same list is reused on every call.

# Correct approach:

# def add(x, target=None):
#     if target is None:
#         target = []
#     target.append(x)
#     return target

# With this approach:
# print(add(1)) -> [1]
# print(add(2)) -> [2]

# Key rule:
# Default arguments are evaluated once, not every call.