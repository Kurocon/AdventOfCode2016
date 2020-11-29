from days import AOCDay, day


@day(18)
class Day18(AOCDay):
    def is_safe(self, prev_row, index):
        l = (prev_row[index - 1] if index - 1 >= 0 else ".") == "."
        c = prev_row[index] == "."
        r = (prev_row[index + 1] if index + 1 < len(prev_row) else ".") == "."

        return (l, c, r) not in [
            (True, True, False),  # L C ^R
            (False, True, True),  # ^L C R
            (True, False, False),  # L ^C ^R
            (False, False, True),  # ^L ^C R
        ]

    def next_row(self, prev_row):
        return "".join("." if self.is_safe(prev_row, i) else "^" for i in range(len(prev_row)))

    def get_maze(self, first_row, size):
        maze = [first_row]
        for _ in range(size - 1):
            maze.append(self.next_row(maze[-1]))
        return maze

    def count_safe(self, maze):
        return sum(sum(1 if x == "." else 0 for x in row) for row in maze)

    def test(self, input_data):
        assert self.next_row("..^^.") == ".^^^^", f'{self.next_row("..^^.")} != ".^^^^"'
        assert self.next_row(".^^^^") == "^^..^", f'{self.next_row(".^^^^")} != "^^..^"'

        assert self.next_row(".^^.^.^^^^") == "^^^...^..^", f'{self.next_row(".^^.^.^^^^")} != "^^^...^..^"'
        assert self.next_row("^^^...^..^") == "^.^^.^.^^.", f'{self.next_row("^^^...^..^")} != "^.^^.^.^^."'
        assert self.next_row("^.^^.^.^^.") == "..^^...^^^", f'{self.next_row("^.^^.^.^^.")} != "..^^...^^^"'
        assert self.next_row("..^^...^^^") == ".^^^^.^^.^", f'{self.next_row("..^^...^^^")} != ".^^^^.^^.^"'
        assert self.next_row(".^^^^.^^.^") == "^^..^.^^..", f'{self.next_row(".^^^^.^^.^")} != "^^..^.^^.."'
        assert self.next_row("^^..^.^^..") == "^^^^..^^^.", f'{self.next_row("^^..^.^^..")} != "^^^^..^^^."'
        assert self.next_row("^^^^..^^^.") == "^..^^^^.^^", f'{self.next_row("^^^^..^^^.")} != "^..^^^^.^^"'
        assert self.next_row("^..^^^^.^^") == ".^^^..^.^^", f'{self.next_row("^..^^^^.^^")} != ".^^^..^.^^"'
        assert self.next_row(".^^^..^.^^") == "^^.^^^..^^", f'{self.next_row(".^^^..^.^^")} != "^^.^^^..^^"'

        assert self.get_maze("..^^.", 3) == ["..^^.", ".^^^^", "^^..^"]
        assert self.get_maze(".^^.^.^^^^", 10) == [".^^.^.^^^^", "^^^...^..^", "^.^^.^.^^.", "..^^...^^^",
                                                   ".^^^^.^^.^", "^^..^.^^..", "^^^^..^^^.", "^..^^^^.^^",
                                                   ".^^^..^.^^", "^^.^^^..^^"]

        assert self.count_safe(self.get_maze("..^^.", 3)) == 6
        assert self.count_safe(self.get_maze(".^^.^.^^^^", 10)) == 38

    def part1(self, input_data):
        yield self.count_safe(self.get_maze(self.input_data, 40))

    def part2(self, input_data):
        yield self.count_safe(self.get_maze(self.input_data, 400000))
