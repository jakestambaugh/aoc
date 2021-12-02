"""
Advent of Code utilities and skeleton
"""
import argparse


def get_lines(filename):
    with open(filename, 'r') as f:
        contents = "".join(line for line in f if not line.isspace())
        return contents.strip().split("\n")


def parse_dir_amount(line):
    split = line.split()
    return (split[0], int(split[1]))


def part1(filename):
    lines = get_lines(filename)
    dir_amount_pairs = [parse_dir_amount(l) for l in lines]
    horizontal = 0
    depth = 0
    for pair in dir_amount_pairs:
        match pair:
            case ("forward", x):
                horizontal += x
            case ("down", x):
                depth += x
            case ("up", x):
                depth -= x
    answer = horizontal * depth
    print(answer)


def part2(filename):
    lines = get_lines(filename)
    dir_amount_pairs = [parse_dir_amount(l) for l in lines]
    horizontal = 0
    depth = 0
    aim = 0
    for pair in dir_amount_pairs:
        match pair:
            case ("forward", x):
                horizontal += x
                depth += (aim * x)
            case ("down", x):
                aim += x
            case ("up", x):
                aim -= x
    answer = horizontal * depth
    print(answer)


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
