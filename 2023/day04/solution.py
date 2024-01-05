"""
Advent of Code utilities and skeleton
"""
import argparse
import time


def get_lines(filename):
    with open(filename, "r") as f:
        contents = "".join(line for line in f if not line.isspace())
        return contents.strip().split("\n")


def parse_line(line):
    line = " ".join(line.split())
    parts = line.strip().split(" ")
    card = int(parts[1].split(":")[0])
    elements = parts[2:]
    bar = elements.index("|")
    return (
        card,
        (
            [int(x) for x in elements[:bar]],
            [int(x) for x in elements[bar + 1 :]],
        ),
    )


def calculate_score(line):
    _card, (mine, winners) = parse_line(line)
    winners = set(winners)
    points = 0
    for i in mine:
        if i in winners:
            if points == 0:
                points = 1
            else:
                points = 2 * points
    return points


def count_points(mine, winners):
    points = 0
    winners = set(winners)
    for i in mine:
        if i in winners:
            points += 1
    return points


def calculate_score_for_line(cards, line):
    mine, winners = cards[line]
    points = count_points(mine, winners)
    return 1 + sum(
        calculate_score_for_line(cards, i) for i in range(line + 1, line + points + 1)
    )


def calculate_score_set(cards):
    return sum(calculate_score_for_line(cards, i) for i in range(1, len(cards) + 1))


def part1(filename):
    lines = get_lines(filename)
    scores = [calculate_score(line) for line in lines]
    total = sum(scores)
    print(f"Part 1: {total}")


def part2(filename):
    lines = get_lines(filename)
    cards = {
        card: (mine, winners)
        for card, (mine, winners) in [parse_line(line) for line in lines]
    }
    scores = calculate_score_set(cards)
    print(f"Part 2: {scores}")


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
