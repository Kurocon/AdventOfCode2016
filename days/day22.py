import re
from itertools import permutations

from days import AOCDay, day


@day(22)
class Day22(AOCDay):
    node_re = re.compile(r"/dev/grid/node-x([0-9]+)-y([0-9]+) +([0-9]+)T +([0-9]+)T +([0-9]+)T +([0-9]+)%")
    nodes = {}

    test_input = """Filesystem            Size  Used  Avail  Use%
Filesystem            Size  Used  Avail  Use%
/dev/grid/node-x0-y0   10T    8T     2T   80%
/dev/grid/node-x0-y1   11T    6T     5T   54%
/dev/grid/node-x0-y2   32T   28T     4T   87%
/dev/grid/node-x1-y0    9T    7T     2T   77%
/dev/grid/node-x1-y1    8T    0T     8T    0%
/dev/grid/node-x1-y2   11T    7T     4T   63%
/dev/grid/node-x2-y0   10T    6T     4T   60%
/dev/grid/node-x2-y1    9T    8T     1T   88%
/dev/grid/node-x2-y2    9T    6T     3T   66%""".split("\n")

    def empty(self, node):
        return self.used(node) == 0

    def size(self, node):
        return self.nodes[node][0]

    def used(self, node):
        return self.nodes[node][1]

    def avail(self, node):
        return self.nodes[node][2]

    def test(self, input_data):
        self.common(input_data)
        res = next(self.part1(input_data))
        assert res == 1020, f"Part 1 test failed: {res} != 1020"
        res = next(self.part2(input_data))
        assert res == 198, f"Part 2 test failed: {res} != 198"

    def common(self, input_data):
        # input_data = self.test_input
        self.nodes = {}
        for line in input_data[2:]:
            if m := self.node_re.match(line):
                x, y, size, used, avail, use = m.groups()
                self.nodes[int(x), int(y)] = (int(size), int(used), int(avail), int(use))
            else:
                raise ValueError(f"Line '{line}' failed to parse.")

        self.max_x = max(map(lambda x: x[0], self.nodes.keys()))
        self.max_y = max(map(lambda x: x[1], self.nodes.keys()))
        self.target = (self.max_x, 0)

    def part1(self, input_data):
        yield sum(1 for a, b in permutations(self.nodes.keys(), 2) if not self.empty(a) and self.avail(b) >= self.used(a))

    def part2(self, input_data):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        start_pos = next(x for x in self.nodes.keys() if self.used(x) == 0)

        queue = [(start_pos, self.target, 0)]
        visited = {(start_pos, self.target)}

        while queue:
            old_pos, old_data_pos, old_steps = queue.pop(0)
            new_steps = old_steps + 1
            for d in directions:
                new_pos = (old_pos[0] + d[0], old_pos[1] + d[1])
                if 0 <= new_pos[1] < (self.max_y + 1) and 0 <= new_pos[0] < (self.max_x + 1) and self.used(new_pos) < 100:
                    new_data_pos = old_pos if new_pos == old_data_pos else old_data_pos
                    if (new_pos, new_data_pos) not in visited:
                        queue.append((new_pos, new_data_pos, new_steps))
                        visited.add((new_pos, new_data_pos))
                    if new_data_pos == (0, 0):
                        yield new_steps
                        return
