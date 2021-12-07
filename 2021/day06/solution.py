"""
Advent of Code utilities and skeleton
"""
import argparse
from functools import cache


def parse_file(filename):
    with open(filename, "r") as f:
        line = f.readline()
        return [int(x) for x in line.split(",")]


@cache
def fish_born_after_days(age, days):
    if days == 0:
        return 0
    if age == 0:
        return 1 + fish_born_after_days(6, days - 1) + fish_born_after_days(8, days - 1)
    return fish_born_after_days(age - 1, days - 1)


def part1(filename):
    starting_fish_ages = parse_file(filename)
    days = 80
    num_new_fish = [
        fish_born_after_days(fish_age, days) for fish_age in starting_fish_ages
    ]
    print(sum(num_new_fish) + len(starting_fish_ages))
    print(f"Cache info: {fish_born_after_days.cache_info()}")


def part2(filename):
    starting_fish_ages = parse_file(filename)
    days = 256
    num_new_fish = [
        fish_born_after_days(fish_age, days) for fish_age in starting_fish_ages
    ]
    print(sum(num_new_fish) + len(starting_fish_ages))
    print(f"Cache info: {fish_born_after_days.cache_info()}")


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
