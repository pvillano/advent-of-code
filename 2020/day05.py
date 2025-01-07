# best = 0
# for line in open("day05.txt"):
#     stripped = line.strip()
#     row, seat = stripped[:7], stripped[7:]
#     row = row.replace("B", "1").replace("F", "0")
#     row = int(row, 2)
#     seat = seat.replace("L", "0").replace("R", "1")
#     seat = int(seat, 2)
#     id = row * 8 + seat
#     best = max(id, best)
# print(best)

seats = []
for line in open("day05.txt"):
    stripped = line.strip()
    row, seat = stripped[:7], stripped[7:]
    row = row.replace("B", "1").replace("F", "0")
    row = int(row, 2)
    seat = seat.replace("L", "0").replace("R", "1")
    seat = int(seat, 2)
    id = row * 8 + seat
    seats.append(id)
seats.sort()
for x in seats:
    if x + 1 not in seats:
        print(x + 1)
