"""
Advent of Code utilities and skeleton
"""
import argparse
import time


class RangeMap:
    def __init__(self, fromtype, totype):
        self.fromtype = fromtype
        self.totype = totype
        self.map = {}

    def insert(self, out_start, in_start, length):
        self.map[(in_start, in_start + length)] = out_start

    def get(self, key):
        found = key
        for k, v in self.map.items():
            if key >= k[0] and key < k[1]:
                found = v + (key - k[0])
        return found


def parse_file(filename):
    with open(filename, "r") as f:
        seeds = f.readline().strip().split(": ")[1]
        # skip empty line
        f.readline()
        list_of_mappings = []
        mapping = []
        for line in f:
            if line == "\n":
                list_of_mappings.append(mapping)
                mapping = []
            else:
                mapping.append(line.strip())
        list_of_mappings.append(mapping)
        return seeds, list_of_mappings


def parse_mapping_line(line):
    title = line.split(" ")[0]
    parts = title.split("-")
    fr, to = parts[0], parts[2]
    return fr, to


def build_mappings(list_of_mappings):
    mappings = {}
    for mapping in list_of_mappings:
        fr, to = parse_mapping_line(mapping[0])
        rm = RangeMap(fr, to)
        mappings[fr] = rm
        for line in mapping[1:]:
            parts = [int(p) for p in line.split(" ")]
            mappings[fr].insert(*parts)
    return mappings


def part1(filename):
    seeds, list_of_mappings = parse_file(filename)
    mappings = build_mappings(list_of_mappings)
    seeds = [int(s) for s in seeds.split(" ")]
    locations = []
    for s in seeds:
        fr = "seed"
        value = s
        while fr != "location":
            value = mappings[fr].get(value)
            fr = mappings[fr].totype
        locations.append(value)
    print(f"Part 1: {min(locations)}")


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
