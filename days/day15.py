import re

from days import AOCDay, day


@day(15)
class Day15(AOCDay):
    test_data = """Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.""".split("\n")

    LINE_RE = re.compile(r"Disc #([0-9]+) has ([0-9]+) positions; at time=0, it is at position ([0-9]+)")
    discs = []  # (disc_id, num_positions, pos_time_zero)

    def can_pass(self, disc_id, num_positions, pos_time_zero, btn_press_time):
        return ((pos_time_zero + disc_id + btn_press_time) % num_positions) == 0

    def common(self, input_data):
        # self.input_data = self.test_data
        self.discs = []
        for line in self.input_data:
            if m := self.LINE_RE.match(line):
                self.discs.append((int(m.group(1)), int(m.group(2)), int(m.group(3))))
        self.debug(str(self.discs))

    def part1(self, input_data):
        start_time = 0
        while True:
            if all(self.can_pass(x[0], x[1], x[2], start_time) for x in self.discs):
                yield start_time
                break
            start_time += 1

    def part2(self, input_data):
        # Add new disk
        self.discs.append((7, 11, 0))

        start_time = 0
        while True:
            if all(self.can_pass(x[0], x[1], x[2], start_time) for x in self.discs):
                yield start_time
                break
            start_time += 1
