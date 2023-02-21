with open("input.txt") as f:
    str_in = [s.strip() for s in f.readlines()]


def isvar(char):
    return char in "wxyz"


def run(program, inp):
    vars = {c: 0 for c in "wxyz"}
    inps = [int(i) for i in str(inp)]
    for line in program:
        struct = line[:3]
        param = line.split(" ")[1:]
        if struct == "inp":
            print(to_base_26(vars["z"]))
            vars[param[0]] = inps.pop(0)
        else:
            assign, source = param
            val = vars[source] if isvar(source) else int(source)
            if struct == "add":
                vars[assign] += val
            elif struct == "mul":
                vars[assign] *= val
            elif struct == "div":
                vars[assign] //= val
            elif struct == "mod":
                vars[assign] %= val
            elif struct == "eql":
                vars[assign] = 1 if vars[assign] == val else 0
    return vars

def to_base_26(num):
    st = ""
    while num != 0:
        st = str(num % 26) + " " + st
        num //= 26
    return st

print(to_base_26(26))

def has_zero(num):
    return "0" in str(num)


def part1():
    return run(str_in, 91897399498995)

def part2():
    return run(str_in, 51121176121391)
print(part2())

import re
tmp = "\n".join(str_in)
# print(tmp.replace("inp w\nmul x 0\nadd x z\nmod x 26\ndiv z ", " ")
#       .replace("\neql x w\neql x 0\nmul y 0\nadd y 25\nmul y x\nadd y 1\nmul z y\nmul y 0\nadd y w\nadd y ", " ")
#       .replace("\nmul y x\nadd z y", " ")
#       .replace("\nadd x", " "))