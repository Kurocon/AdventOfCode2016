import networkx as nx
from itertools import permutations

from days import AOCDay, day

WALL = "#"
EMPTY = "."


@day(24)
class Day24(AOCDay):
    test_input = """###########
#0.1.....2#
#.#######.#
#4.......3#
###########""".split("\n")

    graph = None
    poi_coords = []
    max_poi = None
    distances = {}

    def common(self, input_data):
        # input_data = self.test_input
        self.poi_coords = {}
        self.distances = {}

        max_x = len(input_data[0])
        max_y = len(input_data)
        self.graph = nx.generators.grid_2d_graph(max_y, max_x)

        # Remove walls from the graph, find points of interest and start position
        poi_ids = []
        for y, row in enumerate(input_data):
            for x, val in enumerate(row):
                if val == "#":
                    self.graph.remove_node((y, x))
                if val not in "#.":
                    poi_ids.append(int(val))
                    self.poi_coords[int(val)] = (y, x)

        # Find highest POI number
        self.max_poi = max(poi_ids)

        # Calculate shortest paths between all points of interest pairs
        for p1 in range(self.max_poi + 1):
            for p2 in range(self.max_poi + 1):
                self.distances[p1, p2] = nx.shortest_path_length(self.graph, self.poi_coords[p1], self.poi_coords[p2])
                self.distances[p2, p1] = self.distances[p1, p2]

    def part1(self, input_data):
        shortest = -1
        for path in permutations(range(1, self.max_poi + 1)):
            full_path = [0] + list(path)
            path_distance = 0
            self.debug(f"Path {full_path}:")
            for i in range(len(path)):
                self.debug(f"  {full_path[i]}-{full_path[i+1]}: {self.distances[full_path[i+1], full_path[i]]}")
                path_distance += self.distances[full_path[i+1], full_path[i]]
            if shortest > 0:
                shortest = min(path_distance, shortest)
            else:
                shortest = path_distance
            self.debug(f"Shortest: {shortest}")
        yield shortest

    def part2(self, input_data):
        shortest = -1
        for path in permutations(range(1, self.max_poi + 1)):
            full_path = [0] + list(path) + [0]
            path_distance = 0
            for i in range(len(path) + 1):
                path_distance += self.distances[full_path[i+1], full_path[i]]
            if shortest > 0:
                shortest = min(path_distance, shortest)
            else:
                shortest = path_distance
        yield shortest
