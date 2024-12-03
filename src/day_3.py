from utils import read_input
import re


p1_pattern = r"mul\((\d+),(\d+)\)"
p2_pattern = r"(mul\((\d+),(\d+)\)|do\(\)|don't\(\))"


def map_fn(line):
    return re.findall(p1_pattern, line)


def map_fn_2(line):
    return re.findall(p2_pattern, line)


def part_1():
    lines = read_input(3, map_fn)
    result = 0
    for instructions in lines:
        for a, b in instructions:
            result += int(a) * int(b)

    print(f"Part 1: {result}")
    assert result == 161085926


def part_2():
    lines = read_input(3, map_fn_2)
    result = 0
    enabled = True
    for instructions in lines:
        for instruction in instructions:
            match instruction:
                case ("do()", _, _):
                    enabled = True
                case ("don't()", _, _):
                    enabled = False
                case (operator, a, b) if "mul" in operator and enabled:
                    result += int(a) * int(b)
    print(f"Part 2: {result}")
    assert result == 82045421


part_1()
part_2()
