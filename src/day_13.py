import re
from collections import namedtuple

from utils import read_multisection_input

re_button = re.compile(r"Button (?P<button>[AB]): X\+(?P<x>\d+), Y\+(?P<y>\d+)")
re_prize = re.compile(r"Prize: X=(?P<x>\d+), Y=(?P<y>\d+)")

Button = namedtuple("Button", ["name", "x", "y", "cost"])
Prize = namedtuple("Prize", ["x", "y"])
Machine = namedtuple("Machine", ["A", "B", "prize"])
Play = namedtuple("Play", ["x", "y", "cost"])


def map_fn(section: str) -> Machine:
    lines = section.split("\n")
    a_button = re.match(re_button, lines[0]).groupdict()
    a_button = Button(a_button["button"], int(a_button["x"]), int(a_button["y"]), 3)

    b_button = re.match(re_button, lines[1])
    b_button = Button(b_button["button"], int(b_button["x"]), int(b_button["y"]), 1)

    prize = re.match(re_prize, lines[2].strip()).groups()
    prize = Prize(int(prize[0]), int(prize[1]))

    return Machine(a_button, b_button, prize)


def calculate_cost(machine: Machine) -> int:
    """Calculates the cost of finding the prize for a machine
    or 0 if no solution is found in 100 presses for each button.

    :param machine Machine for which to calculate the cost

    :returns cost of finding the prize
    """

    if 100 * machine.A.x + 100 * machine.B.x < machine.prize.x:
        return 0
    if 100 * machine.A.y + 100 * machine.B.y < machine.prize.y:
        return 0
    for a_presses in range(101):
        for b_presses in range(101):
            x = a_presses * machine.A.x + b_presses * machine.B.x
            y = a_presses * machine.A.y + b_presses * machine.B.y
            if (x, y) == machine.prize:
                return machine.A.cost * a_presses + machine.B.cost * b_presses

    return 0


def find_cheapest_win(machine: Machine) -> int:
    """Solution by lamperi: https://github.com/lamperi/aoc/blob/main/2024/13/solve.py"""
    a_presses = (machine.A.x * machine.prize.y - machine.A.y * machine.prize.x) / (
        machine.A.x * machine.B.y - machine.A.y * machine.B.x
    )
    b_presses = (machine.prize.x - a_presses * machine.B.x) / machine.A.x
    if int(a_presses) == a_presses and int(b_presses) == b_presses:
        return int(a_presses) + 3 * int(b_presses)

    return 0


def find_cheapest_win_sympy(machine: Machine) -> int:
    """Solution adapted from Wouter's. Requires sympy!"""
    import sympy

    # Define unknowns
    a_presses, b_presses = sympy.symbols("a_presses b_presses", integer=True)

    # Define equations
    equations = [
        a_presses * machine.A.x + b_presses * machine.B.x - machine.prize.x,
        a_presses * machine.A.y + b_presses * machine.B.y - machine.prize.y,
    ]

    # Solve unknowns
    solution = sympy.solve(equations)

    # If there is a solution, calculate the cost
    if solution:
        return (
            machine.A.cost * solution[a_presses] + machine.B.cost * solution[b_presses]
        )

    return 0


def part_1():
    machines = read_multisection_input(13, [map_fn])

    cost = sum(calculate_cost(machine) for machine in machines)

    print(f"Part 1: {cost}")
    assert cost == 31552


def part_2():
    machines = read_multisection_input(13, [map_fn])

    cost = 0
    for machine in machines:
        machine = Machine(
            machine.A,
            machine.B,
            Prize(
                machine.prize.x + 10_000_000_000_000,
                machine.prize.y + 10_000_000_000_000,
            ),
        )

        cost += find_cheapest_win(machine)

    print(f"Part 2: {cost}")
    assert cost == 95273925552482


part_1()
part_2()
