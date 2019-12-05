from days import AOCDay, day


@day(8)
class Day8(AOCDay):
    test_input = """rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1"""

    screen = []
    instructions = []

    def print_screen(self):
        for line in self.screen:
            print("".join(line))

    def common(self, input_data):
        # input_data = self.test_input.split("\n")
        self.screen = [[" " for i in range(50)] for j in range(6)]
        self.instructions = [x.split() for x in input_data]

        for instruction in self.instructions:
            if instruction[0] == "rect":
                self.rect(instruction[1])
            elif instruction[0] == "rotate" and instruction[1] == "row":
                self.rotate_row(instruction[2][2:], instruction[4])
            elif instruction[0] == "rotate" and instruction[1] == "column":
                self.rotate_column(instruction[2][2:], instruction[4])

    def rect(self, dimensions):
        x, y = map(int, dimensions.split("x"))
        for i in range(x):
            for j in range(y):
                self.screen[j][i] = "#"

    def rotate_row(self, row, amount):
        row = int(row)
        amount = int(amount)
        for i in range(amount):
            carry = self.screen[row][-1]
            for j in range(len(self.screen[row]) - 2, -1, -1):
                self.screen[row][j + 1] = self.screen[row][j]
            self.screen[row][0] = carry

    def rotate_column(self, column, amount):
        column = int(column)
        amount = int(amount)
        for i in range(amount):
            carry = self.screen[-1][column]
            for j in range(len(self.screen) - 2, -1, -1):
                self.screen[j + 1][column] = self.screen[j][column]
            self.screen[0][column] = carry

    def part1(self, input_data):
        yield sum(1 if x == "#" else 0 for line in self.screen for x in line)

    def part2(self, input_data):
        self.print_screen()
