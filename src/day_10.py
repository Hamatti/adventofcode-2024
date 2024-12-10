from utils import read_input
from collections import namedtuple

Coordinate = namedtuple("Coordinate", ["x", "y"])


def create_grid(inputs):
    grid = {}
    trailheads = []
    for y, row in enumerate(inputs):
        for x, cell in enumerate(row):
            cell = int(cell)
            coordinate = Coordinate(x, y)
            grid[coordinate] = cell
            if cell == 0:
                trailheads.append(coordinate)
    return grid, trailheads


def get_neighbours(coordinate):
    return [
        Coordinate(coordinate.x - 1, coordinate.y),
        Coordinate(coordinate.x + 1, coordinate.y),
        Coordinate(coordinate.x, coordinate.y - 1),
        Coordinate(coordinate.x, coordinate.y + 1),
    ]


def find_paths_to_peak(height, position, grid):
    if height == 9:
        return [position]

    paths = []
    for neighbour in get_neighbours(position):
        neighbouring_height = grid.get(neighbour)
        if neighbouring_height == height + 1:
            paths += find_paths_to_peak(neighbouring_height, neighbour, grid)

    return paths


def part_1():
    inputs = read_input(10, str)
    grid, trailheads = create_grid(inputs)
    score = 0
    for trailhead in trailheads:
        paths = find_paths_to_peak(0, trailhead, grid)
        score += len(set(paths))
    print(f"Part 1: {score}")
    assert score == 587


def part_2():
    inputs = read_input(10, str)
    grid, trailheads = create_grid(inputs)
    rating = 0
    for trailhead in trailheads:
        rating += len(find_paths_to_peak(0, trailhead, grid))
    print(f"Part 2: {rating}")
    assert rating == 1340


part_1()
part_2()
