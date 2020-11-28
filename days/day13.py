from typing import Optional

from days import AOCDay, day


@day(13)
class Day13(AOCDay):
    input = 0
    start = (1, 1)
    target = (0, 0)

    def common(self, input_data):
        self.input = int(input_data)

    def is_wall(self, x, y):
        val = (x * x + 3 * x + 2 * x * y + y + y * y) + self.input
        bits = [int(x) for x in "{:b}".format(val)]

        return sum(bits) % 2 == 1

    def manhattan_distance(self, source, target):
        return sum(abs(x - y) for x, y in zip(source, target))

    def possible_moves(self, position):
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neigh_pos = [(position[0] - neigh[0], position[1] - neigh[1]) for neigh in neighbors]
        return [x for x in neigh_pos if x[0] >= 0 and x[1] >= 0 and not self.is_wall(x[0], x[1])]

    def find_path(self) -> Optional[int]:
        # Breath first search
        visited = []
        queue = [self.start]
        parents = {}

        if self.start == self.target:
            return 0

        while queue:
            node = queue.pop(0)
            if node not in visited:
                visited.append(node)

                if node == self.target:
                    path = []
                    while node != self.start:
                        path.append(node)
                        node = parents[node]
                    return len(list(reversed(path)))

                neighbours = self.possible_moves(node)
                for neighbour in neighbours:
                    if neighbour not in visited and neighbour not in queue:
                        parents[neighbour] = node
                        queue.append(neighbour)
        return None

    def part1(self, input_data):
        self.target = (31, 39)

        path = self.find_path()
        yield path

    def part2(self, input_data):
        num_reachable = 0
        for y in range(51):
            self.debug(f"y = {y}/51")
            for x in range(51):
                if not self.is_wall(x, y):
                    self.target = (x, y)
                    distance = self.find_path()
                    if distance is not None and distance <= 50:
                        num_reachable += 1
        yield num_reachable
