entries = [...]
# for x in entries:
#     for y in entries:
#         if x + y == 2020:
#             print(x,y,x*y)

for x in entries:
    for y in entries:
        for z in entries:
            if x + y + z == 2020:
                print(x, y, z, x * y * z)
