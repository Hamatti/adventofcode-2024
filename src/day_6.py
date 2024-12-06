from utils import read_input
from collections import deque, namedtuple


class Token:
    EMPTY = "."
    GUARD = "^"
    OBSTACLE = "#"
    OUTSIDE = None


class Direction:
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


Coordinate = namedtuple("Coordinate", ["x", "y"])


class Guard:
    def __init__(self, start):
        self.position = start
        self.direction = Direction.UP
        self.direction_order = deque(
            [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        )

    def next(self, grid):
        new_coord = None
        match self.direction:
            case Direction.UP:
                new_coord = Coordinate(self.position.x, self.position.y - 1)
            case Direction.DOWN:
                new_coord = Coordinate(self.position.x, self.position.y + 1)
            case Direction.LEFT:
                new_coord = Coordinate(self.position.x - 1, self.position.y)
            case Direction.RIGHT:
                new_coord = Coordinate(self.position.x + 1, self.position.y)

        next_location = grid.get(new_coord)
        if next_location == Token.EMPTY:
            self.position = new_coord
            return True

        if next_location == Token.OBSTACLE:
            self.direction = self.direction_order[0]
            self.direction_order.rotate(-1)
            return True

        if next_location == Token.OUTSIDE:
            return False


def make_grid(inputs):
    grid = {}
    for y, row in enumerate(inputs):
        for x, cell in enumerate(row):
            if cell == Token.GUARD:
                guard = Guard(Coordinate(x, y))
                cell = Token.EMPTY
            grid[Coordinate(x, y)] = cell

    return grid, guard


def part_1():
    inputs = read_input(6, list)
    grid, guard = make_grid(inputs)
    visited = set([guard.position])

    while guard.next(grid):
        visited.add(guard.position)

    result = len(visited)
    print(f"Part 1: {result}")
    assert result == 5086
    return visited


def part_2(guard_path):
    inputs = read_input(6, list)
    grid, guard = make_grid(inputs)
    start = guard.position
    visited = set([(guard.position, Direction.UP)])
    loop_locations = 0

    for coordinate in guard_path:
        n_guard = Guard(start)
        n_grid = grid.copy()
        n_visited = visited.copy()
        if coordinate == start:
            continue
        if n_grid.get(coordinate) == Token.EMPTY:
            n_grid[coordinate] = Token.OBSTACLE

        while n_guard.next(n_grid):
            spot = (n_guard.position, n_guard.direction)
            if spot in n_visited:
                loop_locations += 1
                break
            n_visited.add(spot)

    print(f"Part 2: {loop_locations}")
    assert loop_locations == 1770


visited = part_1()
part_2(visited)
