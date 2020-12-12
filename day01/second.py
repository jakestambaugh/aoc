def find_triple(values, target=2020):
    for x in values:
        for y in values:
            for z in values:
                if x + y + z == target:
                    return (x, y, z)
    return (None, None, None)

def main():
    pathname = "input.txt"
    with open(pathname) as f:
        content = f.readlines()
        values = [int(x) for x in content]
        x, y, z = find_triple(values, 2020)
        if not x or not y or not z:
            print("Failed to find")
        else:
            print("{} * {} * {} = {}".format(x, y, z, x * y * z))


if __name__ == "__main__":
    main()
