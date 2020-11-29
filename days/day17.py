from functools import lru_cache
from hashlib import md5
from typing import Optional, List, Tuple

from days import AOCDay, day


@day(17)
class Day17(AOCDay):

    print_debug = True

    start = (0, 0, "")
    target = (3, 3)

    def is_open(self, c):
        return c in 'bcdef'

    def possible_moves(self, node) -> List[Tuple[int, int, str]]:
        x, y, code = node
        hash = md5(code.encode("utf-8")).hexdigest()
        u, d, l, r = hash[:4]
        moves = []
        if self.is_open(u) and (y-1) >= 0:
            moves.append((x, y-1, code+"U"))
        if self.is_open(d) and (y+1) < 4:
            moves.append((x, y+1, code+"D"))
        if self.is_open(l) and (x-1) >= 0:
            moves.append((x-1, y, code+"L"))
        if self.is_open(r) and (x+1) < 4:
            moves.append((x+1, y, code+"R"))
        return moves

    def find_path(self) -> Optional[str]:
        # Breath first search
        visited = []
        queue = [self.start]
        parents = {}

        while queue:
            node = queue.pop(0)
            if node not in visited:
                visited.append(node)

                if (node[0], node[1]) == self.target:
                    return node[2][len(self.start[2]):]

                neighbours = self.possible_moves(node)
                for neighbour in neighbours:
                    if neighbour not in visited and neighbour not in queue:
                        parents[neighbour] = node
                        queue.append(neighbour)
        return None

    def find_all_paths(self):
        # Breath first search
        visited = []
        queue = [self.start]
        parents = {}

        if (self.start[0], self.start[1]) == self.target:
            yield self.start[2][len(self.start[2]):]

        while queue:
            node = queue.pop(0)
            if node not in visited:
                visited.append(node)

                if (node[0], node[1]) == self.target:
                    yield node[2][len(self.start[2]):]
                    continue

                neighbours = self.possible_moves(node)
                for neighbour in neighbours:
                    if neighbour not in visited and neighbour not in queue:
                        parents[neighbour] = node
                        queue.append(neighbour)

    def longest_path(self):
        paths = sorted(list(self.find_all_paths()), key=lambda x: len(x))
        return len(paths[-1])

    def test(self, input_data):
        self.start = (0, 0, "ihgpwlah")
        assert self.find_path() == "DDRRRD", f'{self.find_path()} != "DDRRRD"'
        self.start = (0, 0, "kglvqrro")
        assert self.find_path() == "DDUDRLRRUDRD", f'{self.find_path()} != "DDUDRLRRUDRD"'
        self.start = (0, 0, "ulqzkmiv")
        assert self.find_path() == "DRURDRUDDLLDLUURRDULRLDUUDDDRR", f'{self.find_path()} != "DRURDRUDDLLDLUURRDULRLDUUDDDRR"'

        # These take a long time
        # self.start = (0, 0, "ihgpwlah")
        # assert self.longest_path() == 370, f'{self.longest_path()} != 370'
        # self.start = (0, 0, "kglvqrro")
        # assert self.longest_path() == 492, f'{self.longest_path()} != 492'
        # self.start = (0, 0, "ulqzkmiv")
        # assert self.longest_path() == 830, f'{self.longest_path()} != 830'

    def part1(self, input_data):
        self.start = (0, 0, self.input_data)
        yield self.find_path()

    def part2(self, input_data):
        self.start = (0, 0, self.input_data)
        yield self.longest_path()
