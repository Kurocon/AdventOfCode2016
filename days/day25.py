from days import AOCDay, day


class WrongOutputError(RuntimeError):
    pass


class SuccessError(RuntimeError):
    pass


@day(25)
class Day25(AOCDay):
    registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    instruction_set = {}
    pc = 0

    out_count = 0
    out_expected = 0

    def common(self, input_data):
        self.registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
        self.instruction_set = {
            'cpy': self.cpy,
            'inc': self.inc,
            'dec': self.dec,
            'jnz': self.jnz,
            'out': self.out,
        }
        self.pc = 0
        self.instructions = []
        self.out_count = 0
        self.out_expected = 0
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

    def out(self, x):
        x = x if type(x) == int else self.registers[x]
        self.debug(f"out {x}")
        if x == self.out_expected:
            self.out_count += 1
            self.out_expected = 1 if self.out_expected == 0 else 0
        else:
            raise WrongOutputError(f"Expected {self.out_expected}, got {x}")
        return True

    def part1(self, input_data):
        current_a = 0
        try:
            while True:
                self.debug(f"Starting with a == {current_a}")
                self.registers['a'] = current_a
                while self.pc < len(self.instructions):
                    instr, *args = self.instructions[self.pc]
                    try:
                        inc = self.instruction_set[instr](*args)
                        if inc:
                            self.pc += 1

                        if self.out_count > 50:
                            raise SuccessError("Done!")
                    except WrongOutputError as e:
                        self.debug(str(e))
                        break

                # It was not this A, reset VM and continue.
                current_a += 1
                self.registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
                self.pc = 0
                self.out_count = 0
                self.out_expected = 0
        except SuccessError:
            pass
        yield current_a

    def part2(self, input_data):
        yield "Merry christmas!"
