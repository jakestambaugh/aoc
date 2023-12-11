"""
Advent of Code utilities and skeleton
"""
import argparse


def get_lines(filename):
    with open(filename, "r") as f:
        contents = "".join(line for line in f if not line.isspace())
        return contents.strip().split("\n")


def find_first_and_last(line):
    num_chars = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for char in line:
        if char in num_chars:
            first = char
            break
    for char in reversed(line):
        if char in num_chars:
            last = char
            break
    return first, last


def replace_words(line):
    char_words = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    new_line = ""
    last_safe = 0
    i = 0
    while i < len(line):
        for k, v in char_words.items():
            if k == line[i : i + len(k)]:
                new_line += line[last_safe:i] + v
                last_safe = i + len(k)
                break
        i += 1
    new_line += line[last_safe:]
    return new_line


def part1(filename):
    lines = get_lines(filename)
    total = 0
    for line in lines:
        first, last = find_first_and_last(line)
        i = int(first + last)
        total += i
    print(f"Part 1: {total}")


def part2(filename):
    lines = get_lines(filename)
    total = 0
    for line in lines:
        new_line = replace_words(line)
        first, last = find_first_and_last(new_line)
        i = int(first + last)
        total += i
        print(f"{line} -> {new_line} -> {first},{last} -> {i}")
    print(f"Part 2: {total}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code.")
    parser.add_argument(
        "-p",
        "--part",
        metavar="N",
        type=int,
        default=1,
        choices=range(1, 3),
        help="Use --part 2 to run the second problem each day",
    )
    parser.add_argument(
        "-t",
        "--test",
        dest="test",
        action="store_true",
        help="Use the input in test.txt instead of input.txt",
    )
    parser.set_defaults(test=False)
    args = vars(parser.parse_args())

    filename = "test.txt" if args["test"] else "input.txt"

    if args["part"] == 1:
        part1(filename)
    elif args["part"] == 2:
        part2(filename)
