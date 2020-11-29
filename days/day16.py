from days import AOCDay, day


@day(16)
class Day16(AOCDay):
    def dragon_curve(self, a):
        b = "".join("0" if x == "1" else "1" for x in reversed(a))
        return a + "0" + b

    def fill_to(self, initial, size):
        while len(initial) < size:
            initial = self.dragon_curve(initial)
        return initial[:size]

    def checksum(self, data):
        check = "".join("1" if data[2*i] == data[(2*i)+1] else "0" for i in range(len(data) // 2))
        if len(check) % 2 == 0:
            return self.checksum(check)
        else:
            return check

    def test(self, input_data):
        assert self.dragon_curve("1") == "100", f'{self.dragon_curve("1")} != "100"'
        assert self.dragon_curve("0") == "001", f'{self.dragon_curve("0")} != "001"'
        assert self.dragon_curve("11111") == "11111000000", f'{self.dragon_curve("11111")} != "11111000000"'
        assert self.dragon_curve("111100001010") == "1111000010100101011110000", f'{self.dragon_curve("111100001010")} != "1111000010100101011110000"'

        assert self.checksum("110010110100") == "100", f'{self.checksum("110010110100")} != "100"'

        assert self.fill_to("10000", 20) == "10000011110010000111110"[:20], f'{self.fill_to("10000", 20)} != {"10000011110010000111110"[:20]}'

        assert self.checksum(self.fill_to("10000", 20)) == "01100", f'{self.checksum(self.fill_to("10000", 20))} != "01100"'

    def part1(self, input_data):
        yield self.checksum(self.fill_to(self.input_data, 272))

    def part2(self, input_data):
        yield self.checksum(self.fill_to(self.input_data, 35651584))
