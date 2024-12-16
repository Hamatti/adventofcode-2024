from utils import read_input, create_grid, Coordinate
from typing import List, Callable, Literal, Tuple
from collections import defaultdict
from itertools import pairwise
import math

Grid = dict[Coordinate, str]
Direction = Literal["U", "D", "R", "L"]
State = Tuple[Coordinate, Direction]


def print_grid(grid: Grid, start: Coordinate, end: Coordinate) -> None:
    """Prints a sparse grid, replacing missing items with '.'
    and the robot position with '@'."""
    max_x = max(x for x, y in grid)
    max_y = max(y for x, y in grid)
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if start == (x, y):
                print("S", end="")
            elif end == (x, y):
                print("E", end="")
            else:
                print(grid.get((x, y), "."), end="")
        print()
    print()


def reconstruct_path(came_from: dict, item: State) -> List[State]:
    path: List[State] = []
    while item in came_from:
        item = came_from[item]
        path.append(item)
    return list(reversed(path))


def constant_factory(x: int) -> Callable[[], int]:
    return lambda: x


def distance_to_target(start: Coordinate, target: Coordinate) -> int:
    return abs(start.x - target.x) + abs(start.y - target.y)


def get_valid_neighbours(
    current: Coordinate, grid: Grid, path: List[State]
) -> List[Coordinate]:
    neighbours = [
        Coordinate(current.x, current.y - 1),
        Coordinate(current.x, current.y + 1),
        Coordinate(current.x - 1, current.y),
        Coordinate(current.x + 1, current.y),
    ]

    path = [coord for coord, _ in path]

    return [
        neighbour
        for neighbour in neighbours
        if grid.get(neighbour) != "#" and neighbour not in path
    ]


def smallest_f_score(
    f_score: dict[State, int],
    open_set: set[State],
) -> State:
    first = open_set.pop()
    smallest = f_score[first]
    smallest_pos = first[0]
    smallest_direction = first[1]
    for pos, direction in open_set:
        if (score := f_score[pos, direction]) < smallest:
            smallest_pos = pos
            smallest_direction = direction
            smallest = score
    open_set.add(first)

    return smallest_pos, smallest_direction


def get_next_direction(
    current: Coordinate, neighbour: Coordinate, direction: Direction
) -> Direction:
    nexts: dict[Tuple[int, int], Direction] = {
        (0, 1): "U",
        (0, -1): "D",
        (1, 0): "L",
        (-1, 0): "R",
    }
    return nexts[(current.x - neighbour.x, current.y - neighbour.y)]


def find_shortest_path(
    start: Coordinate, target: Coordinate, grid: Grid, direction: Direction
) -> Tuple[List[State], int] | None:
    """A* path finding to find the shortest path from start to target."""
    open_set = set()
    open_set.add((start, direction))
    came_from: dict[State, State] = {}

    g_score: dict[State, int] = defaultdict(constant_factory(math.inf))
    g_score[(start, direction)] = 0

    f_score: dict[State, int] = defaultdict(constant_factory(math.inf))
    f_score[(start, direction)] = distance_to_target(start, target)

    while open_set:
        current, direction = smallest_f_score(f_score, open_set)
        if current == target:
            score = g_score[(current, direction)]
            return (
                reconstruct_path(came_from, (current, direction))
                + [(current, direction)],
                score,
            )
        open_set.remove((current, direction))

        path = reconstruct_path(came_from, (current, direction))
        for neighbour in get_valid_neighbours(current, grid, path):
            next_direction = get_next_direction(current, neighbour, direction)
            tentative_g_score = g_score[(current, direction)] + 1
            if next_direction != direction:
                tentative_g_score += 1000

            if tentative_g_score < g_score[(neighbour, next_direction)]:
                came_from[(neighbour, next_direction)] = (current, direction)
                g_score[(neighbour, next_direction)] = tentative_g_score
                f_score[(neighbour, next_direction)] = (
                    tentative_g_score + distance_to_target(neighbour, target)
                )
                open_set.add((neighbour, next_direction))

    return None


def print_path(grid: Grid, path: List[State]):
    path = [c for c, d in path]
    max_x = max(x for x, y in grid)
    max_y = max(y for x, y in grid)
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (x, y) in path:
                print("o", end="")
            else:
                if grid.get((x, y)):
                    print("#", end="")
                else:
                    print(".", end="")
        print()
    print()


def calculate_score(path):
    score = 0
    for (_, prev_dir), (_, next_dir) in pairwise(path):
        score += 1
        if next_dir != prev_dir:
            score += 1000

    return score


def part_1():
    data = read_input(16, str)
    grid = create_grid(data, predicate=lambda x: x != ".")

    start = [key for key, value in grid.items() if value == "S"][0]
    del grid[start]

    target = [key for key, value in grid.items() if value == "E"][0]
    del grid[target]

    path, score = find_shortest_path(start, target, grid, "R")
    print(f"Part 1: {score}")

    assert score == 94436


def part_2():
    raise NotImplementedError


part_1()
