from days import AOCDay, day


@day(3)
class Day3(AOCDay):
    triangles = []

    def common(self, input_data):
        self.triangles = []

    def part1(self, input_data):
        for line in input_data:
            self.triangles.append(tuple(int(x) for x in line.split()))
        possible = 0
        for triangle in self.triangles:
            if all([
                triangle[0] + triangle[1] > triangle[2],
                triangle[0] + triangle[2] > triangle[1],
                triangle[1] + triangle[2] > triangle[0],
                triangle[1] + triangle[0] > triangle[2],
                triangle[2] + triangle[1] > triangle[0],
                triangle[2] + triangle[0] > triangle[1]
            ]):
                possible += 1
        yield possible

    def part2(self, input_data):
        ind = 0
        while ind < len(input_data):
            l1 = tuple(int(x) for x in input_data[ind].split())
            l2 = tuple(int(x) for x in input_data[ind + 1].split())
            l3 = tuple(int(x) for x in input_data[ind + 2].split())

            self.triangles.append((l1[0], l2[0], l3[0]))
            self.triangles.append((l1[1], l2[1], l3[1]))
            self.triangles.append((l1[2], l2[2], l3[2]))

            ind += 3

        possible = 0
        for triangle in self.triangles:
            if all([
                triangle[0] + triangle[1] > triangle[2],
                triangle[0] + triangle[2] > triangle[1],
                triangle[1] + triangle[2] > triangle[0],
                triangle[1] + triangle[0] > triangle[2],
                triangle[2] + triangle[1] > triangle[0],
                triangle[2] + triangle[0] > triangle[1]
            ]):
                possible += 1
        yield possible

