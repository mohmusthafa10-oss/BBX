import random

secret=random.randint(1,100)

for attempt in range(7):

    while True:
        try:
            user = int(input("Guess a number btw 1-100 : "))
            break
        except ValueError:
            print("Please enter a number.")

        

    if user == secret:
        print("You Won")
        break

    elif user < secret:
        print("Higher")

    else:
        print("Lower")

else:
    print(f"You Lost ; the no is {secret}")