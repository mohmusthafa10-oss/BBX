print(7 // 2, -7 // 2, 7 % 2, -7 % 2)  
# 3 -4 1 1

print(4 / 2, type(4 / 2))
# 2.0 <class 'float>

x = 256
y = 256
print(x is y)
# True

x = 257
y = 257
print(x is y)
# True

print(0.1 + 0.2 == 0.3)
# False , because 0.1 and 0.2 is taken as binary 

a = [1,2]
b = [1,2]
print(a == b, a is b)
# True , False

print(bool(''), bool('0'), bool([]), bool([0]))
# False True False True

print(int('10.5'))
# This raise valuError , because type is int and the value is string

age = input('Age: ')
print(age + 5)
# This raise a typeError ,Because input values are string and we are performing +5 which is int we can solve this by converting age into int "int(age)"