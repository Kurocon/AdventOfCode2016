import re

from days import AOCDay, day


@day(9)
class Day9(AOCDay):
    def common(self, input_data):
        pass

    def decompress_once(self, string):
        result_str = ""
        i = 0
        while i < len(string):
            if string[i] == "(":
                endi = string[i:].find(")")
                chars, repeats = [int(x) for x in string[(i + 1):(i + endi)].split("x")]

                repeat_block = string[(i + endi + 1):(i + endi + 1 + chars)]
                result_str += "".join(repeat_block for _ in range(repeats))

                i += endi + chars
            else:
                result_str += string[i]
            i += 1
        return result_str

    def decompress_length(self, string):
        result_len = 0
        i = 0
        if string.find("(") == -1:
            return len(string)
        while i < len(string):
            substring = string[i:]
            starti = substring.find("(")
            # Length of eventual inbitweenstring
            result_len += len(string[i:i + starti])
            if starti != -1:
                endi = substring[starti:].find(")")
                chars, repeats = [int(x) for x in substring[(starti + 1):(starti + endi)].split("x")]
                partlen = self.decompress_length(substring[(starti + endi + 1):(starti + endi + 1 + chars)]) * repeats
                result_len += partlen
                i += endi + chars + 1
            else:
                break
        return result_len

    def decompress_fully(self, string):
        while "(" in string:
            string = self.decompress_once(string)
        return string

    def part1(self, input_data):
        result_str = self.decompress_once(input_data)
        yield len(result_str)

    def part2(self, input_data):
        yield self.decompress_length(input_data)
