import time

from utils import debug_print, getlines

data = """..."""

test_data = """2 * 3 + (4 * 5)"""

lines = getlines(data, data)

start_time = time.time()


tot = 0
#
# for line in lines:
#     num_stack = []
#     op_stack = []
#     tokens = line.replace("(", "( ").replace(")", " )").split(" ")
#     for token in tokens:
#         if token == "+":
#             op_stack.append(token)
#         elif token == "*":
#             op_stack.append(token)
#         elif token == ")":
#             paren = op_stack.pop()
#             assert paren == "("
#             while op_stack:
#                 symb = op_stack.pop()
#                 if symb == "+":
#                     n1, n2 = num_stack.pop(), num_stack.pop()
#                     num_stack.append(n1 + n2)
#                 elif symb == "*":
#                     n1, n2 = num_stack.pop(), num_stack.pop()
#                     num_stack.append(n1 * n2)
#                 elif symb == "(":
#                     op_stack.append("(")
#                     break
#         elif token == "(":
#             op_stack.append("(")
#         else:
#             num = int(token)
#             num_stack.append(num)
#             while op_stack:
#                 symb = op_stack.pop()
#                 if symb == "+":
#                     n1, n2 = num_stack.pop(), num_stack.pop()
#                     num_stack.append(n1 + n2)
#                 elif symb == "*":
#                     n1, n2 = num_stack.pop(), num_stack.pop()
#                     num_stack.append(n1 * n2)
#                 elif symb == "(":
#                     op_stack.append("(")
#                     break
#         debug_print(token, op_stack, num_stack)
#
#     tot += num_stack[0]

for line in lines:
    num_stack = []
    op_stack = []
    tokens = line.replace("(", "( ").replace(")", " )").split(" ")
    for token in tokens:
        if token == "+":
            op_stack.append(token)
        elif token == "*":
            op_stack.append(token)
        elif token == ")":
            while op_stack:
                symb = op_stack.pop()
                if symb == "+":
                    n1, n2 = num_stack.pop(), num_stack.pop()
                    num_stack.append(n1 + n2)
                elif symb == "*":
                    n1, n2 = num_stack.pop(), num_stack.pop()
                    num_stack.append(n1 * n2)
                elif symb == "(":
                    break
        elif token == "(":
            op_stack.append("(")
        else:
            num = int(token)
            num_stack.append(num)
            if op_stack and op_stack[-1] == "*":
                continue
            while op_stack:
                debug_print(token, op_stack, num_stack)
                symb = op_stack.pop()
                if symb == "+":
                    n1, n2 = num_stack.pop(), num_stack.pop()
                    num_stack.append(n1 + n2)
                elif symb == "*":
                    # n1, n2 = num_stack.pop(), num_stack.pop()
                    # num_stack.append(n1 * n2)
                    op_stack.append(symb)
                    break
                elif symb == "(":
                    op_stack.append("(")
                    break
        debug_print(token, op_stack, num_stack)
    while op_stack:
        debug_print(op_stack, num_stack)
        symb = op_stack.pop()
        if symb == "+":
            n1, n2 = num_stack.pop(), num_stack.pop()
            num_stack.append(n1 + n2)
        elif symb == "*":
            n1, n2 = num_stack.pop(), num_stack.pop()
            num_stack.append(n1 * n2)
        elif symb == "(":
            op_stack.append("(")

    debug_print(op_stack, num_stack)
    debug_print()

    if len(num_stack) > 1:
        raise ValueError
    tot += num_stack[0]

print(tot)

# not 256968103841318








debug_print("debug")

print("ran in", time.time() - start_time, "seconds")
