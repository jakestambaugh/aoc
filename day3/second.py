def count_trees(rows, right, down):
    y = 0
    trees = 0
    for i, r in enumerate(rows):
        if not i % down == 0:
            continue
        row = r.strip()
        coord = row[y % len(row)]
        if coord == "#":
            trees += 1
        y += right
    return trees

def main():
    pathname = "input.txt"
    with open(pathname) as f:
        content = f.readlines()
        trees = []
        trees.append(count_trees(content, 1, 1))
        trees.append(count_trees(content, 3, 1))
        trees.append(count_trees(content, 5, 1))
        trees.append(count_trees(content, 7, 1))
        trees.append(count_trees(content, 1, 2))
        product = 1
        for x in trees:
            product = product * x
        print("{}".format(product))


if __name__ == "__main__":
    main()
