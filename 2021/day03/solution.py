"""
Advent of Code utilities and skeleton
"""
import argparse


def get_lines(filename):
    with open(filename, 'r') as f:
        contents = "".join(line for line in f if not line.isspace())
        return contents.strip().split("\n")


def parse_binary(line):
    """Takes a string of '0' and '1' characters and converts it to int"""
    power = 1
    total = 0
    reversed = line[::-1]
    for char in reversed:
        if char == "1":
            total += power
        power *= 2
    return total


def get_frequencies(lines):
    frequencies = [{"0":0, "1":0} for _ in lines[0]]
    for line in lines:
        for i, c in enumerate(line):
            frequencies[i][c] += 1
    return frequencies

def most_frequent(pair):
    zeroes = pair["0"]
    ones = pair["1"]
    if zeroes > ones:
        return "0"
    else:
        return "1"


def least_frequent(pair):
    zeroes = pair["0"]
    ones = pair["1"]
    if zeroes < ones:
        return "0"
    else:
        return "1"


def count_column(lines, bit_position):
    ones = 0
    zeroes = 0
    for line in lines:
        if line[bit_position] == "0":
            zeroes += 1
        elif line[bit_position] == "1":
            ones += 1
    return (ones, zeroes)


def calculate_oxygen_rating(lines: list[str], bit_position=0):
    ones, zeroes = count_column(lines, bit_position)
    target = "0" if zeroes > ones else "1"
    filtered = list(filter(lambda line: line[bit_position] == target, lines))
    if len(filtered) == 1:
        return filtered[0]
    else:
        return calculate_oxygen_rating(filtered, bit_position=(bit_position + 1))


def calculate_co2_rating(lines: list[str], bit_position=0):
    ones, zeroes = count_column(lines, bit_position)
    target = "1" if ones < zeroes else "0"
    filtered = list(filter(lambda line: line[bit_position] == target, lines))
    if len(filtered) == 1:
        return filtered[0]
    else:
        return calculate_co2_rating(filtered, bit_position=(bit_position + 1))


def part1(filename):
    lines = get_lines(filename)
    frequencies = get_frequencies(lines)
    gamma = parse_binary([most_frequent(freq) for freq in frequencies])
    epsilon = parse_binary([least_frequent(freq) for freq in frequencies])
    power = gamma * epsilon
    print(power)

def part2(filename):
    lines = get_lines(filename)
    oxygen_generator_rating = parse_binary(calculate_oxygen_rating(lines))
    co2_scrubber_rating = parse_binary(calculate_co2_rating(lines))
    life_support_rating = oxygen_generator_rating * co2_scrubber_rating
    print(life_support_rating)

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
