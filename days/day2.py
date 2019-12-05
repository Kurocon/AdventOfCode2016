from days import AOCDay, day


KEYPAD = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
]

KEYPAD2 = [
    [' ', ' ', '1', ' ', ' '],
    [' ', '2', '3', '4', ' '],
    ['5', '6', '7', '8', '9'],
    [' ', 'A', 'B', 'C', ' '],
    [' ', ' ', 'D', ' ', ' '],
]

DELTA_POS = {
    "U": (0, -1),
    "D": (0, 1),
    "L": (-1, 0),
    "R": (1, 0),
}

@day(2)
class Day2(AOCDay):

    x = 1
    y = 1

    def common(self, input_data):
        pass

    def part1(self, input_data):
        code = []
        for line in input_data:
            for char in line:
                self.x = min(max(self.x + DELTA_POS[char][0], 0), 2)
                self.y = min(max(self.y + DELTA_POS[char][1], 0), 2)
            code.append(KEYPAD[self.y][self.x])
        yield "".join(code)

    def part2(self, input_data):
        code = []
        for line in input_data:
            for char in line:
                newx = min(max(self.x + DELTA_POS[char][0], 0), 4)
                newy = min(max(self.y + DELTA_POS[char][1], 0), 4)
                self.x = newx if KEYPAD2[self.y][newx] != ' ' else self.x
                self.y = newy if KEYPAD2[newy][self.x] != ' ' else self.y
            code.append(KEYPAD2[self.y][self.x])
        yield "".join(code)
