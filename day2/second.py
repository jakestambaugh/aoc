import re


class Password:
    def __init__(self, pos1, pos2, target, password):
        self.pos1 = pos1 - 1
        self.pos2 = pos2 - 1
        self.target = target
        self.password = password

    def __repr__(self):
        return "pos1: {}, pos2: {}, char: {}, pass: {}".format(self.pos1, self.pos2, self.target, self.password)

    def is_valid(self):
        return (self.password[self.pos1] == self.target) != (self.password[self.pos2] == self.target)


def parse_password(line):
    p = re.compile(r"(?P<a>[0-9]+)-(?P<b>[0-9]+) (?P<char>[a-z]): (?P<pass>[a-z]+)")
    m = p.match(line)
    if m:
        groups = m.groupdict()
        return Password(int(groups["a"]), int(groups["b"]), groups["char"], groups["pass"])


def main():
    pathname = "input.txt"
    with open(pathname) as f:
        content = f.readlines()
        valid = 0
        for line in content:
            passw = parse_password(line)
            if passw.is_valid():
                valid += 1
    print("{}".format(valid))


if __name__ == "__main__":
    main()
