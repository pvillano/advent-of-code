from itertools import count
from math import lcm

data ="""..."""

test_data = """939
7,13,x,x,59,x,31,19"""

import time
execution_start = time.time()

lines = test_data.rstrip().split("\n")
#
# start_time, bus_ids = lines
# start_time = int(start_time)
# bus_ids = [int(x) for x in bus_ids.split(",") if x != "x"]
#
# for time in count(start_time):
#     for id in bus_ids:
#         if time % id == 0:
#             print(id, time, time - start_time, (time - start_time) * id)
#             exit(0)


start_time, bus_ids = lines

pairs = []
for i, id in enumerate(bus_ids.split(",")):
    if id == "x":
        continue
    else:
        pairs.append((i,int(id)))

bus_time = 0
lcm_previous = 1

for offset, id in pairs:
    while (bus_time + offset) % id != 0:
        bus_time += lcm_previous
    lcm_previous = lcm(lcm_previous, id)

print(bus_time)


print(time.time() - execution_start)