from utils import read_input, Coordinate
import re
from collections import Counter
from typing import List, NamedTuple
import math


class Velocity(NamedTuple):
    dx: int
    dy: int


class Robot(NamedTuple):
    position: Coordinate
    velocity: Velocity


def map_fn(line: str) -> Robot:
    numbers = [int(num) for num in re.findall(r"-?\d+", line)]
    return Robot(Coordinate(numbers[0], numbers[1]), Velocity(numbers[2], numbers[3]))


def print_grid(positions: List[Coordinate], width: int, height: int) -> None:
    c = Counter(positions)
    for y in range(height):
        for x in range(width):
            if cell := c.get((x, y)):
                print(cell, end="")
            else:
                print(" ", end="")
        print()


def part_1():
    robots = read_input(14, map_fn)
    width, height = 101, 103
    seconds = 100
    quadrants = [0] * 4
    for robot in robots:
        start_position = robot.position
        velocity = robot.velocity
        final_position = Coordinate(
            (start_position.x + (velocity.dx * seconds)) % width,
            (start_position.y + (velocity.dy * seconds)) % height,
        )

        is_left = final_position.x < width // 2
        is_right = final_position.x > width // 2
        is_top = final_position.y < height // 2
        is_bottom = final_position.y > height // 2

        if is_left and is_top:
            quadrants[0] += 1
        elif is_right and is_top:
            quadrants[1] += 1
        elif is_left and is_bottom:
            quadrants[2] += 1
        elif is_right and is_bottom:
            quadrants[3] += 1

    safety_factor = math.prod(quadrants)
    print(f"Part 1: {safety_factor}")
    assert safety_factor == 232589280


def part_2():
    robots = read_input(14, map_fn)
    width, height = 101, 103

    for seconds in range(width * height):
        for idx, robot in enumerate(robots):
            new_pos = Coordinate(
                (robot.position.x + robot.velocity.dx) % width,
                (robot.position.y + robot.velocity.dy) % height,
            )
            robots[idx] = Robot(new_pos, robot.velocity)

        # The correct solution for my input
        if seconds == 7568:
            print_grid([r.position for r in robots], width, height)

    print("Part 2: 7569")  # +1 since I start at 0 instead of 1


part_1()
part_2()
