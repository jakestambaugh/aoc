class Instruction:
    def __init__(self, op, val):
        self.op = op
        self.val = int(val)

    def __repr__(self):
        return "{} {:5d}".format(self.op, self.val)


class Processor:
    def __init__(self, prog):
        self.acc = 0
        self.pc = 0
        self.visited = []
        self.infinite = False
        self.program = prog[:]
 
    def mutate(self, mutation):
        line = mutation[0]
        target = self.program[line]
        self.program[line] = Instruction(mutation[1], target.val)

    def execute(self):
        while not self.pc in self.visited and self.pc < len(self.program):
            self.visited.append(self.pc)
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

    def print_execution_order(self):
        for line, ins in enumerate(self.program):
            if line in self.visited:
                print("{} | {}".format(ins, self.visited.index(line)))
            else:
                print("{} |".format(ins))


def parse_line(line):
    instruction = line.strip().split(" ")
    assert(len(instruction) == 2)
    return Instruction(instruction[0], instruction[1])


def parse_program(program):
    return [parse_line(line) for line in program]


def find_jmps(instructions):
    return [i for i, ins in enumerate(instructions) if ins.op == "jmp"]


def find_nops(instructions):
    return [i for i, ins in enumerate(instructions) if ins.op == "nop"]


def find_mutations(instructions):
    jmps = find_jmps(instructions)
    nops = find_nops(instructions)
    return [(i, "nop") for i in jmps] + [(j, "jmp") for j in nops]


def main():
    pathname = "input.txt"
    with open(pathname) as f:
        content = f.readlines()
        instructions = parse_program(content)
        mutations = find_mutations(instructions)
        for mutation in mutations:
            proc = Processor(instructions)
            proc.mutate(mutation)
            proc.execute()
            if proc.infinite == False:
                proc.print_execution_order()
                print("Accumulator: {}".format(proc.acc))


if __name__ == "__main__":
    main()
