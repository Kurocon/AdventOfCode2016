import re

from days import AOCDay, day


@day(7)
class Day7(AOCDay):

    test_input = """abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn"""

    test_input2 = """aba[bab]xyz
xyx[xyx]xyx
aaa[kek]eke
zazbz[bzb]cdb"""

    addresses = []

    ADDR_RE = re.compile("(?:(?P<outside>[^\[\]][a-z]+[^\[\]])|\[(?P<inside>[a-z]+)\])")
    ABBA_RE = re.compile("(?P<a>[a-z])(?P<b>[a-z])(?P=b)(?P=a)")
    ABA_M_RE = re.compile("(?=(?P<a>[a-z])[a-z](?P=a))")
    ABA_RE = re.compile("(?P<a>[a-z])[a-z](?P=a)")

    def common(self, input_data):
        self.addresses = []
        for address in input_data:
            inside = []
            outside = []
            rx = self.ADDR_RE.findall(address)
            for x in rx:
                if x[0]:
                    outside.append(x[0])
                if x[1]:
                    inside.append(x[1])
            self.addresses.append((outside, inside))

    def has_abba(self, string):
        match = self.ABBA_RE.search(string)
        return match and len(list(set(match.group(0)))) > 1

    def supports_tls(self, address):
        outside_has_abba = any(self.has_abba(x) for x in address[0])
        inside_has_abba = any(self.has_abba(x) for x in address[1])
        return outside_has_abba and not inside_has_abba

    def supports_ssl(self, address):
        for part in address[0]:

            for m in self.ABA_M_RE.finditer(part):
                match = self.ABA_RE.search(part[m.start():])
                if match and len(list(set(match.group(0)))) > 1:
                    aba = match.group(0)
                    bab = (aba + aba[1:])[1:4]
                    if any(bab in x for x in address[1]):
                        return True

    def part1(self, input_data):
        yield len(list(filter(lambda x: self.supports_tls(x), self.addresses)))


    def part2(self, input_data):
        yield len(list(filter(lambda x: self.supports_ssl(x), self.addresses)))
