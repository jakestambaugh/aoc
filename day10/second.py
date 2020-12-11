from collections import deque

cache = {}

def count_combos(adapters):
    combos = 0
    current = adapters.popleft()
    if current in cache:
        return cache[current]
    if not adapters:
        return 1
    for x in range(1,4):
        if adapters and current + x == adapters[0]:
            combos += count_combos(adapters.copy())
            adapters.popleft()
    cache[current] = combos
    return combos


def main():
    pathname = "input.txt"
    with open(pathname) as f:
        content = f.readlines()
        adapters = deque(sorted([int(line) for line in content]))
        adapters.appendleft(0)
        count = count_combos(adapters)
        print("{} arrangements".format(count))


if __name__ == "__main__":
    main()
