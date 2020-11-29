from collections import defaultdict
from math import floor, log

from days import AOCDay, day


@day(19)
class Day19(AOCDay):
    # This is the Josephus Problem:
    # Wikipedia: https://en.wikipedia.org/wiki/Josephus_problem
    # J(N) = (N - 2^floor(log2(N)))*2 + 1

    def common(self, input_data):
        self.num_elves = int(self.input_data)

    def part1(self, input_data):
        yield (self.num_elves - 2 ** floor(log(self.num_elves, 2))) * 2 + 1

    def part2(self, input_data):
        l = floor(log(self.num_elves, 3))
        k = self.num_elves - 3 ** l
        if k == 0:
            yield self.num_elves  # is a power of 3
        elif l == 1 or k <= (3 ** l):
            yield k
        else:
            yield 3 ** l + 2 * (k - 3 ** l)
