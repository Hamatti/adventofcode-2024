from utils import read_input
from collections import namedtuple

Coordinate = namedtuple("Coordinate", ["x", "y"])


def create_grid(inputs):
    grid = {}
    for y, row in enumerate(inputs):
        for x, cell in enumerate(row):
            grid[Coordinate(x, y)] = cell
    return grid


def get_neighbours(pos):
    return (
        Coordinate(pos.x + 1, pos.y),
        Coordinate(pos.x - 1, pos.y),
        Coordinate(pos.x, pos.y + 1),
        Coordinate(pos.x, pos.y - 1),
    )


def find_plot(pos, grid, visited):
    visited.add(pos)
    new_neighbours = [
        n
        for n in get_neighbours(pos)
        if n not in visited and grid.get(n) == grid.get(pos)
    ]
    if not new_neighbours:
        return visited
    for neighbour in new_neighbours:
        visited.update(find_plot(neighbour, grid, visited))
    return visited


def find_perimeter(position, grid):
    perimeter = 0
    value = grid.get(position)
    for neighbour in get_neighbours(position):
        if grid.get(neighbour) != value:
            perimeter += 1
    return perimeter


def find_plots(grid):
    plots = []
    processed = set()
    for position in grid:
        if position in processed:
            continue
        plot = find_plot(position, grid, set())
        processed.update(plot)
        plots.append(plot)
    return plots


def is_inside_corner(pos1, pos2, area):
    return pos1 in area and pos2 in area


def is_outside_corner(pos1, pos2, area):
    return not (pos1 in area or pos2 in area)


def is_not_double_corner(pos1, pos2, other_plots, grid):
    if grid.get(pos1) is not None and grid.get(pos2) is not None:
        for other in other_plots:
            if pos1 in other and pos2 not in other:
                return False
            if pos1 not in other and pos2 in other:
                return False
    return True


def count_corners(pos, area, grid, other_plots, rev=False):
    left = Coordinate(pos.x - 1, pos.y)
    right = Coordinate(pos.x + 1, pos.y)
    up = Coordinate(pos.x, pos.y - 1)
    down = Coordinate(pos.x, pos.y + 1)

    corners = 0
    if rev:
        if is_inside_corner(left, up, area):
            corners += 1
        if is_inside_corner(left, down, area):
            corners += 1
        if is_inside_corner(right, up, area):
            corners += 1
        if is_inside_corner(right, down, area):
            corners += 1
    else:
        if is_outside_corner(left, up, area) and is_not_double_corner(
            left, up, other_plots, grid
        ):
            corners += 1
        if is_outside_corner(left, down, area) and is_not_double_corner(
            left, down, other_plots, grid
        ):
            corners += 1
        if is_outside_corner(right, up, area) and is_not_double_corner(
            right, up, other_plots, grid
        ):
            corners += 1
        if is_outside_corner(right, down, area) and is_not_double_corner(
            right, down, other_plots, grid
        ):
            corners += 1

    return corners


def count_sides(area):
    xs = [x for x, y in area]
    ys = [y for x, y in area]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    grid = {}
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in area:
                grid[Coordinate(x, y)] = "x"
            else:
                grid[Coordinate(x, y)] = "."

    other_plots = [sub_area for sub_area in find_plots(grid) if sub_area != area]

    sides = 0

    # Outside sides
    for pos in area:
        sides += count_corners(pos, area, grid, other_plots)

    # Inside sides
    for other in other_plots:
        for pos in other:
            sides += count_corners(pos, area, grid, [], rev=True)

    return sides


def part_1():
    inputs = read_input(12, str)
    grid = create_grid(inputs)
    plots = find_plots(grid)

    cost = 0
    for plot in plots:
        area = len(plot)
        perimeter = sum(find_perimeter(pos, grid) for pos in plot)
        cost += area * perimeter

    print(f"Part 1: {cost}")
    assert cost == 1546338


def part_2():
    inputs = read_input(12, str)
    grid = create_grid(inputs)
    plots = find_plots(grid)

    cost = 0
    for area in plots:
        sides = count_sides(area)
        cost += sides * len(area)

    print(f"Part 2: {cost}")
    assert cost == 978590


part_1()
part_2()
