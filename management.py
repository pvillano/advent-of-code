import os
if __name__ == '__main__':
    for i in range(1, 26):
        filename = f'day{i:0>2}'
        if not os.path.isfile(filename):
            with open(filename + '.txt', 'w') as f:
                f.write("\n")
            with open(filename + '.py', 'w') as f:
                f.write(f"""
from math import *
from itertools import *


with open('{filename}.txt') as f:
    for line in f:
        for token in line.split(', '):
            answer = token
            
print(answer)
""")
