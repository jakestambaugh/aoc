def count_deltas(adapters):
    adapters.sort()
    ones, twos, threes = 0, 0, 1
    prev = 0
    for a in adapters:
        if a - prev == 1:
            ones += 1
        elif a - prev == 2:
            twos += 1
        elif a - prev == 3:
            threes += 1
        prev = a
    return ones, twos, threes


def main():
    pathname = "input.txt"
    with open(pathname) as f:
        content = f.readlines()
        adapters = [int(line) for line in content]
        ones, twos, threes = count_deltas(adapters)
        print("{} 1-jolt deltas and {} 3-jolt deltas => {}".format(ones, threes, ones * threes))

if __name__ == "__main__":
    main()
