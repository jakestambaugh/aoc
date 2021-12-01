def split_groups(content):
    groups = content.split("\n\n")
    answers = []
    for group in groups:
        s = group.split("\n")
        answers.append([x for x in s if x])
    return answers


def count_yes(group):
    first = set(list(group[0]))
    rest = [set(list(x)) for x in group[1:]]
    intersect = first.intersection(*rest)
    return len(intersect)


def main():
    pathname = "input.txt"
    with open(pathname) as f:
        content = f.read()
        groups = split_groups(content)
        sums = 0
        for group in groups:
            sums += count_yes(group)
        print("Total yes answers: {}".format(sums))

if __name__ == "__main__":
    main()
