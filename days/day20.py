from days import AOCDay, day


@day(20)
class Day20(AOCDay):
    ranges = []

    test_input = """5-8
0-2
4-7""".split("\n")

    def test(self, input_data):
        self.input_data = self.test_input
        self.common(self.input_data)
        assert self.ranges == [(0, 2), (4, 8)], f'{self.ranges} != [(0, 2), (4, 8)]'
        self.input_data = input_data

    def common(self, input_data):
        self.ranges = []
        current_range = None
        for line in sorted(self.input_data, key=lambda x: int(x.split("-")[0])):
            x, y = map(int, line.split("-"))
            if current_range is not None:
                if current_range[0] <= x <= (current_range[1] + 1):
                    if y > current_range[1]:
                        current_range = (current_range[0], y)
                    # Else values already included in current range
                elif (current_range[0] - 1) <= y <= current_range[1]:
                    if x < current_range[0]:
                        current_range = (x, current_range[1])
                    # Else values already included in current range
                else:
                    self.ranges.append(current_range)
                    current_range = (x, y)
            else:
                current_range = (x, y)
        self.ranges.append(current_range)
        self.debug(f"Ranges: {self.ranges}")

    def part1(self, input_data):
        yield self.ranges[0][1]+1

    def part2(self, input_data):
        allowed = 0
        # Initial IPs
        allowed += self.ranges[0][0]

        # IPs between blocks
        for i in range(len(self.ranges) - 1):
            r1, r2 = self.ranges[i], self.ranges[i+1]
            allowed += (r2[0] - 1) - r1[1]

        # Last few IPs
        allowed += 4294967295 - self.ranges[-1][1]

        yield allowed
