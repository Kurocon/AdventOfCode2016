from days import AOCDay, day


@day(12)
class Day12(AOCDay):
    test_input = """cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a""".split("\n")
    registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    instruction_set = {}
    pc = 0

    def common(self, input_data):
        # input_data = self.test_input
        self.registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
        self.instruction_set = {
            'cpy': self.cpy,
            'inc': self.inc,
            'dec': self.dec,
            'jnz': self.jnz,
        }
        self.pc = 0
        self.instructions = []
        for line in input_data:
            instr = line.split()
            for i in range(len(instr)):
                try:
                    instr[i] = int(instr[i])
                except ValueError:
                    pass
            self.instructions.append(instr)

    def cpy(self, x, y):
        self.registers[y] = x if type(x) == int else self.registers[x]
        return True

    def inc(self, x):
        self.registers[x] += 1
        return True

    def dec(self, x):
        self.registers[x] -= 1
        return True

    def jnz(self, x, y):
        if (x if type(x) == int else self.registers[x]) != 0:
            self.pc += y
            return False
        return True

    def part1(self, input_data):
        while self.pc < len(self.instructions):
            instr, *args = self.instructions[self.pc]
            inc = self.instruction_set[instr](*args)
            if inc:
                self.pc += 1
        print(self.registers['a'])

    def part2(self, input_data):
        self.registers['c'] = 1
        while self.pc < len(self.instructions):
            instr, *args = self.instructions[self.pc]
            inc = self.instruction_set[instr](*args)
            if inc:
                self.pc += 1
        print(self.registers['a'])
