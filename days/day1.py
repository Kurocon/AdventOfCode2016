from days import AOCDay, day

NORTH = 0
EAST  = 1
SOUTH = 2
WEST  = 3

LEFT  = -1
RIGHT = 1

DIR_MAP = {"L": LEFT, "R": RIGHT}
DELTA_POS = {
    NORTH: (0, 1),
    EAST: (1, 0),
    SOUTH: (0, -1),
    WEST: (-1, 0),

}

@day(1)
class Day1(AOCDay):

    direction = NORTH
    position = (0, 0)
    instructions = []
    history = []

    def manhattan_distance(self, x, y):
        return sum(abs(xi - yi) for xi, yi in zip(x, y))

    def common(self, input_data):
        self.instructions = input_data.split(", ")
        self.direction = NORTH
        self.position = (0, 0)
        self.history = [(0, 0)]

    def part1(self, input_data):
        for instruction in self.instructions:
            self.direction = (self.direction + DIR_MAP[instruction[0]]) % 4
            for i in range(int(instruction[1:])):
                self.position = (
                    self.position[0] + DELTA_POS[self.direction][0],
                    self.position[1] + DELTA_POS[self.direction][1]
                )
        yield self.manhattan_distance((0, 0), self.position)

    def part2(self, input_data):
        for instruction in self.instructions:
            self.direction = (self.direction + DIR_MAP[instruction[0]]) % 4
            for i in range(int(instruction[1:])):
                self.position = (
                    self.position[0] + DELTA_POS[self.direction][0],
                    self.position[1] + DELTA_POS[self.direction][1]
                )
                if self.position in self.history:
                    yield self.manhattan_distance((0, 0), self.position)
                    return
                else:
                    self.history.append(self.position)
