from utils import read_input
from itertools import product


def map_fn(line):
    result, numbers = line.split(": ")
    result = int(result)

    numbers = [int(num) for num in numbers.split()]

    return result, numbers


def is_solvable(result, numbers):
    operators = ["*", "+"]

    for operator_order in product(operators, repeat=len(numbers) - 1):
        total = numbers[0]
        for idx, num in enumerate(numbers[1:]):
            if operator_order[idx - 1] == "+":
                total += num
            elif operator_order[idx - 1] == "*":
                total *= num
            if total > result:
                break
        if total == result:
            return True
    return False


def part_1():
    equations = read_input(7, map_fn)

    solvable = set()
    for result, numbers in equations:
        if is_solvable(result, numbers):
            solvable.add((result, tuple(numbers)))

    calibration_result = sum(res for res, _ in solvable)
    print(f"Part 1: {calibration_result}")
    assert calibration_result == 7885693428401

    return solvable


def is_solvable_with_concatenation(result, numbers):
    operators = ("*", "||", "+")

    for operator_order in product(operators, repeat=len(numbers) - 1):
        total = numbers[0]
        for idx, num in enumerate(numbers[1:]):
            if operator_order[idx - 1] == "+":
                total += num
            elif operator_order[idx - 1] == "*":
                total *= num
            elif operator_order[idx - 1] == "||":
                total = int(f"{total}{num}")
            if total > result:
                break

        if total == result:
            return True


def part_2(solved):
    equations = read_input(7, map_fn)

    calibration_result = 0
    for result, numbers in equations:
        if (result, tuple(numbers)) in solved:
            continue
        if is_solvable_with_concatenation(result, numbers):
            calibration_result += result

    calibration_result += sum(r for r, _ in solved)

    print(f"Part 2: {calibration_result}")
    assert calibration_result == 348360680516005


solvable = part_1()
part_2(solvable)
