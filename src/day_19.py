from utils import read_multisection_input
from typing import List, Tuple
from functools import cache


def map_patterns(section: str) -> List[str]:
    return section.split(", ")


def map_designs(section: str) -> List[str]:
    return section.split("\n")


def is_valid_design(design: str, patterns: List[str]) -> bool:
    """Recursively check if a design can be constructed of any
    of the patterns available"""
    # Empty design is always valid
    if len(design) == 0:
        return True

    for pattern in patterns:
        # If a design starts with a pattern, check if the rest
        # can be constructed from available pieces
        if design.startswith(pattern):
            rest = design[len(pattern) :]
            if is_valid_design(rest, patterns):
                return True

    return False


@cache
def count_valid_designs(design: str, patterns: Tuple[str]) -> int:
    """Count how many ways a design can be implemented with given patterns."""
    if len(design) == 0:
        return 1

    count = 0
    for pattern in patterns:
        if design.startswith(pattern):
            count += count_valid_designs(design[len(pattern) :], patterns)
    return count


def part_1():
    patterns, designs = read_multisection_input(19, [map_patterns, map_designs])
    valid_designs = 0
    for design in designs:
        if is_valid_design(design, patterns):
            valid_designs += 1

    print(f"Part 1: {valid_designs}")
    assert valid_designs == 358


def part_2():
    patterns, designs = read_multisection_input(19, [map_patterns, map_designs])
    patterns = tuple(patterns)

    valid_designs = 0
    for design in designs:
        valid_designs += count_valid_designs(design, patterns)

    print(f"Part 2: {valid_designs}")
    assert valid_designs == 600639829400603


if __name__ == "__main__":
    part_1()
    part_2()
