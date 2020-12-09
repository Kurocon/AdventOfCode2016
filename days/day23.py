from days import AOCDay, day


@day(23)
class Day23(AOCDay):
    test_input = """cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
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
            'tgl': self.tgl,
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
        if type(y) == int:
            # Invalid instruction (probably toggled), ignore.
            return True
        self.registers[y] = x if type(x) == int else self.registers[x]
        return True

    def inc(self, x):
        if type(x) == int:
            # Invalid instruction (probably toggled), ignore.
            return True
        self.registers[x] += 1
        return True

    def dec(self, x):
        if type(x) == int:
            # Invalid instruction (probably toggled), ignore.
            return True
        self.registers[x] -= 1
        return True

    def jnz(self, x, y):
        if (x if type(x) == int else self.registers[x]) != 0:
            self.pc += y if type(y) == int else self.registers[y]
            return False
        return True

    def tgl(self, x):
        x = x if type(x) == int else self.registers[x]
        try:
            instr = self.instructions[self.pc + x]
        except IndexError:
            # Ignore if target instruction out of range
            return True

        if len(instr[1:]) == 1:
            # inc becomes dec, and all other one-argument instructions become inc.
            instr[0] = "dec" if instr[0] == "inc" else "inc"
        elif len(instr[1:]) == 2:
            # jnz becomes cpy, and all other two-instructions become jnz.
            instr[0] = "cpy" if instr[0] == "jnz" else "jnz"
        self.instructions[self.pc + x] = instr
        return True

    def starting_addition(self):
        # Return source and destination registers if we are starting an addition, else return (None, None)
        try:
            i0, i1, i2 = self.instructions[self.pc:self.pc + 3]
        except ValueError:
            # Not enough instructions left, so no loop
            return None, None

        # An add loop will be either (inc, dec, jnz -2), or (dec, inc, jnz -2). Not in a loop if that is not true
        if (i0[0], i1[0], i2[0]) not in [('inc', 'dec', 'jnz'), ('dec', 'inc', 'jnz')] or i2[2] != -2:
            return None, None

        # Get the increment/decrement registers into variables based on the first instruction
        inc_reg, dec_reg = (i0[1], i1[1]) if i0[0] == 'inc' else (i1[1], i0[1])

        # Jump reg should be the same as the dec reg, and inc reg should not be the same as dec reg
        if i2[1] != dec_reg or inc_reg == dec_reg:
            return None, None

        # Else we are in an add loop, return the increment and decrement register so we can optimize
        return inc_reg, dec_reg

    def starting_multiplication(self, inc_reg, dec_reg):
        # Return multiplication register if we are starting a multiplication loop, else return None
        try:
            i0, i1 = self.instructions[self.pc + 3:self.pc + 5]
        except ValueError:
            # Not enough instructions left, so no loop
            return None

        # A multiplication loop will be (dec, jnz -5). Not in a loop if that is not true
        if (i0[0], i1[0]) != ('dec', 'jnz') or i1[2] != -5:
            return None

        # Multiplication register should be the same as the jump register, and not the same as the inc or dec registers.
        if i0[1] != i1[1] or i0[1] == inc_reg or i0[1] == dec_reg:
            return None

        return i0[1]

    def optimize(self):
        # Check if we can optimize and modify params accordingly.
        # Return True if optimized (skips instruction), else False

        inc_reg, dec_reg = self.starting_addition()
        if inc_reg is None or dec_reg is None:
            return False

        mult_reg = self.starting_multiplication(inc_reg, dec_reg)
        if mult_reg is not None:
            # Can optimize a multiplication
            self.registers[inc_reg] += self.registers[dec_reg] * self.registers[mult_reg]
            self.registers[dec_reg] = 0
            self.registers[mult_reg] = 0
            self.pc += 5
        else:
            # Can optimize an addition
            self.registers[inc_reg] += self.registers[dec_reg]
            self.registers[dec_reg] = 0
            self.pc += 3
        return True

    def part1(self, input_data):
        self.registers['a'] = 7
        while self.pc < len(self.instructions):
            instr, *args = self.instructions[self.pc]
            inc = self.instruction_set[instr](*args)
            if inc:
                self.pc += 1
        yield self.registers['a']

    def part2(self, input_data):
        self.registers['a'] = 12
        while self.pc < len(self.instructions):
            if self.optimize():
                continue
            instr, *args = self.instructions[self.pc]
            inc = self.instruction_set[instr](*args)
            if inc:
                self.pc += 1
        yield self.registers['a']
