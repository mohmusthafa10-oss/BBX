# PART A

names=['Ali','Jhon','David']

for name in names:
    print(name)

numbers = [1, 2, 3, 4, 5, 6]
result=[x * x for x in numbers if x % 2 == 0]
print(result)


items = [10, 20, 30]
target = 20

for item in items:
    if item == target:
        print("Key found")
        break


else:
    print("Key not found")


my_list = [10, 20, 30]

if my_list:
    process(my_list)


a = [1, 2, 3]
b = ["A", "B", "C"]

for i,j in zip(a,b):
    print(i,j)




# PART B

x=[
    "FizzBuzz" if i%3==0 and i%5==0 
    else "Fizz" if i%3==0
    else "Buzz" if i%5==0
    else i
    for i in range(1,101)
]
print (x)