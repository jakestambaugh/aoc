from collections import deque


def find_first_invalid(data, ws):
    window = deque(data[:ws])
    for x in data[ws:]:
        valid = False
        for i in window:
            for j in window:
                if x == i + j and i != j:
                    valid = True
        if valid:
            window.popleft()
            window.append(x)
            assert(len(window) == ws)
        if not valid:
            return x


def main():
    pathname = "input.txt"
    window_size = 25
    with open(pathname) as f:
        content = f.readlines()
        data = [int(line) for line in content]
        outlier = find_first_invalid(data, window_size)
        print("{} is the first value that can't be made of a sum in the window".format(outlier))


if __name__ == "__main__":
    main()
