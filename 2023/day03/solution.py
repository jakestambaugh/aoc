"""
Advent of Code utilities and skeleton
"""
import argparse
from collections import defaultdict


def flatten_list(xss):
    return [x for xs in xss for x in xs]


def get_lines(filename):
    with open(filename, "r") as f:
        contents = "".join(line for line in f if not line.isspace())
        return contents.strip().split("\n")


def build_grid(lines):
    grid = []
    for line in lines:
        grid.append([*line])
    return grid


def flood_number(grid, i, j):
    # look top left, then top center, then top right
    numbers = []
    builder = []
    if i > 0 and j > 0 and grid[i - 1][j - 1].isdigit():
        k = j - 1
        while k >= 0 and grid[i - 1][k].isdigit():
            builder.insert(0, grid[i - 1][k])
            k -= 1
    # either extend the top left number, start a new builder or
    # save the existing builder
    if i > 0 and grid[i - 1][j].isdigit():
        builder.append(grid[i - 1][j])
    elif builder:
        numbers.append(int("".join(builder)))
        builder = []
    # either extend the existing number or save it
    if i > 0 and j < len(grid) - 1 and grid[i - 1][j + 1].isdigit():
        k = j + 1
        while k < len(grid) and grid[i - 1][k].isdigit():
            builder.append(grid[i - 1][k])
            k += 1
    if builder:
        numbers.append(int("".join(builder)))
        builder = []
    # Look left
    if j > 0 and grid[i][j - 1].isdigit():
        k = j - 1
        while k >= 0 and grid[i][k].isdigit():
            builder.insert(0, grid[i][k])
            k -= 1
    if builder:
        numbers.append(int("".join(builder)))
        builder = []
    # Look right
    if j < len(grid) - 1 and grid[i][j + 1].isdigit():
        k = j + 1
        while k < len(grid) and grid[i][k].isdigit():
            builder.append(grid[i][k])
            k += 1
    if builder:
        numbers.append(int("".join(builder)))
        builder = []
    # Look bottom left
    if i < len(grid) - 1 and j > 0 and grid[i + 1][j - 1].isdigit():
        k = j - 1
        while k >= 0 and grid[i + 1][k].isdigit():
            builder.insert(0, grid[i + 1][k])
            k -= 1
    # Look bottom center
    if i < len(grid) - 1 and grid[i + 1][j].isdigit():
        builder.append(grid[i + 1][j])
    # If bottom left added to the builder but bottom center didn't, save the number
    # so that we can start building a new number in bottom right
    elif builder:
        numbers.append(int("".join(builder)))
        builder = []
    # look bottom right
    if i < len(grid) - 1 and j < len(grid) - 1 and grid[i + 1][j + 1].isdigit():
        k = j + 1
        while k < len(grid) and grid[i + 1][k].isdigit():
            builder.append(grid[i + 1][k])
            k += 1
    # Build whatever's left in the builder
    if builder:
        numbers.append(int("".join(builder)))
    return numbers


def find_symbols(grid):
    symbol_positions = defaultdict(list)
    for i, row in enumerate(grid):
        for j, item in enumerate(row):
            if not item.isdigit() and item != ".":
                symbol_positions[item].append((i, j))
    return symbol_positions


def calculate_ratios(grid, gears):
    ratios = []
    for gear in gears:
        detected_numbers = flood_number(grid, *gear)
        if len(detected_numbers) == 2:
            ratio = detected_numbers[0] * detected_numbers[1]
            ratios.append(ratio)
    return ratios


def part1(filename):
    lines = get_lines(filename)
    grid = build_grid(lines)
    symbol_positions = find_symbols(grid)
    detected_numbers = [
        flood_number(grid, *pos) for pos in flatten_list(symbol_positions.values())
    ]
    total = sum(flatten_list(detected_numbers))
    print(f"Part 1: {total}")


def part2(filename):
    lines = get_lines(filename)
    grid = build_grid(lines)
    symbol_positions = find_symbols(grid)
    gears = symbol_positions["*"]
    ratios = calculate_ratios(grid, gears)
    total = sum(ratios)
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
