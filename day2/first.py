import re


class Password:
    def __init__(self, low, high, target, password):
        self.low = low
        self.high = high
        self.target = target
        self.password = password

    def __repr__(self):
        return "min: {}, max: {}, char: {}, pass: {}".format(self.low, self.high, self.target, self.password)

    def is_valid(self):
        t = 0
        for x in self.password:
            if x == self.target:
                t += 1
        return (self.low <= t) and (t <= self.high)


def parse_password(line):
    p = re.compile(r"(?P<min>[0-9]+)-(?P<max>[0-9]+) (?P<char>[a-z]): (?P<pass>[a-z]+)")
    m = p.match(line)
    if m:
        groups = m.groupdict()
        return Password(int(groups["min"]), int(groups["max"]), groups["char"], groups["pass"])


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
