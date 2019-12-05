import re
from collections import Counter

from days import AOCDay, day


@day(4)
class Day4(AOCDay):
    test_input = """aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]"""

    ROOM_REGEX = re.compile("(?P<name>[a-z-]+)-(?P<sector_id>[0-9]+)\[(?P<checksum>[a-z]{5})\]")

    rooms = []

    def common(self, input_data):
        # input_data = self.test_input.split("\n")
        for line in input_data:
            rx = self.ROOM_REGEX.match(line)
            self.rooms.append([rx.group('name').replace("-", ""), int(rx.group('sector_id')), rx.group('checksum'), rx.group('name')])

    def is_real(self, room):
        counter = Counter(sorted(room[0]))
        common = "".join(x[0] for x in counter.most_common(5))
        return common == room[2]

    def part1(self, input_data):
        yield sum(x[1] for x in self.rooms if self.is_real(x))


    def rotate(self, text, amount):
        return "".join(" " if text[i] == "-" else chr((ord(text[i]) + amount - 97) % 26 + 97) for i in range(len(text)))


    def part2(self, input_data):
        real_rooms = filter(self.is_real, self.rooms)
        names = [(self.rotate(x[3], x[1]), x[1]) for x in real_rooms]
        yield list(set(x[1] for x in names if "north" in x[0]))[0]
