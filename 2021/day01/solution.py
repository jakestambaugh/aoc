"""
Advent of Code utilities and skeleton
"""
import argparse
from collections import deque

def get_lines(filename):
    with open(filename, 'r') as f:
        contents = "".join(line for line in f if not line.isspace())
        return contents.strip().split("\n")


def part1(filename):
    lines = get_lines(filename)
    depths = iter([int(line) for line in lines])
    times_increased = 0
    prev = next(depths)
    for depth in depths:
        if prev < depth:
            times_increased += 1
        prev = depth
    print(times_increased)


def part2(filename):
    lines = get_lines(filename)
    depths = iter([int(line) for line in lines])
    times_increased = 0
    prev_window = deque([next(depths) for _ in range(3)])
    for depth in depths:
        depth_window = prev_window.copy()
        depth_window.popleft()
        depth_window.append(depth)
        if sum(prev_window) < sum(depth_window):
            times_increased += 1
        prev_window = depth_window
    print(times_increased)


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
