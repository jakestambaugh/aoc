"""
Advent of Code utilities and skeleton
"""
import argparse
import time


def get_lines(filename):
    with open(filename, "r") as f:
        contents = "".join(line for line in f if not line.isspace())
        return contents.strip().split("\n")


def part1(filename):
    print(f"Part 1: {filename}")


def part2(filename):
    print(f"Part 2: {filename}")


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
    parser.add_argument(
        "-b",
        "--benchmark",
        dest="benchmark",
        action="store_true",
        help="Collect timing information from run",
    )
    parser.set_defaults(test=False)
    args = vars(parser.parse_args())

    filename = "test.txt" if args["test"] else "input.txt"

    if args["benchmark"]:
        start_time = time.perf_counter()

    if args["part"] == 1:
        part1(filename)
    elif args["part"] == 2:
        part2(filename)

    if args["benchmark"]:
        end_time = time.perf_counter()
        print(f"Runtime: {end_time - start_time:.4f} seconds")
