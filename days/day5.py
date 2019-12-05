import hashlib

from days import AOCDay, day


@day(5)
class Day5(AOCDay):
    test_input = "abc"
    int_index = 0

    def common(self, input_data):
        self.int_index = 0

    def part1(self, input_data):
        password = ""

        for i in range(8):
            hash = None
            while hash is None or hash[0:5] != "00000":
                self.int_index += 1
                hash = hashlib.md5("{}{}".format(input_data, self.int_index).encode()).hexdigest()
            password += hash[5]
        yield password

    def part2(self, input_data):
        password = ['_', '_', '_', '_', '_', '_', '_', '_']

        while "_" in password:
            hash = None
            while hash is None or hash[0:5] != "00000":
                self.int_index += 1
                hash = hashlib.md5("{}{}".format(input_data, self.int_index).encode()).hexdigest()
            try:
                if int(hash[5]) < 8 and password[int(hash[5])] == "_":
                    password[int(hash[5])] = hash[6]
                    print("".join(password))
            except ValueError:
                pass
        yield "".join(password)
