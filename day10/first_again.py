def count_deltas(adapters):
    adapters = set(adapters)
    ones, twos, threes = 0, 0, 1
    prev = 0
    while adapters:
        if prev + 1 in adapters:
            ones += 1
            adapters.remove(prev + 1)
            prev += 1
        elif prev + 2 in adapters:
            twos += 1
            adapters.remove(prev + 2)
            prev += 2
        elif prev + 3 in adapters:
            threes += 1
            adapters.remove(prev + 3)
            prev += 3
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
