from time import sleep
import sys

def build_board(lines):
    return [[c for c in chars.strip()] for chars in lines]


def visible_occupied(b, r, c):
    count = 0
    for v in range(0, 9):
        ro = (v // 3) - 1
        co = (v % 3) - 1
        y = r+ro
        x = c+co
        while not ((y == r and x == c) or (y < 0 or y >= len(b)) or (x < 0 or x >= len(b[0]))):
            if b[y][x] == "#":
                count += 1
                break
            elif b[y][x] == "L":
                break
            y += ro
            x += co
    return count


def adjacent_occupied(b, r, c):
    count = 0
    for v in range(0, 9):
        ro = (v // 3) - 1
        co = (v % 3) - 1
        y = r+ro
        x = c+co
        if y == r and x == c:
            continue
        elif y < 0 or y >= len(b):
            continue
        elif x < 0 or x >= len(b[0]):
            continue
        else:
            if b[y][x] == "#":
                count += 1
    return count


def simulate(board, r, c):
    density = visible_occupied(board, r, c) 
    updated = board[r][c]
    if board[r][c] == ".":
        updated = "."
    elif board[r][c] == "#" and density >= 5:
        updated = "L"
    elif board[r][c] == "L" and density == 0:
        updated = "#"
    return updated, str(density)


def simulate_round(board):
    new_board = [[None for x in range(len(board[0]))] for y in range(len(board))]
    densities = [[None for x in range(len(board[0]))] for y in range(len(board))]
    for r in range(len(board)):
        for c in range(len(board[0])):
            new_board[r][c], densities[r][c] = simulate(board, r, c)
    return new_board, densities


def print_board(board):
    sys.stdout.write(u"\u001b[1000D") # Move left
    sys.stdout.flush()
    sys.stdout.write(u"\u001b[" + str(len(board)) + "A") # Move up
    sys.stdout.flush()
    print("\n".join(["".join(row) for row in board]))


def count_filled(board):
    flat = [item for sublist in board for item in sublist]
    count = 0
    for x in flat:
        if x == "#":
            count += 1
    return count


def main():
    pathname = "input.txt"
    with open(pathname) as f:
        content = f.readlines()
        board = build_board(content)
        i = -1
        previous = None
        while board != previous:
            previous = board
            board, densities = simulate_round(board)
            i += 1
        print("{} filled seats after {} iterations.".format(count_filled(board), i))


if __name__ == "__main__":
    main()
