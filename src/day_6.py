from utils import read_input


class Token:
    EMPTY = "."
    GUARD = "^"
    OBSTACLE = "#"
    VOID = None


class Guard:
    def __init__(self, start):
        self.position = start
        self.direction = "up"

    def next_direction(self):
        match self.direction:
            case "up":
                return "right"
            case "right":
                return "down"
            case "down":
                return "left"
            case "left":
                return "up"

    def next(self, grid):
        new_coord = None
        match self.direction:
            case "up":
                new_coord = self.position[0], self.position[1] - 1
            case "down":
                new_coord = self.position[0], self.position[1] + 1
            case "left":
                new_coord = self.position[0] - 1, self.position[1]
            case "right":
                new_coord = self.position[0] + 1, self.position[1]

        potential_next = grid.get(new_coord)
        if potential_next == Token.EMPTY:
            self.position = new_coord
            return True

        if potential_next == Token.OBSTACLE:
            self.direction = self.next_direction()
            return True

        if potential_next == Token.VOID:
            return False


def make_grid(inputs):
    grid = {}
    for y, row in enumerate(inputs):
        for x, cell in enumerate(row):
            if cell == Token.GUARD:
                guard = Guard((x, y))
                cell = "."
            grid[(x, y)] = cell

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


part_1()
