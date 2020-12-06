def count_trees(rows):
    y = 0
    trees = 0
    for r in rows:
        row = r.strip()
        coord = row[y % len(row)]
        if coord == "#":
            trees += 1
        y += 3
    return trees

def main():
    pathname = "input.txt"
    with open(pathname) as f:
        content = f.readlines()
        trees = count_trees(content)
        print("{} trees".format(trees))


if __name__ == "__main__":
    main()
