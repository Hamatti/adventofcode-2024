from utils import read_multisection_input
from typing import Tuple

Registers = dict[str, int]
NewPointer = int | None
Output = int | None
ReturnValue = Tuple[Registers, NewPointer, Output]


def adv(registers: Registers, operand: int) -> ReturnValue:
    numerator = registers["A"]
    value = combos[operand]
    if operand > 3:
        value = registers[value]
    denominator = 2**value
    registers["A"] = int(numerator / denominator)
    return registers, None, None


def bxl(registers: Registers, operand: int) -> ReturnValue:
    registers["B"] = registers["B"] ^ operand
    return registers, None, None


def bst(registers: Registers, operand: int) -> ReturnValue:
    value = combos[operand]
    if operand > 3:
        value = registers[value]
    registers["B"] = value % 8
    return registers, None, None


def jnz(registers: Registers, operand: int) -> ReturnValue:
    jump_to = None
    if registers["A"] != 0:
        jump_to = operand
    return registers, jump_to, None


def bxc(registers: Registers, operand: int) -> ReturnValue:
    registers["B"] = registers["B"] ^ registers["C"]
    return registers, None, None


def out(registers: Registers, operand: int) -> ReturnValue:
    value = combos[operand]
    if operand > 3:
        value = registers[value]
    return registers, None, value % 8


def bdv(registers: Registers, operand: int) -> ReturnValue:
    numerator = registers["A"]
    value = combos[operand]
    if operand > 3:
        value = registers[value]
    denominator = 2**value

    registers["B"] = int(numerator / denominator)
    return registers, None, None


def cdv(registers: Registers, operand: int) -> ReturnValue:
    numerator = registers["A"]
    value = combos[operand]
    if operand > 3:
        value = registers[value]
    denominator = 2**value
    registers["C"] = int(numerator / denominator)

    return registers, None, None


opcodes = {0: adv, 1: bxl, 2: bst, 3: jnz, 4: bxc, 5: out, 6: bdv, 7: cdv}

combos = {0: 0, 1: 1, 2: 2, 3: 3, 4: "A", 5: "B", 6: "C"}


def process(program, registers):
    pointer = 0
    prints = []
    while pointer < len(program):
        opcode = program[pointer]
        operand = program[pointer + 1]

        func = opcodes[opcode]
        registers, pointer_movement, output = func(registers, operand)
        if output is not None:
            prints.append(output)
        if pointer_movement is not None:
            pointer = pointer_movement
        else:
            pointer = pointer + 2

    return prints


def process_2(program, registers):
    pointer = 0
    prints = []
    while pointer < len(program):
        opcode = program[pointer]
        operand = program[pointer + 1]

        func = opcodes[opcode]
        registers, pointer_movement, output = func(registers, operand)
        if output is not None:
            prints.append(output)
        if pointer_movement is not None:
            pointer = pointer_movement
        else:
            pointer = pointer + 2

        if prints != program[: len(prints)]:
            return []

    return prints


def process_simplified(A):
    output = []
    while A != 0:
        a = (A % 8) ^ 1
        b = a ^ 5
        c = A // (2**a)
        res = (b ^ c) % 8
        output.append(res)
        A = A // 8
    return output


def map_registers(section):
    lines = section.split("\n")
    a = int(lines[0].split(": ")[1])
    b = int(lines[1].split(": ")[1])
    c = int(lines[2].split(": ")[1])

    return {"A": a, "B": b, "C": c}


def map_program(section):
    codes = section.split(": ")[1]
    return [int(code) for code in codes.split(",")]


def part_1():
    registers, program = read_multisection_input(17, [map_registers, map_program])
    # output = process(program, registers)
    output = process_simplified(registers["A"])
    output = ",".join([str(o) for o in output])

    print(f"Part 1: {output}")
    assert output == "5,0,3,5,7,6,1,5,4"


def part_2():
    registers, program = read_multisection_input(17, [map_registers, map_program])
    output = []
    a = 48382068
    # a = 0
    b = registers["B"]
    c = registers["C"]
    while output != program:
        print(a)
        registers["A"] = a
        output = process_simplified(a)
        a += 1
    print(f"Part 2: {a-1}")


# part_1()
part_2()