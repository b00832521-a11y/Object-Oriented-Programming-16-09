import math


# Question 1 : nombres complexes (+ et -)
class Complex:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    def __repr__(self):
        sign = "+" if self.imag >= 0 else "-"
        return f"{self.real} {sign} {abs(self.imag)}i"

    def __add__(self, other):
        return Complex(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        return Complex(self.real - other.real, self.imag - other.imag)


# Question 2 : Person, comparaison > sur l'age
class Person:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def __gt__(self, other):
        return self.age > other.age


# Question 3 : Vector, * = produit scalaire
class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z


# Question 4 : Circle, les 6 comparaisons selon le rayon
class Circle:
    def __init__(self, radius):
        self.radius = radius

    def __lt__(self, other):
        return self.radius < other.radius

    def __gt__(self, other):
        return self.radius > other.radius

    def __eq__(self, other):
        return self.radius == other.radius

    def __ne__(self, other):
        return self.radius != other.radius

    def __ge__(self, other):
        return self.radius >= other.radius

    def __le__(self, other):
        return self.radius <= other.radius


# Question 5 : Point2D, comparaisons selon la distance a l'origine
class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __lt__(self, other):
        return self.distance() < other.distance()

    def __gt__(self, other):
        return self.distance() > other.distance()

    def __eq__(self, other):
        return self.distance() == other.distance()

    def __ne__(self, other):
        return self.distance() != other.distance()

    def __ge__(self, other):
        return self.distance() >= other.distance()

    def __le__(self, other):
        return self.distance() <= other.distance()


# Question 6 : Matrix, * = produit matriciel
class Matrix:
    def __init__(self, rows):
        self.rows = rows

    def __repr__(self):
        return f"Matrix({self.rows})"

    def __mul__(self, other):
        if len(self.rows[0]) != len(other.rows):
            raise ValueError("Dimensions incompatibles")
        n_rows = len(self.rows)
        n_inner = len(other.rows)
        n_cols = len(other.rows[0])
        result = []
        for i in range(n_rows):
            new_row = []
            for j in range(n_cols):
                total = 0
                for k in range(n_inner):
                    total += self.rows[i][k] * other.rows[k][j]
                new_row.append(total)
            result.append(new_row)
        return Matrix(result)


if __name__ == "__main__":
    print(Complex(5, 3) - Complex(2, 1), "|", Complex(3, 2) + Complex(1, 4))
    print(Person("Alice", 30, "F") > Person("Bob", 25, "M"))
    print(Vector(1, 2, 3) * Vector(4, 5, 6))
    print(Circle(2) < Circle(5), Circle(2) == Circle(5))
    print(Point2D(3, 4) > Point2D(1, 1), Point2D(3, 4) == Point2D(-5, 0))
    print(Matrix([[1, 2], [3, 4]]) * Matrix([[5, 6], [7, 8]]))
