import math


def parse_schedule(raw_schedule):
    return [int(x) for x in raw_schedule.strip().split(",") if not x == "x"]


def next_arrival(earliest, schedule):
    upcoming = {}
    for bus in schedule:
        time = int(math.ceil(earliest / bus)) * bus
        # print("next {} bus after {} => {}".format(bus, earliest, time))
        upcoming[time] = bus
    return upcoming


def main():
    pathname = "input.txt"
    with open(pathname) as f:
        content = f.readlines()
        earliest = int(content[0].strip())
        schedule = parse_schedule(content[1])
        arrivals = next_arrival(earliest, schedule)
        n = min(arrivals.keys())
        print("Next bus is {} coming at {}. Answer is {}".format(arrivals[n], n, (n - earliest) * arrivals[n]))


if __name__ == "__main__":
    main()
