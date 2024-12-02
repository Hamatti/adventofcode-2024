from utils import read_input
from itertools import pairwise


def map_fn(line):
    """Splits each line of input by whitespace and maps
    each value to integer.

    Example line:
    7 6 4 2 1
    """
    return [int(number) for number in line.split()]


def calc_sign(a, b):
    """Returns:
    0 if a == b
    -1 if a < b
    1 if a > b
    """
    diff = a - b
    if diff == 0:
        return 0
    return diff / abs(diff)


def is_report_safe(report):
    """Checks if a given list of numbers satisfies
    following rules:

    1. Numbers are either increasing or decreasing consistently
    2. Difference between two consecutive numbers is 0 < number < 4
    """
    sign = calc_sign(report[0], report[1])
    for prev, next in pairwise(report):
        diff = abs(prev - next)
        if diff <= 0 or diff > 3:
            return False
        if sign != calc_sign(prev, next):
            return False
    return True


def check_report_with_dampener(report):
    """Checks if a given list of numbers satisfies following rules:

    1. Numbers are either increasing or decreasing consistently
    2. Difference between two consecutive numbers is 0 < number < 4

    If it fails a rule, it retries by removing one number each time.
    If any of the shorter lists satisfies the rules, returns True.
    """
    if is_report_safe(report):
        return True

    for idx, _ in enumerate(report):
        if is_report_safe(report[:idx] + report[idx + 1 :]):
            return True

    return False


def part_1():
    reports = read_input(2, map_fn)
    valid_reports = 0
    for report in reports:
        if is_report_safe(report):
            valid_reports += 1
    print(f"Part 1: {valid_reports}")
    assert valid_reports == 549


def part_2():
    reports = read_input(2, map_fn)
    valid_reports = 0
    for report in reports:
        if check_report_with_dampener(report):
            valid_reports += 1
    print(f"Part 2: {valid_reports}")
    assert valid_reports == 589


part_1()
part_2()
