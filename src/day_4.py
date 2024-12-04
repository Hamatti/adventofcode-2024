from utils import read_input


def create_grid(rows):
    """Turns a list of strings into
    a dictionary where keys are the coordinates
    and values are the letters."""
    grid = {}
    for y, row in enumerate(rows):
        for x, cell in enumerate(row):
            grid[(x, y)] = cell
    return grid


def check_direction(start, direction, grid):
    """Given a starting index,
    a direction and a grid of letters, checks
    if rest of the word forms MAS in the given direction."""

    sx, sy = start
    directions = {
        "nw": (-1, -1),
        "n": (0, -1),
        "ne": (1, -1),
        "e": (1, 0),
        "se": (1, 1),
        "s": (0, 1),
        "sw": (-1, 1),
        "w": (-1, 0),
    }
    letters = ("M", "A", "S")

    for i in range(1, 4):
        new_index = (
            sx + directions[direction][0] * i,
            sy + directions[direction][1] * i,
        )
        if grid.get(new_index) != letters[i - 1]:
            return 0
    return 1


def check_for_xmas(index, grid):
    """Checks if a given index is a starting point
    for a word XMAS in any direction."""
    current = grid.get(index)
    if current != "X":
        return 0

    found = 0

    for direction in ["nw", "n", "ne", "e", "se", "s", "sw", "w"]:
        found += check_direction(index, direction, grid)

    return found


def is_part_of_cross(index, grid):
    """Checks if the given index is in the middle of
    a diagonal cross with M and S in opposite sides.

    For example:
    M.S
    .A.
    M.S

    where the index points to A
    """
    sx, sy = index

    top_left = grid.get((sx - 1, sy - 1))
    bottom_right = grid.get((sx + 1, sy + 1))

    bottom_left = grid.get((sx + 1, sy - 1))
    top_right = grid.get((sx - 1, sy + 1))

    downwards_mas = (top_left == "S" and bottom_right == "M") or (
        top_left == "M" and bottom_right == "S"
    )
    upwards_mas = (bottom_left == "S" and top_right == "M") or (
        bottom_left == "M" and top_right == "S"
    )

    if downwards_mas and upwards_mas:
        return 1
    else:
        return 0


def part_1():
    rows = read_input(4, str)
    grid = create_grid(rows)
    found = 0
    for index in grid:
        found += check_for_xmas(index, grid)

    print(f"Part 1: {found}")
    assert found == 2504


def part_2():
    rows = read_input(4, str)
    grid = create_grid(rows)
    found = 0

    for index in grid:
        if grid.get(index) == "A":
            found += is_part_of_cross(index, grid)

    print(f"Part 2: {found}")
    assert found == 1923


part_1()
part_2()
