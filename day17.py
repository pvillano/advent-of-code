import z3

from utils import benchmark, get_day, test
from utils.parsing import extract_ints


def parse(raw: str):
    registers, program = raw.split("\n\n")
    registers = registers.splitlines()
    registers = {lhs[-1]: int(rhs) for lhs, rhs in [r.split(": ") for r in registers]}
    program = list(extract_ints(program))
    return registers, program


def part1(raw: str):
    registers, program = parse(raw)
    ip = 0
    out = []
    while ip in range(len(program)):
        op = program[ip]
        literal = program[ip + 1]
        combo = [0, 1, 2, 3, registers['A'], registers['B'], registers['C']][literal]
        match op:
            case 0:
                registers['A'] = registers['A'] >> combo
            case 1:
                registers['B'] ^= literal
            case 2:
                registers['B'] = combo % 8
            case 3:
                if registers['A'] != 0:
                    ip = literal
                    continue
            case 4:
                registers['B'] ^= registers['C']
            case 5:
                out.append(combo % 8)
            case 6:
                registers['B'] = registers['A'] >> combo
            case 7:
                registers['C'] = registers['A'] >> combo
        ip += 2
    return ','.join(map(str, out))


def part2(raw):
    registers, program = parse(raw)
    ip = 0
    a = z3.BitVec('a', len(program) * 3 + 3)
    optimizer = z3.Optimize()
    optimizer.minimize(a)
    optimizer.add(a > 0)
    registers['A'] = a
    times_outputted = 0
    while True:
        op = program[ip]
        literal = program[ip + 1]
        combo = [0, 1, 2, 3, registers['A'], registers['B'], registers['C']][literal]
        match op:
            case 0:
                registers['A'] = registers['A'] >> combo
            case 1:
                registers['B'] = registers['B'] ^ literal
            case 2:
                registers['B'] = combo % 8
            case 3:
                if times_outputted < len(program):
                    optimizer.add(registers['A'] != 0)
                    ip = literal
                    continue
                else:
                    optimizer.add(registers['A'] == 0)
                    break
            case 4:
                registers['B'] ^= registers['C']
            case 5:
                optimizer.add(combo % 8 == program[times_outputted])
                times_outputted += 1
            case 6:
                registers['B'] = registers['A'] >> combo
            case 7:
                registers['C'] = registers['A'] >> combo
        ip += 2
    optimizer.check()
    return optimizer.model().eval(a)


test1 = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""

expected1 = "4,6,3,5,6,3,5,2,1,0"

test2 = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""
expected2 = 117440


def main():
    raw = get_day(17)
    benchmark(part2, raw)
    test(part1, test1, expected1)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
