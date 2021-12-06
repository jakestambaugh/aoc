"""
Advent of Code utilities and skeleton
"""
import argparse
from pprint import pprint
from itertools import chain


def row_winner(row, drawn):
    row = set(row)
    drawn = set(drawn)
    return row.issubset(drawn)


def col_winner(board, index, drawn):
    col = set([row[index] for row in board])
    drawn = set(drawn)
    return col.issubset(drawn)


class Board:
    def __init__(self, items):
        self.rows = items

    def __repr__(self):
        return "\n".join([" ".join([f"{x:3d}" for x in row]) for row in self.rows])

    def winner(self, drawn):
        # check rows
        for row in self.rows:
            if row_winner(row, drawn):
                return True
        # check columns
        for i in range(5):
            if col_winner(self.rows, i, drawn):
                return True
        return False


def chunker(seq, size):
    return (seq[pos : pos + size] for pos in range(0, len(seq), size))


def parse_input(filename):
    lines = []
    with open(filename, "r") as f:
        lines = f.readlines()
    drawn = lines[0]
    drawn = [int(x) for x in drawn.split(",")]
    board_lines = lines[1:]
    boards = list()
    for group in chunker(board_lines, 6):
        board = [[int(col) for col in row.split()] for row in group[1:]]
        boards.append(Board(board))
    return (drawn, boards)


def tester(filename):
    drawn, boards = parse_input(filename)
    b = boards[2]
    print()
    print(b)
    print(b.winner(drawn[0:12]))
    print(drawn[0:12])


def part1(filename):
    drawn, boards = parse_input(filename)
    for c in range(len(drawn)):
        iter_drawn = drawn[0 : (c + 1)]
        winners = [board for board in boards if board.winner(iter_drawn)]
        if len(winners) == 1:
            winner = winners[0]
            tiles = chain.from_iterable(winner.rows)
            unused = [x for x in tiles if x not in iter_drawn]
            print(sum(unused) * iter_drawn[-1])
            break


def part2(filename):
    drawn, boards = parse_input(filename)
    contenders = boards
    for c in range(len(drawn)):
        iter_drawn = drawn[0 : (c + 1)]
        prev_contenders = contenders
        contenders = [board for board in contenders if not board.winner(iter_drawn)]
        if len(prev_contenders) == 1 and len(contenders) == 0:
            loser = prev_contenders[0]
            tiles = chain.from_iterable(loser.rows)
            unused = [x for x in tiles if x not in iter_drawn]
            print(sum(unused) * iter_drawn[-1])
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code.")
    parser.add_argument(
        "-p",
        "--part",
        metavar="N",
        type=int,
        default=1,
        choices=range(1, 4),
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
    elif args["part"] == 3:
        tester(filename)
