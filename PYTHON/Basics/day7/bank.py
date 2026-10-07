from abc import ABC, abstractmethod


class InsufficientFundsError(Exception):
    pass


class Account(ABC):

    def __init__(self, name, balance):
        self.name = name
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount):
        self.__balance += amount

    def withdraw(self, amount):
        if amount > self.__balance:
            raise InsufficientFundsError("Insufficient balance")

        self.__balance -= amount

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["balance"])

    @staticmethod
    def validate_account_number(number):
        return number.isdigit() and len(number) == 10

    @abstractmethod
    def calculate_interest(self):
        ...


    def __str__(self):
        return f"{self.__class__.__name__}: {self.name} | Balance: {self.balance}"

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}', {self.balance})"


class SavingsAccount(Account):

    def calculate_interest(self):
        return self.balance * 0.05


class CurrentAccount(Account):

    def calculate_interest(self):
        return self.balance * 0.02


if __name__ == "__main__":

    savings = SavingsAccount("Rex", 10000)

    print(savings)
    print(repr(savings))
    print("Balance:", savings.balance)
    print("Interest:", savings.calculate_interest())

    savings.deposit(2000)
    print("After deposit:", savings.balance)

    savings.withdraw(3000)
    print("After withdrawal:", savings.balance)

    print(
        "Valid account number:",
        Account.validate_account_number("1234567890")
    )

    data = {
        "name": "John",
        "balance": 5000
    }

    account = SavingsAccount.from_dict(data)
    print(account)