class Vehicle:
    def drive(self):
        return "Driving a vehicle"


class Car(Vehicle):
    def drive(self):
        return "Driving a car"


class Bicycle(Vehicle):
    def drive(self):
        return "Riding a bicycle"


class Person:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def introduce(self):
        return f"Hi, I'm {self.name}, {self.age} years old, and I live at {self.address}."


class Student(Person):
    def __init__(self, name, age, address, field_of_study):
        super().__init__(name, age, address)
        self.field_of_study = field_of_study

    def introduce(self):
        return f"Hi, I'm {self.name}, {self.age} years old, and I study {self.field_of_study}."


class Employee(Person):
    def __init__(self, name, age, address, company):
        super().__init__(name, age, address)
        self.company = company

    def introduce(self):
        return f"Hi, I'm {self.name}, {self.age} years old, and I work at {self.company}."


class BankAccount:
    def __init__(self, account_number, balance=0):
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            return False
        self.balance -= amount
        return True

    def transfer(self, destination, amount):
        if not self.withdraw(amount):
            return False
        destination.deposit(amount)
        return True


class SavingsAccount(BankAccount):
    def __init__(self, account_number, balance=0, interest_rate=0.0):
        super().__init__(account_number, balance)
        self.interest_rate = interest_rate

    def add_interest(self):
        self.balance += self.balance * self.interest_rate

    def check_balance(self):
        return self.balance


if __name__ == "__main__":
    print(Vehicle().drive(), "|", Car().drive(), "|", Bicycle().drive())
    print(Person("Alice", 40, "1 rue A").introduce())
    print(Student("Bob", 20, "2 rue B", "Computer Science").introduce())
    print(Employee("Carla", 30, "3 rue C", "Acme").introduce())
    a = BankAccount("FR01", 100)
    s = SavingsAccount("FR02", 50, interest_rate=0.10)
    print(a.transfer(s, 30), a.balance, s.balance)
    print(a.transfer(s, 1000), a.balance, s.balance)
    s.add_interest()
    print(s.check_balance())
