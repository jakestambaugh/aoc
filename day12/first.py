def apply_rotations(instructions):
    facing = 90
    cardinals = []
    for i in instructions:
        op, value = i
        if op == "N" or op == "E" or op == "S" or op == "W":
            cardinals.append(i)
        elif op == "R":
            facing = (facing + value) % 360
            assert(facing > -1)
        elif op == "L":
            facing = (facing - value) % 360
            assert(facing > -1)
        elif op == "F":
            if facing == 0:
                motion = "N"
            elif facing == 90:
                motion = "E"
            elif facing == 180:
                motion = "S"
            elif facing == 270:
                motion = "W"
            else:
                print("Something has gone wrong at {}".format(i))
            cardinals.append((motion, value))
    return cardinals


def apply_translations(instructions):
    translations = []
    for direction, value in instructions:
        if direction == "N":
            translations.append((0, value))
        elif direction == "E":
            translations.append((value, 0))
        elif direction == "S":
            translations.append((0, -1 * value))
        elif direction == "W":
            translations.append((-1 * value, 0))
    return translations


def manhattan_distance(motions):
    x, y = 0, 0
    for mx, my in motions:
        x += mx
        y += my
    return abs(x) + abs(y)


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
        cardinals = apply_rotations(instructions)
        motions = apply_translations(cardinals)
        distance = manhattan_distance(motions)
        print("{} is the Manhattan distance travelled.".format(distance))


if __name__ == "__main__":
    main()
