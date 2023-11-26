"""
Advent of Code utilities and skeleton
"""
import argparse
from enum import Enum

correct_digits = {
    "0": "abcefg",
    "1": "cf",
    "2": "acdeg",
    "3": "acdfg",
    "4": "bcfd",
    "5": "abdfg",
    "6": "abdefg",
    "7": "acf",
    "8": "abcdefg",
    "9": "abcdfg",
}


class Segment(Enum):
    TOP = 1
    UPPER_LEFT = 2
    UPPER_RIGHT = 3
    CENTER = 4
    LOWER_LEFT = 5
    LOWER_RIGHT = 6
    BOTTOM = 7


def parse_entry(line):
    sections = line.split("|")
    preview = sections[0].split()
    entry = sections[1].split()
    return preview, entry


def parse_file(filename):
    with open(filename, "r") as f:
        return [parse_entry(line) for line in f]


def decoded(digit):
    if len(digit) == 2:
        return 1
    if len(digit) == 4:
        return 4
    if len(digit) == 3:
        return 7
    if len(digit) == 7:
        return 8
    else:
        return None
    return digit


def create_mapping(preview):
    # Segment Candidates
    sc = {x: set("abcdefg") for x in Segment}
    for digit in preview:
        if len(digit) == 2:
            sc[Segment.UPPER_RIGHT] = sc[Segment.UPPER_RIGHT].union(digit)
            sc[Segment.LOWER_RIGHT] = sc[Segment.LOWER_RIGHT].union(digit)
        elif len(digit) == 3:
            sc[Segment.TOP] = sc[Segment.TOP].union(digit)
            sc[Segment.UPPER_RIGHT] = sc[Segment.UPPER_RIGHT].union(digit)
            sc[Segment.LOWER_RIGHT] = sc[Segment.LOWER_RIGHT].union(digit)
        elif len(digit) == 4:
            sc[Segment.UPPER_RIGHT] = sc[Segment.UPPER_RIGHT].union(digit)
            sc[Segment.UPPER_LEFT] = sc[Segment.UPPER_LEFT].union(digit)
            sc[Segment.CENTER] = sc[Segment.CENTER].union(digit)
            sc[Segment.LOWER_RIGHT] = sc[Segment.LOWER_RIGHT].union(digit)
        elif len(digit) == 7:
            sc[Segment.TOP] = sc[Segment.TOP].union(digit)
            sc[Segment.UPPER_RIGHT] = sc[Segment.UPPER_RIGHT].union(digit)
            sc[Segment.UPPER_LEFT] = sc[Segment.UPPER_LEFT].union(digit)
            sc[Segment.CENTER] = sc[Segment.CENTER].union(digit)
            sc[Segment.LOWER_RIGHT] = sc[Segment.LOWER_RIGHT].union(digit)
            sc[Segment.LOWER_LEFT] = sc[Segment.LOWER_LEFT].union(digit)
            sc[Segment.BOTTOM] = sc[Segment.BOTTOM].union(digit)
        elif len(digit) == 5:
            # 2, 3, 5
            sc[Segment.TOP] = sc[Segment.TOP].union(digit)
            sc[Segment.CENTER] = sc[Segment.CENTER].union(digit)
            sc[Segment.BOTTOM] = sc[Segment.BOTTOM].union(digit)


def part1(filename):
    entries = parse_file(filename)
    count = 0
    for _, entry in entries:
        for digit in entry:
            if decoded(digit):
                count += 1
    print(count)


def part2(filename):
    entries = parse_file(filename)
    count = 0
    for preview, entry in entries:
        mapping = create_mapping(preview)


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
