def find_sum(values, target):
    values.sort()
    start = 0
    end = len(values) - 1
    while start < end:
        sum = values[start] + values[end]
        if sum == target:
            return values[start], values[end]
        elif sum > target:
            end -= 1
        elif sum < target:
            start += 1
    return (None, None)

def main():
    pathname = "input.txt"
    with open(pathname) as f:
        content = f.readlines()
        values = [int(x) for x in content]
        x, y = find_sum(values, 2020)
        print("{} * {} = {}".format(x, y, x * y))


if __name__ == "__main__":
    main()
