"""
Advent of Code utilities and skeleton
"""
import argparse
from dataclasses import dataclass
from itertools import chain
from collections import defaultdict


@dataclass(eq=True, frozen=True)
class Coordinate:
    x: int
    y: int


@dataclass
class Vent:
    start: Coordinate
    end: Coordinate

    def is_horizontal(self):
        return self.start.x == self.end.x

    def is_vertical(self):
        return self.start.y == self.end.y

    def is_diagonal(self):
        delta_x = abs(self.start.x - self.end.x)
        delta_y = abs(self.start.y - self.end.y)
        return delta_x == delta_y

    def positions(self):
        if self.is_horizontal():
            same_x = self.start.x
            lower = min(self.start.y, self.end.y)
            higher = max(self.start.y, self.end.y) + 1
            return [Coordinate(same_x, y) for y in range(lower, higher)]
        elif self.is_vertical():
            same_y = self.start.y
            lower = min(self.start.x, self.end.x)
            higher = max(self.start.x, self.end.x) + 1
            return [Coordinate(x, same_y) for x in range(lower, higher)]
        elif self.is_diagonal():
            x_direction = 1 if self.start.x < self.end.x else -1
            y_direction = 1 if self.start.y < self.end.y else -1
            x_list = [
                x for x in range(self.start.x, self.end.x + x_direction, x_direction)
            ]
            y_list = [
                y for y in range(self.start.y, self.end.y + y_direction, y_direction)
            ]
            return [Coordinate(x, y) for x, y in zip(x_list, y_list)]
        else:
            return []


def parse_pair(pair: str):
    x, y = tuple(pair.split(","))
    return Coordinate(int(x), int(y))


def parse_line(line: str):
    chunks = line.split()
    start = chunks[0]
    end = chunks[2]
    start = parse_pair(start)
    end = parse_pair(end)
    return Vent(start, end)


def parse_file(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        vents = [parse_line(line) for line in lines]
        return vents


def part1(filename):
    vents: list[Vent] = parse_file(filename)
    tiles = chain.from_iterable([[p for p in vent.positions()] for vent in vents])
    overlaps = defaultdict(int)
    for tile in tiles:
        overlaps[tile] += 1
    num_overlaps = 0
    for k, v in overlaps.items():
        if v > 1:
            num_overlaps += 1
    print(num_overlaps)


def part2(filename):
    vents: list[Vent] = parse_file(filename)
    tiles = chain.from_iterable([[p for p in vent.positions()] for vent in vents])
    overlaps = defaultdict(int)
    for tile in tiles:
        overlaps[tile] += 1
    num_overlaps = 0
    for k, v in overlaps.items():
        if v > 1:
            num_overlaps += 1
    print(num_overlaps)


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
