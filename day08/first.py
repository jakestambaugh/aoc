class Instruction:
    def __init__(self, op, val):
        self.op = op
        self.val = int(val)

    def __repr__(self):
        return "{} {}".format(self.op, self.val)


class Processor:
    def __init__(self, prog):
        self.acc = 0
        self.pc = 0
        self.visited = set()
        self.program = prog

    def execute(self):
        while not self.pc in self.visited and self.pc < len(self.program):
            self.visited.add(self.pc)
            ins = self.program[self.pc]
            if ins.op == "acc":
                self.acc += ins.val
            elif ins.op == "jmp":
                self.pc += (ins.val - 1)
            elif ins.op == "nop":
                pass
            self.pc += 1
        if self.pc in self.visited:
            self.infinite = True


def parse_line(line):
    instruction = line.strip().split(" ")
    assert(len(instruction) == 2)
    return Instruction(instruction[0], instruction[1])


def parse_program(program):
    return [parse_line(line) for line in program]

def main():
    pathname = "input.txt"
    with open(pathname) as f:
        content = f.readlines()
        instructions = parse_program(content)
        proc = Processor(instructions)
        proc.execute()
        print("Accumulator: {}".format(proc.acc))


if __name__ == "__main__":
    main()
