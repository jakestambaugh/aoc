def split_groups(content):
    groups = content.split("\n\n")
    answers = []
    for group in groups:
        answers.append(group.split("\n"))
    return answers


def count_yes(group):
    yes = set()
    for answer in group:
        for c in answer:
            yes.add(c)
    return len(yes)


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
