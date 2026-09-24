class DivisionByZeroError(Exception):
    pass


def calculate(a, b, op):

    match op:
        case '+':
            x = a + b
            return x

        case '-':
            x = a - b
            return x

        case '*':
            x = a * b
            return x

        case '/':
            try:
                x = a / b
                return x
            except ZeroDivisionError:
                raise DivisionByZeroError("Division by zero is not allowed")

        case _:
            raise ValueError("Unknown operator")


def main():
    try:
        x = calculate(14, 94, '=')

    except DivisionByZeroError as e:
        print(e)

    except ValueError as e:
        print(e)

    else:
        print(x)

    finally:
        print("Calculation attempted.")


main()