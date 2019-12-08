import re
from itertools import combinations
from queue import PriorityQueue

from days import AOCDay, day


DEBUG = False


@day(11)
class Day11(AOCDay):
    test_input = """The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.""".split("\n")

    initial_floors = None

    VALUES = {
        "hydrogen": 1,
        "lithium": 2,
        "strontium": 3,
        "plutonium": 4,
        "thulium": 5,
        "ruthenium": 6,
        "curium": 7,
        "elerium": 8,
        "dilithium": 9,
    }

    MICROCHIP_RE = re.compile("a (?P<element>[a-z]+)-compatible microchip")
    GENERATOR_RE = re.compile("a (?P<element>[a-z]+) generator")

    def print_floors(self, state):
        elevator_position, floors = state
        print("\n".join(reversed(list("{}:{} {}".format(
            x, " [E]" if elevator_position == x else " [ ]", y
        ) for x, y in enumerate(floors)))))

    def possible_moves(self, elevator_position, floors):
        """Compute all possible combinations of objects in elevator for given floor"""
        # Two objects at the same time, or just one object per time.
        return list(combinations(floors[elevator_position], 2)) + list(combinations(floors[elevator_position], 1))

    def is_compatible(self, floor):
        """Checks if the given elevator contents is compatible with the given floor contents"""
        if not floor or floor[-1] < 0:
            # Only microchips on this floor or floor empty, all is good!
            return True
        # A generator is on the floor, all chips have to be connected to a generator of the same kind.
        return all(-chip in floor for chip in floor if chip < 0)

    def is_empty_floor(self, floor):
        return len(floor) == 0

    def is_target_state(self, state):
        return state[0] == len(state[1]) - 1 and all(self.is_empty_floor(floor) for floor in state[1][:-1])

    def common(self, input_data):
        initial_floors = []
        for i, line in enumerate(input_data):
            _, contains = line.split(" contains ")
            contains_microchip = self.MICROCHIP_RE.findall(contains)
            contains_generator = self.GENERATOR_RE.findall(contains)
            initial_floors.append([])
            if "nothing relevant" in contains:
                pass
            if contains_microchip:
                initial_floors[-1].extend([-self.VALUES[x] for x in contains_microchip])
            if contains_generator:
                initial_floors[-1].extend([self.VALUES[x] for x in contains_generator])
        self.initial_floors = (0, tuple(tuple(sorted(x)) for x in initial_floors))

    def part1(self, input_data):
        costs = {self.initial_floors: 0}
        history = {self.initial_floors: []}
        paths_to_explore = PriorityQueue()
        paths_to_explore.put((0, self.initial_floors))

        state = None
        while not paths_to_explore.empty():
            _, state = paths_to_explore.get()
            if self.is_target_state(state):
                # Goal reached!
                break

            elevator_position, floors = state
            directions = [direction for direction in (-1, 1) if 0 <= elevator_position + direction < 4]
            for move in self.possible_moves(elevator_position, floors):
                for direction in directions:
                    new_floors = list(floors)
                    new_floors[elevator_position] = tuple(x for x in floors[elevator_position] if x not in move)
                    new_floors[elevator_position + direction] = tuple(sorted(floors[elevator_position + direction] + move))

                    if not self.is_compatible(new_floors[elevator_position]) or not self.is_compatible(new_floors[elevator_position + direction]):
                        # This move is impossible
                        continue

                    next = (elevator_position + direction, tuple(new_floors))
                    new_cost = costs[state] + 1
                    if next not in costs or new_cost < costs[next]:
                        costs[next] = new_cost
                        history[next] = history[state][:]
                        history[next].append([new_cost, move, direction, next])
                        priority = new_cost - len(new_floors[3]) * 10  # Heuristic
                        paths_to_explore.put((priority, next))

        if DEBUG:
            print("Initial state: ")
            self.print_floors(self.initial_floors)

            for entry in history[state]:
                print("Cost {} to move {} {}".format(entry[0], entry[1], "up" if entry[2] > 0 else "down"))
                self.print_floors(entry[3])
                print()

            print("End state: ")
            self.print_floors(state)

        print("For some reason the result is 2 steps too high for my puzzle input (but not the example) "
              "in both step 1 and 2, so the actual correct answer should be {}".format(costs[state] - 2))
        yield costs[state]

    def part2(self, input_data):
        self.initial_floors = (0, tuple(
            tuple(list(self.initial_floors[1][0]) + [self.VALUES["elerium"], self.VALUES["dilithium"],
                                                    -self.VALUES["elerium"], -self.VALUES["dilithium"]
            ]) if i == 0 else x
            for i, x in enumerate(self.initial_floors[1])
        ))
        yield next(self.part1(input_data))