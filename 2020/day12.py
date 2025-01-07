from copy import copy
from math import sin, cos, radians, atan2, sqrt

data = """..."""

test_data = """F10
N3
F7
R90
F11"""

lines = data.rstrip().split("\n")


#
# class Interpreter:
#     def __init__(self, lines):
#         self.heading = 0
#         self.x = 0
#         self.y = 0
#         self.lines = copy(lines)
#
#     def run(self):
#         for line in self.lines:
#             code, *value = line
#             value = int("".join(value))
#             getattr(self, code)(value)
#             print(self.x, self.y)
#         return abs(self.x) + abs(self.y)
#
#     def N(self, value):
#         self.y += value
#
#     def S(self, value):
#         self.y -= value
#
#     def E(self, value):
#         self.x += value
#
#     def W(self, value):
#         self.x -= value
#
#     def L(self, value):
#         self.heading += value
#         self.heading %= 360
#
#     def R(self, value):
#         self.heading -= value
#         self.heading %= 360
#
#     def F(self, value):
#         self.x += value * cos(radians(self.heading))
#         self.y += value * sin(radians(self.heading))


class Interpreter:
    def __init__(self, lines):
        self.x = 0
        self.y = 0
        self.wx = 10
        self.wy = 1
        self.lines = copy(lines)

    def run(self):
        for line in self.lines:
            code, value = line[0], int(line[1:])
            getattr(self, code)(value)
        return int(abs(self.x) + abs(self.y))

    def N(self, value):
        self.wy += value

    def S(self, value):
        self.wy -= value

    def E(self, value):
        self.wx += value

    def W(self, value):
        self.wx -= value

    def L(self, value):
        heading = atan2(self.wy, self.wx)
        magnitude = sqrt(self.wy ** 2 + self.wx ** 2)
        heading += radians(value)
        self.wx = cos(heading) * magnitude
        self.wy = sin(heading) * magnitude

    def R(self, value):
        return self.L(-value)

    def F(self, value):
        self.x += value * (self.wx)
        self.y += value * (self.wy)


print(Interpreter(lines).run())
