def rotate(facing, waypoint):
    if facing == 90 or facing == -270:
        return (waypoint[1], -1 * waypoint[0])
    elif facing == 180 or facing == -180: 
        return (-1 * waypoint[0], -1 * waypoint[1])
    elif facing == 270 or facing == -90:
        return (-1 * waypoint[1], waypoint[0])
    else:
        print("Issue with {} {}".format(facing, waypoint))


def navigate(instructions):
    waypoint = (10, 1)
    boat = (0, 0)
    for op, value in instructions:
        if op == "N":
            waypoint = (waypoint[0], waypoint[1] + value)
        elif op == "E":
            waypoint = (waypoint[0] + value, waypoint[1])
        elif op == "S":
            waypoint = (waypoint[0], waypoint[1] - value)
        elif op == "W":
            waypoint = (waypoint[0] - value, waypoint[1])
        elif op == "R":
            facing = value
            waypoint = rotate(facing, waypoint)
        elif op == "L":
            facing = -1 * value
            waypoint = rotate(facing, waypoint)
        elif op == "F":
            boat = (boat[0] + waypoint[0] * value, boat[1] + waypoint[1] * value)
    return boat 


def parse_instructions(lines):
    instructions = []
    for line in lines:
        line = line.strip()
        op = line[0]
        value = int(line[1:])
        instructions.append((op, value))
    return instructions


def main():
    pathname = "input.txt"
    with open(pathname) as f:
        content = f.readlines()
        instructions = parse_instructions(content)
        boat = navigate(instructions)
        distance = abs(boat[0]) + abs(boat[1])
        print("{} is the Manhattan distance travelled.".format(distance))


if __name__ == "__main__":
    main()
