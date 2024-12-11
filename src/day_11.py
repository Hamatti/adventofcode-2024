from utils import read_input
from functools import cache


def map_fn(line):
    return [int(n) for n in line.split()]


@cache
def blink(stone, iteration=0, max_iteration=25):
    if iteration == max_iteration:
        return 1

    if stone == 0:
        return blink(1, iteration + 1, max_iteration)

    stone_str = str(stone)
    digits = len(stone_str)
    if digits % 2 == 0:
        mid = digits // 2
        left = int(stone_str[:mid])
        right = int(stone_str[mid:])

        return blink(left, iteration + 1, max_iteration) + blink(
            right, iteration + 1, max_iteration
        )

    return blink(stone * 2024, iteration + 1, max_iteration)


def part_1():
    stones = read_input(11, map_fn)[0]
    stone_count = 0
    for stone in stones:
        stone_count += blink(stone)

    print(f"Part 1: {stone_count}")
    assert stone_count == 189092


def part_2():
    stones = read_input(11, map_fn)[0]
    stone_count = 0
    for stone in stones:
        stone_count += blink(stone, max_iteration=75)

    print(f"Part 2: {stone_count}")
    assert stone_count == 224869647102559


part_1()
part_2()
