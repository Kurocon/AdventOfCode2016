import re

from days import AOCDay, day


@day(21)
class Day21(AOCDay):
    def swap_pos(self, password: str, x: int, y: int):
        password = list(password)
        password[x], password[y] = password[y], password[x]
        return "".join(password)

    def swap_letter(self, password: str, x: str, y: str):
        return password.replace(x, ".").replace(y, x).replace(".", y)

    def rotate_left(self, password: str, x: int):
        x = x % len(password)
        return password[x:] + password[:x]

    def rotate_right(self, password: str, x: int):
        x = x % len(password)
        return password[-x:] + password[:-x]

    def rotate_index(self, password: str, x: str):
        index = password.index(x)
        if index >= 4:
            index += 1
        return self.rotate_right(password, 1 + index)

    def r_rotate_index(self, password: str, x: str):
        i = 0
        while True:
            p = self.rotate_left(password, i)
            if password == self.rotate_index(p, x):
                return p
            i += 1

    def reverse(self, password: str, x: int, y: int):
        a, b, c = password[:x], password[x:y+1], password[y+1:]
        return a + b[::-1] + c

    def move(self, password: str, x: int, y: int):
        a, password = password[x], password[:x] + password[x + 1:]
        return password[:y] + a + password[y:]

    def r_move(self, password: str, x: int, y: int):
        a, password = password[y], password[:y] + password[y + 1:]
        return password[:x] + a + password[x:]

    func_map = {
        r"swap position ([0-9]) with position ([0-9])": ('i', swap_pos, swap_pos),
        r"swap letter ([a-z]) with letter ([a-z])": ('c', swap_letter, swap_letter),
        r"rotate left ([0-9]) step": ('i', rotate_left, rotate_right),
        r"rotate right ([0-9]) step": ('i', rotate_right, rotate_left),
        r"rotate based on position of letter ([a-z])": ('c', rotate_index, r_rotate_index),
        r"reverse positions ([0-9]) through ([0-9])": ('i', reverse, reverse),
        r"move position ([0-9]) to position ([0-9])": ('i', move, r_move),
    }

    instructions = []

    def test(self, input_data):
        input = "abcde"
        input = self.swap_pos(input, 4, 0)
        assert input == "ebcda", f'{input} != "ebcda"'
        input = self.swap_letter(input, 'd', 'b')
        assert input == "edcba", f'{input} != "edcba"'
        input = self.reverse(input, 0, 4)
        assert input == "abcde", f'{input} != "abcde"'
        input = self.rotate_left(input, 1)
        assert input == "bcdea", f'{input} != "bcdea"'
        input = self.move(input, 1, 4)
        assert input == "bdeac", f'{input} != "bdeac"'
        input = self.move(input, 3, 0)
        assert input == "abdec", f'{input} != "abdec"'
        input = self.rotate_index(input, 'b')
        assert input == "ecabd", f'{input} != "ecabd"'
        input = self.rotate_index(input, 'd')
        assert input == "decab", f'{input} != "decab"'

        input = "decab"
        input = self.r_rotate_index(input, 'd')
        assert input == "ecabd", f'{input} != "ecabd"'
        input = self.r_rotate_index(input, 'b')
        assert input == "abdec", f'{input} != "abdec"'
        input = self.r_move(input, 3, 0)
        assert input == "bdeac", f'{input} != "bdeac"'
        input = self.r_move(input, 1, 4)
        assert input == "bcdea", f'{input} != "bcdea"'
        input = self.rotate_right(input, 1)
        assert input == "abcde", f'{input} != "abcde"'
        input = self.reverse(input, 0, 4)
        assert input == "edcba", f'{input} != "edcba"'
        input = self.swap_letter(input, 'd', 'b')
        assert input == "ebcda", f'{input} != "ebcda"'
        input = self.swap_pos(input, 4, 0)
        assert input == "abcde", f'{input} != "abcde"'

        assert self.swap_pos(self.swap_pos("abcdef", 1, 2), 1, 2) == "abcdef", "swap_pos reverse (swap_pos) failed"
        assert self.swap_letter(self.swap_letter("abcdef", 'a', 'b'), 'a', 'b') == "abcdef", "swap_letter reverse (swap_letter) failed"
        assert self.rotate_right(self.rotate_left("abcdef", 1), 1) == "abcdef", "rotate_left reverse (rotate_right) failed"
        assert self.rotate_left(self.rotate_right("abcdef", 1), 1) == "abcdef", "rotate_right reverse (rotate_left) failed"
        assert self.r_rotate_index(self.rotate_index("abcdef", 'a'), 'a') == "abcdef", "rotate_index reverse (r_rotate_index) failed"
        assert self.reverse(self.reverse("abcdef", 1, 2), 1, 2) == "abcdef", "reverse reverse (reverse) failed"
        assert self.r_move(self.move("abcdef", 1, 2), 1, 2) == "abcdef", "move reverse (r_move) failed"

        assert self.rotate_right(self.rotate_left("abcdef", 8), 8) == "abcdef", "rotate_left reverse (rotate_right) failed"
        assert self.rotate_left(self.rotate_right("abcdef", 8), 8) == "abcdef", "rotate_right reverse (rotate_left) failed"
        assert self.r_rotate_index(self.rotate_index("abcdef", 'f'), 'f') == "abcdef", "rotate_index reverse (r_rotate_index) failed"
        assert self.r_move(self.move("abcdef", 4, 1), 4, 1) == "abcdef", "move reverse (r_move) failed"

    def common(self, input_data):
        self.instructions = []
        for line in input_data:
            for option in self.func_map.keys():
                if m := re.match(option, line):
                    self.instructions.append((self.func_map[option], m.groups()))
                    break
            else:
                raise ValueError(f"No option found for '{line}'")

    def part1(self, input_data):
        password = "abcdefgh"
        self.debug(password)
        for instruction, params in self.instructions:
            if instruction[0] == 'i':
                params = list(map(int, params))
            password = instruction[1](self, password, *params)
            self.debug(password)
        yield password

    def part2(self, input_data):
        password = "fbgdceah"
        self.debug(password)
        for instruction, params in reversed(self.instructions):
            if instruction[0] == 'i':
                params = list(map(int, params))
            password = instruction[2](self, password, *params)
            self.debug(password)
        yield password
