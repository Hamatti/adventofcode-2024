import os
import sys
from itertools import cycle
from collections import namedtuple
from typing import List, Callable

Coordinate = namedtuple("Coordinate", ["x", "y"])


def read_input[T](
    day: int, map_fn: Callable[[str], T] = str, example: bool = False
) -> List[T]:
    """
    Read puzzle input for file `../inputs/day_{day}.txt'
    and apply map_fn function to each line.

    If `example` is set to True, read file `../inputs/day_{day}_example.txt`
    instead

    :param day Which day's puzzle input to read
    :param map_fn Cast each line into new type
    :param example Read example input?

    :returns Day's input processed into the desired format
    """

    try:
        if example:
            filename = f"day_{day}_example.txt"
        else:
            filename = f"day_{day}.txt"
        with open(os.path.join("..", "inputs", filename)) as input_file:
            return [map_fn(line.strip()) for line in input_file]
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)


def read_multisection_input[T](
    day: int, map_fns: List[Callable[[str], T]] = None, example: bool = False
) -> List[T]:
    """
    Read multisection puzzle input for file `/inputs/day_{day}.txt'
    and apply transformer function to each section.

    If `example` is set to True, read file `/inputs/day_{day}_example.txt`
    instead

    :param day Which day's puzzle input to read
    :param map_fns Map function per section (cycled)
    :param example Read example input?
    """

    try:
        if example:
            filename = f"day_{day}_example.txt"
        else:
            filename = f"day_{day}.txt"
        with open(os.path.join("..", "inputs", filename)) as input_file:
            sections = input_file.read().split("\n\n")
            return [
                transformer(section)
                for section, transformer in zip(sections, cycle(map_fns))
            ]
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)


def create_grid(
    inputs: List[List[str]],
    map_fn: Callable[[str], any] = lambda x: x,
    predicate: Callable[[str], bool] = lambda x: True,
):
    """
    Turns a 2D list of lists into a dictionary with (x, y)
    coordinates as keys.

    :param map_fn Maps input value into a new value.
    :param predicate Filter function for which values to keep

    :returns Dictionary with coordinate tuples as keys and converted values as values

    >>> create_grid([['1','2'], ['4','5']])
    {Coordinate(x=0, y=0): '1', Coordinate(x=1, y=0): '2', Coordinate(x=0, y=1): '4', Coordinate(x=1, y=1): '5'}
    >>> create_grid([['10', '20'], ['30', '40']], map_fn=int)
    {Coordinate(x=0, y=0): 10, Coordinate(x=1, y=0): 20, Coordinate(x=0, y=1): 30, Coordinate(x=1, y=1): 40}
    >>> create_grid([['.', '20'], ['30', '.']], map_fn=int, predicate=lambda x: x != '.')
    {Coordinate(x=1, y=0): 20, Coordinate(x=0, y=1): 30}

    """
    grid = {}
    for y, row in enumerate(inputs):
        for x, cell in enumerate(row):
            if predicate(cell):
                grid[Coordinate(x, y)] = map_fn(cell)
    return grid


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
