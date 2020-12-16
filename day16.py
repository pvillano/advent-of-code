from collections import defaultdict

test_data = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""

data = """..."""

rules, your_ticket, nearby_tickets = data.rstrip().split('\n\n')

your_ticket = your_ticket.split("\n")[1].split(",")
your_ticket = list(map(int, your_ticket))

nearby_tickets = nearby_tickets.split('\n')[1:]
nearby_tickets = [list(map(int, ticket.split(","))) for ticket in nearby_tickets]

rule_lines = rules.split('\n')

rules = defaultdict(list)

for line in rule_lines:
    id, ranges = line.split(': ')
    ranges = ranges.split(" or ")
    for range_pair in ranges:
        start, stop = map(int, range_pair.split("-"))
        rules[id].append(range(start, stop + 1))


def valid(value):
    for r1, r2 in rules.values():
        if value in r1 or value in r2:
            return True
    return False


def valid_ticket(ticket):
    for value in ticket:
        if not valid(value):
            return False
    return True


tot = 0

for ticket in nearby_tickets:
    for value in ticket:
        if not valid(value):
            tot += value

print(tot)

valid_tickets = filter(valid_ticket, nearby_tickets)
valid_tickets = list(valid_tickets)

candidate_fields = [set(rules.keys()) for i in range(len(your_ticket))]

for ticket in valid_tickets:
    for i in range(len(ticket)):
        value = ticket[i]
        for rule_name, (range1, range2) in rules.items():
            if value not in range1 and value not in range2:
                candidate_fields[i].discard(rule_name)

while sum(map(len, candidate_fields)) > len(candidate_fields):
    for idx in range(len(candidate_fields)):
        if len(candidate_fields[idx]) == 1:
            only_one = list(candidate_fields[idx])[0]
            for jdx, item in enumerate(candidate_fields):
                if jdx != idx:
                    item.discard(only_one)

fields = [list(x)[0] for x in candidate_fields]

count = 0
prod = 1
field: str
for field, value in zip(fields, your_ticket):
    if field.startswith("departure"):
        count += 1
        prod *= value

print(count, prod)