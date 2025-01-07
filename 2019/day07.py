
from math import *
from itertools import *
from collections import *


data = (3,8,1001,8,10,8,105,1,0,0,21,38,55,64,81,106,187,268,349,430,99999,3,9,101,2,9,9,1002,9,2,9,101,5,9,9,4,9,99,3,9,102,2,9,9,101,3,9,9,1002,9,4,9,4,9,99,3,9,102,2,9,9,4,9,99,3,9,1002,9,5,9,1001,9,4,9,102,4,9,9,4,9,99,3,9,102,2,9,9,1001,9,5,9,102,3,9,9,1001,9,4,9,102,5,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,99)

def amp(input):
    my_data = list(data)
    ptr = 0
    registers = [0]*4
    while my_data[ptr] != 99:
        opstr = str(my_data[ptr]).zfill(5)
        op = int(opstr[-2:])
        modes = [
            'padding',
            int(opstr[2]),
            int(opstr[1]),
            int(opstr[0]),
        ]
        for i in range(4):
            try:
                if modes[i] == 0:
                    a = my_data[ptr + i]
                    b = my_data[a]
                    registers[i] = b
                elif modes[i] == 1:
                    a = my_data[ptr + i]
                    registers[i] = a
            except IndexError:
                pass
        if op == 1:
            my_data[my_data[ptr + 3]] = registers[1] + registers[2]
            ptr += 4
        elif op == 2:
            my_data[my_data[ptr + 3]] = registers[1] * registers[2]
            ptr += 4
        elif op == 3:
            my_data[my_data[ptr + 1]] = next(input)
            ptr += 2
        elif op == 4:
            yield registers[1]
            ptr += 2
        elif op == 5:
            if registers[1]:
                ptr = registers[2]
            else:
                ptr += 3
        elif op == 6:
            if not registers[1]:
                ptr = registers[2]
            else:
                ptr += 3
        elif op == 7:
            my_data[my_data[ptr + 3]] = int(registers[1] < registers[2])
            ptr += 4
        elif op == 8:
            my_data[my_data[ptr + 3]] = int(registers[1] == registers[2])
            ptr += 4
        else:
            return
best = 0
for A,B,C,D,E in permutations(range(5, 10)):
    buffer = [A, 0]
    def loopback():
        for i in buffer:
            yield i
    x = 0
    for x in amp(chain([E],
            amp(chain([D],
            amp(chain([C],
            amp(chain([B],
            amp(loopback()
            ))))))))):
        buffer.append(x)
    if x > best:
        print(x)
        best = x
