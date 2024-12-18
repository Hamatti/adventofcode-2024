from utils import read_input, Coordinate
from collections import defaultdict
import math
from typing import Callable, List, Tuple


def map_fn(line: str) -> Coordinate:
    x, y = line.split(",")
    return Coordinate(int(x), int(y))


def constant_factory(x: int) -> Callable[[], int]:
    return lambda: x


def distance_to_target(start: Coordinate, target: Coordinate) -> int:
    return abs(start.x - target.x) + abs(start.y - target.y)


def smallest_f_score(
    f_score: dict[Coordinate, int],
    open_set: set[Coordinate],
) -> Coordinate:
    first = open_set.pop()
    smallest = f_score[first]
    smallest_pos = first
    for pos in open_set:
        if (score := f_score[pos]) < smallest:
            smallest_pos = pos
            smallest = score
    open_set.add(first)

    return smallest_pos


def reconstruct_path(came_from: dict, item: Coordinate) -> List[Coordinate]:
    path: List[Coordinate] = []
    while item in came_from:
        item = came_from[item]
        path.append(item)
    return list(reversed(path))


def get_valid_neighbours(
    current: Coordinate, corrupted: List[Coordinate]
) -> List[Coordinate]:
    neighbours = [
        Coordinate(current.x, current.y - 1),
        Coordinate(current.x, current.y + 1),
        Coordinate(current.x - 1, current.y),
        Coordinate(current.x + 1, current.y),
    ]

    return [
        neighbour
        for neighbour in neighbours
        if neighbour not in corrupted
        and neighbour.x >= 0
        and neighbour.y >= 0
        and neighbour.x <= 70
        and neighbour.y <= 70
    ]


def find_shortest_path(
    start: Coordinate, target: Coordinate, corrupted: List[Coordinate]
) -> Tuple[List[Coordinate], int] | None:
    """A* path finding to find the shortest path from start to target."""
    open_set = set()
    open_set.add(start)
    came_from: dict[Coordinate, Coordinate] = {}

    g_score: dict[Coordinate, int] = defaultdict(constant_factory(math.inf))
    g_score[start] = 0

    f_score: dict[Coordinate, int] = defaultdict(constant_factory(math.inf))
    f_score[start] = distance_to_target(start, target)

    while open_set:
        current = smallest_f_score(f_score, open_set)
        if current == target:
            score = g_score[current]
            return (
                reconstruct_path(came_from, current) + [current],
                score,
            )
        open_set.remove(current)

        for neighbour in get_valid_neighbours(current, corrupted):
            tentative_g_score = g_score[current] + 1

            if tentative_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = tentative_g_score
                f_score[neighbour] = tentative_g_score + distance_to_target(
                    neighbour, target
                )
                open_set.add(neighbour)

    return None


def print_path(corrupted: List[Coordinate], path: List[Coordinate]) -> None:
    max_x = max(x for x, y in corrupted)
    max_y = max(y for x, y in corrupted)
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (x, y) in path:
                print("o", end="")
            else:
                if (x, y) in corrupted:
                    print("#", end="")
                else:
                    print(".", end="")
        print()
    print()


def find_first_blocking_corruption(
    start: Coordinate, target: Coordinate, corrupted: List[Coordinate]
) -> int:
    """Returns the index of the first corrupted tile that blocks path
    from start to target."""
    left = 1025
    right = len(corrupted) - 1
    mid = 0
    while left <= right:
        mid = (left + right) // 2
        result = find_shortest_path(start, target, corrupted[:mid])
        if result is None:
            if find_shortest_path(start, target, corrupted[: (mid - 1)]) is not None:
                return mid - 1
            right = mid - 1
        else:
            left = mid + 1


def part_1():
    coordinates = read_input(18, map_fn, False)
    start = Coordinate(0, 0)
    target = Coordinate(70, 70)
    _, score = find_shortest_path(start, target, coordinates[:1024])

    print(f"Part 1: {score}")
    assert score == 292


def part_2():
    coordinates = read_input(18, map_fn, False)
    start = Coordinate(0, 0)
    target = Coordinate(70, 70)
    index = find_first_blocking_corruption(start, target, coordinates)

    first_blocker = coordinates[index]
    print(f"Part 2: {first_blocker}")
    assert first_blocker == Coordinate(58, 44)


part_1()
part_2()
