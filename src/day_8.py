from utils import read_input
from collections import namedtuple, defaultdict
from itertools import combinations

Coordinate = namedtuple("Coordinate", ["x", "y"])


def create_map(inputs):
    antennas = defaultdict(set)
    for y, row in enumerate(inputs):
        for x, cell in enumerate(row):
            if cell != ".":
                antennas[cell].add(Coordinate(x, y))

    grid_size = len(inputs)
    return antennas, grid_size


def sign(a, b):
    return (a - b) // (abs(a - b))


def calculate_antinodes(pos1, pos2, grid_size):
    diff = abs(pos1.x - pos2.x), abs(pos1.y - pos2.y)
    pos1_signs = sign(pos1.x, pos2.x), sign(pos1.y, pos2.y)
    pos2_signs = sign(pos2.x, pos1.x), sign(pos2.y, pos1.y)

    antinode_1 = Coordinate(
        pos1.x + pos1_signs[0] * diff[0], pos1.y + pos1_signs[1] * diff[1]
    )
    antinode_2 = Coordinate(
        pos2.x + pos2_signs[0] * diff[0], pos2.y + pos2_signs[1] * diff[1]
    )

    antinodes = set()
    if (
        antinode_1.x >= 0
        and antinode_1.y >= 0
        and antinode_1.x < grid_size
        and antinode_1.y < grid_size
    ):
        antinodes.add(antinode_1)
    if (
        antinode_2.x >= 0
        and antinode_2.y >= 0
        and antinode_2.x < grid_size
        and antinode_2.y < grid_size
    ):
        antinodes.add(antinode_2)

    return antinodes


def calculate_all_antinodes(pos1, pos2, grid_size):
    diff = abs(pos1.x - pos2.x), abs(pos1.y - pos2.y)
    pos1_signs = sign(pos1.x, pos2.x), sign(pos1.y, pos2.y)
    pos2_signs = sign(pos2.x, pos1.x), sign(pos2.y, pos1.y)

    node = Coordinate(
        pos1.x + pos1_signs[0] * diff[0], pos1.y + pos1_signs[1] * diff[1]
    )

    antinodes = set([pos1, pos2])

    while node.x >= 0 and node.y >= 0 and node.x < grid_size and node.y < grid_size:
        antinodes.add(node)
        node = Coordinate(
            node.x + pos1_signs[0] * diff[0], node.y + pos1_signs[1] * diff[1]
        )

    node = Coordinate(
        pos2.x + pos2_signs[0] * diff[0], pos2.y + pos2_signs[1] * diff[1]
    )

    while node.x >= 0 and node.y >= 0 and node.x < grid_size and node.y < grid_size:
        antinodes.add(node)
        node = Coordinate(
            node.x + pos2_signs[0] * diff[0], node.y + pos2_signs[1] * diff[1]
        )

    return antinodes


def part_1():
    inputs = read_input(8, str)
    antennas, grid_size = create_map(inputs)
    antinodes = set()
    for positions in antennas.values():
        for pos1, pos2 in combinations(positions, 2):
            antinode_positions = calculate_antinodes(pos1, pos2, grid_size)
            antinodes.update(antinode_positions)

    result = len(antinodes)
    print(f"Part 1: {result}")
    assert result == 390


def part_2():
    inputs = read_input(8, str)
    antennas, grid_size = create_map(inputs)
    antinodes = set()
    for positions in antennas.values():
        for pos1, pos2 in combinations(positions, 2):
            antinode_positions = calculate_all_antinodes(pos1, pos2, grid_size)
            antinodes.update(antinode_positions)

    result = len(antinodes)
    print(f"Part 2: {result}")
    assert result == 1246


part_1()
part_2()
