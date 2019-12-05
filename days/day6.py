from days import AOCDay, day

from collections import Counter

@day(6)
class Day6(AOCDay):
    test_input = """eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar"""

    def common(self, input_data):
        pass

    def part1(self, input_data):
        columns = zip(*input_data)
        msg = ""
        for column in columns:
            c = Counter(column)
            msg += c.most_common(1)[0][0]
        yield msg

    def part2(self, input_data):
        columns = zip(*input_data)
        msg = ""
        for column in columns:
            c = Counter(column)
            msg += c.most_common()[-1][0]
        yield msg
