from utils import read_multisection_input
from collections import defaultdict
from functools import cmp_to_key

RULES = None


def map_rules(lines):
    rules = []
    for line in lines.split("\n"):
        before, after = line.split("|")
        rules.append((int(before), int(after)))
    return rules


def map_updates(lines):
    updates = []
    for line in lines.split("\n"):
        updates.append([int(n) for n in line.split(",")])
    return updates


def create_rules_map(rules):
    rules_map = defaultdict(list)
    for before, after in rules:
        rules_map[before].append(after)
    return rules_map


def sort_by_rules(a, b):
    if a in RULES:
        if b in RULES[a]:
            return -1
    if b in RULES:
        if a in RULES[b]:
            return 1
    else:
        return 0


def is_in_order(update):
    s_update = sorted(update, key=cmp_to_key(sort_by_rules))
    return update == s_update


def sum_middle_pages(updates):
    total = 0
    for update in updates:
        mid = len(update) // 2
        total += update[mid]
    return total


def part_1():
    global RULES
    rules, updates = read_multisection_input(5, [map_rules, map_updates])
    RULES = create_rules_map(rules)
    correct_updates = [update for update in updates if is_in_order(update)]
    result = sum_middle_pages(correct_updates)
    print(f"Part 1: {result}")
    assert result == 7074


def part_2():
    global RULES
    rules, updates = read_multisection_input(5, [map_rules, map_updates])
    RULES = create_rules_map(rules)
    corrected_updates = [
        sorted(update, key=cmp_to_key(sort_by_rules))
        for update in updates
        if not is_in_order(update)
    ]
    result = sum_middle_pages(corrected_updates)
    print(f"Part 2: {result}")
    assert result == 4828


part_1()
part_2()
