from utils import read_multisection_input, create_grid, Coordinate
from typing import Tuple, NamedTuple, Literal


class Delta(NamedTuple):
    dx: int
    dy: int


MapData = list[str]
Grid = dict[Coordinate, str]
Direction = Literal["^", ">", "<", "v"]

directions = {
    "^": Delta(0, -1),
    ">": Delta(1, 0),
    "v": Delta(0, 1),
    "<": Delta(-1, 0),
}


def print_grid(grid: Grid, robot: Coordinate) -> None:
    """Prints a sparse grid, replacing missing items with '.'
    and the robot position with '@'."""
    max_x = max(x for x, y in grid)
    max_y = max(y for x, y in grid)
    index_row = "".join([str(x) for x in list(range(0, max_x + 1))])
    print(" ", index_row)
    for y in range(max_y + 1):
        print(y, end=" ")
        for x in range(max_x + 1):
            if robot == (x, y):
                print("@", end="")
            else:
                print(grid.get((x, y), "."), end="")
        print()
    print()


## Part 1 helpers


def move(
    position: Coordinate,
    direction: Literal["^", ">", "<", "v"],
    grid: Grid,
) -> Tuple[Coordinate, Grid]:
    delta = directions[direction]
    next_position = Coordinate(position.x + delta.dx, position.y + delta.dy)
    next_spot = grid.get(next_position, None)

    if next_spot is None:
        return next_position, grid
    elif next_spot == "#":
        return position, grid

    elif next_spot == "O":
        to_move = [next_position]
        next_next_position = Coordinate(
            next_position.x + delta.dx, next_position.y + delta.dy
        )
        next_spot = grid.get(next_next_position, None)

        while next_spot == "O":
            to_move.append(next_next_position)
            next_next_position = Coordinate(
                next_next_position.x + delta.dx, next_next_position.y + delta.dy
            )
            next_spot = grid.get(next_next_position, None)

        if next_spot == "#":
            return position, grid

        for coord in to_move[::-1]:
            n = Coordinate(coord.x + delta.dx, coord.y + delta.dy)
            grid[n] = "O"
            del grid[coord]

        position = next_position

    return position, grid


## Part 2 helpers


def create_expanded_grid(data: MapData) -> Tuple[Grid, Coordinate]:
    """Creates a grid based on the expansion rules:

    1. . -> ..
    2. # -> ##
    3. O -> []
    4. @ -> @.

    :returns Grid
    """
    grid = {}
    start_position = None
    for y, row in enumerate(data):
        x = 0
        for _, cell in enumerate(row):
            if cell == "#":
                grid[Coordinate(x, y)] = cell
                grid[Coordinate(x + 1, y)] = cell
            elif cell == "O":
                grid[Coordinate(x, y)] = "["
                grid[Coordinate(x + 1, y)] = "]"
            elif cell == "@":
                start_position = Coordinate(x, y)
            x += 2
    return grid, start_position


def can_push_up_or_down(position: Coordinate, direction: Direction, grid: Grid) -> bool:
    """Determines recursively if a stack of [] boxes can be moved to given up/down direction"""
    delta = directions[direction]
    above_or_below = grid.get((position.x, position.y + delta.dy))

    if above_or_below is None:
        return True

    coordinates: list[Coordinate] = []

    if above_or_below == "[":
        coordinates.append(Coordinate(position.x, position.y + delta.dy))
        coordinates.append(Coordinate(position.x + 1, position.y + delta.dy))
    elif above_or_below == "]":
        coordinates.append(Coordinate(position.x, position.y + delta.dy))
        coordinates.append(Coordinate(position.x - 1, position.y + delta.dy))
    elif above_or_below == "#":
        return False

    return all(
        can_push_up_or_down(coordinate, direction, grid) for coordinate in coordinates
    )


def get_coordinates_for_vertical_push(
    direction: Direction,
    grid: Grid,
    coordinates: set[Coordinate],
) -> list[Coordinate]:
    delta = directions[direction]

    # If we have coordinates and all of the spots
    # above or below them are empty, return all current coordinates
    if coordinates and all(
        grid.get((c.x, c.y + delta.dy)) is None for c in coordinates
    ):
        return coordinates

    # Find the next row to check
    next_row = set()
    # For every coordinate in the previous row
    for coord in coordinates:
        above_or_below = grid.get((coord.x, coord.y + delta.dy))
        # If left side of the box, add it and its right neighbour
        if above_or_below == "[":
            next_row.add(Coordinate(coord.x, coord.y + delta.dy))
            next_row.add(Coordinate(coord.x + 1, coord.y + delta.dy))
        # If right side of the box, add it and its left neighbour
        elif above_or_below == "]":
            next_row.add(Coordinate(coord.x, coord.y + delta.dy))
            next_row.add(Coordinate(coord.x - 1, coord.y + delta.dy))

    # Recusively go through every position
    return coordinates | get_coordinates_for_vertical_push(direction, grid, next_row)


def push_horizontally(position: Coordinate, direction: Direction, grid: Grid):
    delta = directions[direction]
    next_position = Coordinate(position.x + delta.dx, position.y + delta.dy)
    next_spot = grid.get(next_position, None)
    x = next_position.x
    # Go to the end of a line of boxes
    while next_spot in "[]":
        next_spot = grid.get(Coordinate(x + delta.dx, next_position.y), ".")
        x += delta.dx
    # If there's a wall at the end, move nothing
    if next_spot == "#":
        return position, grid
    # If there's an empty spot
    if next_spot == ".":
        # Walk back from the empty spot
        while x != next_position.x:
            # Replace spot with its neighbour
            grid[Coordinate(x, next_position.y)] = grid[
                Coordinate(x - delta.dx, next_position.y)
            ]
            x -= delta.dx
        # Remove the first moved item so we don't duplicate
        del grid[next_position]
        return next_position, grid


def push_vertically(position: Coordinate, direction: Direction, grid: Grid):
    delta = directions[direction]
    # Check if we can push the full stack
    if not can_push_up_or_down(position, direction, grid):
        return position, grid

    # Find coordinates for each item to be pushed
    to_move = get_coordinates_for_vertical_push(direction, grid, set([position])) - set(
        [position]
    )  # Remove starting position as that gets moved separately

    # Sort them by y axis so we're always moving from the end first
    reverse = not (direction == "^")
    to_move = sorted(to_move, key=lambda x: x.y, reverse=reverse)

    for coordinate in to_move:
        # Move each item to their next position
        grid[Coordinate(coordinate.x, coordinate.y + delta.dy)] = grid[coordinate]
        # Delete moved item
        del grid[coordinate]

    # Return robot's new position which is one up or down from starting, and the grid.
    return Coordinate(position.x, position.y + delta.dy), grid


def move_expanded(
    position: Coordinate,
    direction: Direction,
    grid: Grid,
) -> Tuple[Coordinate, Grid]:
    delta = directions[direction]
    next_position = Coordinate(position.x + delta.dx, position.y + delta.dy)
    next_spot = grid.get(next_position, None)

    if next_spot is None:
        return next_position, grid
    elif next_spot == "#":
        return position, grid
    elif next_spot in "[]":
        if direction in "<>":
            return push_horizontally(position, direction, grid)
        if direction in "^v":
            return push_vertically(position, direction, grid)


def part_1():
    map_data, movement_data = read_multisection_input(15, [str, str])
    grid = create_grid(map_data.split("\n"), predicate=lambda x: x != ".")

    position = [key for key, value in grid.items() if value == "@"][0]
    del grid[position]

    movements = "".join(movement_data.split("\n"))
    for movement in movements:
        position, grid = move(position, movement, grid)

    gps = 0
    for coord, value in grid.items():
        if value == "O":
            gps += coord.y * 100 + coord.x
    print(f"Part 1: {gps}")
    assert gps == 1413675


def part_2():
    map_data, movement_data = read_multisection_input(15, [str, str])
    movements = "".join(movement_data.split("\n"))

    grid, position = create_expanded_grid(map_data.split("\n"))
    for movement in movements:
        position, grid = move_expanded(position, movement, grid)

    gps = 0
    for coord, value in grid.items():
        if value == "[":
            gps += coord.y * 100 + coord.x
    print(f"Part 2: {gps}")
    assert gps == 1399772


if __name__ == "__main__":
    part_1()
    part_2()
