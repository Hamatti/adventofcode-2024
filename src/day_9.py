from utils import read_input


def map_fn(line):
    # Filesystem is the state of disk
    filesystem = {}

    file_lengths = {}
    file_start_indices = {}
    empty_space_lengths = []

    file_id = 0
    fs_pointer = 0

    for idx, value in enumerate(line):
        value = int(value)
        # Is file
        if idx % 2 == 0:
            file_start_indices[file_id] = fs_pointer
            file_lengths[file_id] = value
            for _ in range(value):
                filesystem[fs_pointer] = file_id
                fs_pointer += 1
            file_id += 1
        # Is empty space
        else:
            empty_space_lengths.append((fs_pointer, value))
            fs_pointer += value

    return filesystem, (file_lengths, empty_space_lengths, file_start_indices)


def part_1():
    fs, _ = read_input(9, map_fn)[0]
    max_idx = max(fs)

    for i in range(max_idx + 1):
        if fs.get(i) is not None:
            # It's a file in a correct spot, do nothing
            continue
        while fs.get(max_idx) is None:
            # Find the right-most file index
            max_idx -= 1
        if i >= max_idx:
            # Don't move files to the right
            break

        # Move from end to the current empty spot
        fs[i] = fs[max_idx]

        # Delete old file block pointer
        del fs[max_idx]
        max_idx -= 1

    checksum = sum(index * file_id for index, file_id in fs.items())

    print(f"Part 1: {checksum}")
    assert checksum == 6288707484810


def find_empty_slot(empty_spaces, length):
    for index, (fs_index, empty_length) in enumerate(empty_spaces):
        if empty_length >= length:
            return (index, (fs_index))
    return None


def part_2():
    fs, (file_lengths, empty_lengths, file_start_indices) = read_input(9, map_fn)[0]

    for file_id in reversed(file_lengths):
        length = file_lengths[file_id]

        empty_slot = find_empty_slot(empty_lengths, length)
        if empty_slot is None:
            continue

        empty_lengths_idx, empty_fs_idx = empty_slot

        start_idx = file_start_indices[file_id]
        if empty_fs_idx > start_idx:
            continue

        for k in range(length):
            fs[empty_fs_idx + k] = fs[start_idx + k]
            del fs[start_idx + k]

        empty_lengths[empty_lengths_idx] = (
            empty_fs_idx + length,
            empty_lengths[empty_lengths_idx][1] - length,
        )

    checksum = sum(index * file_id for index, file_id in fs.items())

    print(f"Part 2: {checksum}")

    assert checksum == 6311837662089


part_1()
part_2()
