import copy
import time


# Part A - Predict and Verify

a = [[1, 2], [3, 4]]
b = a
c = a[:]
d = copy.deepcopy(a)

a[0][0] = 99

print(b[0][0], c[0][0], d[0][0])

# Prediction: 99 99 1
# c is a shallow copy, so only the outer list is copied.
# The inner lists are still shared between a and c.

  # Part C - Performance

my_list = []

for i in range(100000):
    my_list.append(i)

my_set = set()

for i in range(100000):
    my_set.add(i)


# Time list membership

start = time.perf_counter()

result = 99999 in my_list

stop = time.perf_counter()

list_time = stop - start

print("List time:", list_time)


# Time set membership

start = time.perf_counter()

result = 99999 in my_set

stop = time.perf_counter()

set_time = stop - start

print("Set time:", set_time)
