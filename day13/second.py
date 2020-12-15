import math
import functools
import operator


def flip(func):
    @functools.wraps(func)
    def newfunc(x, y):
        return func(y, x)
    return newfunc


def foldr(func, acc, xs):
    return functools.reduce(flip(func), reversed(xs), acc)


def parse_schedule(schedule):
    parsed = [int(x) if not x == "x" else x for x in schedule.strip().split(",")]
    return [(bus, offset) for offset, bus in enumerate(parsed) if not bus == "x"]


def gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, s, t = gcd(b % a, a)
    return (g, t - (b // a) * s, s)


def inv(a, m):
    _, i, _ = gcd(a, m)
    print(m)
    return i % m


def chinese_remainder_theorem(first, second):
    r1, m1 = first
    r2, m2 = second
    print(first, second)
    r = r2 + m2 * (r1 - r2) * inv(m2, m1)
    m = m2 * m1
    return (r % m, m)


def next_bus(bus, t):
    return int(math.ceil(t / bus)) * bus


def find_remainder(schedule):
    return foldr(chinese_remainder_theorem, (0, 1), schedule)


def main():
    pathname = "input.txt"
    with open(pathname) as f:
        content = f.readlines()
        schedule = parse_schedule(content[1])
        mods = {bus: -off % bus for bus, off in schedule}
        print(mods)
        busses = list(reversed(sorted(mods)))
        target = mods[busses[0]]
        candidate = busses[0]
        for b in busses[1:]:
            while target % b != mods[b]:
                target += candidate
            candidate *= b
        print("t = {}".format(target))


if __name__ == "__main__":
    main()
