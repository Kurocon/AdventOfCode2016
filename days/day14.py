import re
from hashlib import md5

from defaultlist import defaultlist

from days import AOCDay, day


@day(14)
class Day14(AOCDay):
    test_input = "abc"

    THREE_SAME = re.compile(r"(.)\1\1")

    hash_cache = defaultlist()

    def has_triplet(self, s):
        return self.THREE_SAME.search(s)

    def stretch_hash(self, hash):
        for _ in range(2016):
            hash = md5(hash.encode("utf-8")).hexdigest()
        return hash

    def common(self, input_data):
        if isinstance(self.input_data, str):
            self.input_data = self.input_data.encode("utf-8")
        self.hash_cache = defaultlist()

    def part1(self, input_data):
        index = 0
        found_keys = []
        while len(found_keys) < 64:
            if self.hash_cache[index] is None:
                self.hash_cache[index] = md5(self.input_data + str(index).encode("utf-8")).hexdigest()
            hash = self.hash_cache[index]
            if c := self.has_triplet(hash):
                for i in range(1, 1001):
                    if self.hash_cache[index+i] is None:
                        self.hash_cache[index+i] = md5(self.input_data + str(index+i).encode("utf-8")).hexdigest()
                    hash2 = self.hash_cache[index+i]
                    if f"{c.group(1)}{c.group(1)}{c.group(1)}{c.group(1)}{c.group(1)}" in hash2:
                        self.debug(f"#{len(found_keys)+1}")
                        self.debug(f"3 -- {index}: {hash}")
                        self.debug(f"5 -- {index+i}: {hash2}")
                        found_keys.append((index, index+i, hash))
                        break  # Break from for loop
            index += 1

        yield found_keys[-1][0]

    def part2(self, input_data):
        index = 0
        found_keys = []
        while len(found_keys) < 64:
            if self.hash_cache[index] is None:
                self.hash_cache[index] = self.stretch_hash(md5(self.input_data + str(index).encode("utf-8")).hexdigest())
            hash = self.hash_cache[index]
            if c := self.has_triplet(hash):
                five_same_re = re.compile(f".*{c.group(1)}{c.group(1)}{c.group(1)}{c.group(1)}{c.group(1)}.*")
                for i in range(1, 1001):
                    if self.hash_cache[index+i] is None:
                        self.hash_cache[index+i] = self.stretch_hash(md5(self.input_data + str(index+i).encode("utf-8")).hexdigest())
                    hash2 = self.hash_cache[index+i]
                    if f"{c.group(1)}{c.group(1)}{c.group(1)}{c.group(1)}{c.group(1)}" in hash2:
                        self.debug(f"#{len(found_keys)+1}")
                        self.debug(f"3 -- {index}: {hash}")
                        self.debug(f"5 -- {index+i}: {hash2}")
                        found_keys.append((index, index+i, hash))
                        break  # Break from for loop
            index += 1

        yield found_keys[-1][0]
