from utils import read_input


def map_fn(line):
    """Map input line to a tuple of ints

    Input line is in format:
    3   4
    """
    left, right = line.split()
    return int(left), int(right)


def calculate_distance(inputs):
    """Calculate distance between two lists by calculating
    the absolute difference between the smallest items, 2nd
    smallest items etc and summing them up."""

    lefts, rights = zip(*inputs)
    lefts = sorted(lefts)
    rights = sorted(rights)

    total_distance = 0
    for left, right in zip(lefts, rights):
        distance = abs(left - right)
        total_distance += distance

    return total_distance


def calculate_similarity_scores(inputs):
    """Calculate similarity scores by multiplying each
    left item in a tuple with how many times it appears
    as the right item in the list of tuples
    """

    lefts, rights = zip(*inputs)

    total_similarity_score = 0
    for number in lefts:
        appears_in_right = rights.count(number)
        similarity_score = number * appears_in_right
        total_similarity_score += similarity_score

    return total_similarity_score


def part_1():
    inputs = read_input(1, map_fn)
    total_distance = calculate_distance(inputs)
    print(f"Part 1: {total_distance}")
    assert total_distance == 1765812


def part_2():
    inputs = read_input(1, map_fn)
    total_similarity_score = calculate_similarity_scores(inputs)
    print(f"Part 2: {total_similarity_score}")

    assert total_similarity_score == 20520794


part_1()
part_2()
