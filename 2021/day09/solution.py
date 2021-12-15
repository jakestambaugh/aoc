"""
Advent of Code utilities and skeleton
"""
import argparse

def parse_grid(filename):
    with open(filename, "r") as f:
        return [ [ int(x) for x in line if not x == "\n" ] for line in f]


def is_local_minima(candidate, *neighbors):
    if candidate < min(neighbors):
        return True
    return False


def find_local_minima(grid):
    local_minima = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            neighbors = []
            if x > 0:
                neighbors.append(grid[x-1][y]) 
            if x < len(grid) - 1:
                neighbors.append(grid[x+1][y])
            if y > 0:
                neighbors.append(grid[x][y-1])
            if y < len(row) -1:
                neighbors.append(grid[x][y+1])
            candidate = grid[x][y]
            if is_local_minima(candidate, *neighbors):
                # print(f"Found {candidate} at {x},{y}: neighbors {neighbors}")
                local_minima.append(candidate)
    return local_minima


def part1(filename):
    grid = parse_grid(filename)
    low_points = find_local_minima(grid)
    risk_levels = [x + 1 for x in low_points]
    print(sum(risk_levels))

def part2(filename):
    grid = parse_grid(filename)
    # todo flood fill

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
