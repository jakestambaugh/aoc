"""
Advent of Code utilities and skeleton
"""
import argparse
from statistics import median


def parse_line(filename):
    with open(filename, "r") as f:
        line = f.readline()
        return [int(x) for x in line.split(",")]


def part1(filename):
    crab_positions = parse_line(filename)
    m = int(median(crab_positions))
    fuel = sum([abs(x - m) for x in crab_positions])
    print(f"location: {m}")
    print(fuel)


def calculate_fuel_to_point(i, positions):
    sum = 0
    for x in positions:
        distance = abs(i - x)
        fuel = (distance * (distance + 1)) // 2
        sum += fuel
    return sum


def calculate_fuel_spends(positions):
    fuel_totals = [0 for _ in positions]
    for i in range(len(fuel_totals)):
        fuel_totals[i] = calculate_fuel_to_point(i, positions)
    return fuel_totals


def part2(filename):
    crab_positions = parse_line(filename)
    fuel_spent_per_target = calculate_fuel_spends(crab_positions)
    print(min(fuel_spent_per_target))


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
