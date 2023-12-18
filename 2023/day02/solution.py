"""
Advent of Code utilities and skeleton
"""
import argparse


def get_lines(filename):
    with open(filename, "r") as f:
        contents = "".join(line for line in f if not line.isspace())
        return contents.strip().split("\n")


def min_cubes(line):
    parts = line.split(":")
    game, rest = parts[0], parts[1]
    pulls = rest.split(";")
    r, g, b = 0, 0, 0
    for pull in pulls:
        colors = pull.split(",")
        for color in colors:
            halves = color.split(" ")
            if halves[2] == "red" and r < int(halves[1]):
                r = int(halves[1])
            elif halves[2] == "green" and g < int(halves[1]):
                g = int(halves[1])
            elif halves[2] == "blue" and b < int(halves[1]):
                b = int(halves[1])
    return (r, g, b)


def valid_color(count, color):
    if color == "red" and count > 12:
        return False
    elif color == "green" and count > 13:
        return False
    elif color == "blue" and count > 14:
        return False
    else:
        return True


def possible_game(line):
    parts = line.split(":")
    game, rest = parts[0], parts[1]
    game_num = game.split(" ")[1]
    pulls = rest.split(";")
    possible = True
    for pull in pulls:
        colors = pull.split(",")
        for color in colors:
            halves = color.split(" ")
            possible = possible and valid_color(int(halves[1]), halves[2])
    return int(game_num) if possible else 0


def part1(filename):
    lines = get_lines(filename)
    total = 0
    for line in lines:
        id = possible_game(line)
        total += id
    print(f"Part 1: {total}")


def part2(filename):
    lines = get_lines(filename)
    total = 0
    for line in lines:
        cubes = min_cubes(line)
        power = cubes[0] * cubes[1] * cubes[2]
        total += power
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
