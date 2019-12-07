from typing import Dict, Tuple, Optional

from days import AOCDay, day


DEBUG = False


class Unit:
    id = None

    def __init__(self, id):
        self.id = id

    def put(self, value):
        raise NotImplementedError()

    def step(self, target_low=None, target_high=None) -> Tuple[bool, bool]:
        raise NotImplementedError()


class Input(Unit):
    id = None
    value = None
    output: Unit = None

    def __str__(self):
        return "Input ({}) => {} {}".format(self.value, type(self.output), self.output.id)

    def put(self, value):
        self.value = value

    def step(self, target_low=None, target_high=None):
        if self.output is not None and self.value is not None:
            if DEBUG:
                print("Input gives value {} to {} {}".format(self.value, type(self.output), self.output.id))
            self.output.put(self.value)
            self.value = None
            return True, False
        return False, False


class Output(Unit):
    id = None
    values = []

    def __init__(self, id):
        super(Output, self).__init__(id)
        self.values = []

    def __str__(self):
        return "Output #{}".format(self.id)

    def put(self, value):
        self.values.append(value)

    def step(self, target_low=None, target_high=None):
        return False, False


class Bot(Unit):
    id = None
    microchips = []
    low_output: Optional[Unit] = None
    high_output: Optional[Unit] = None

    def __init__(self, id):
        super(Bot, self).__init__(id)
        self.microchips = []
        self.low_output = None
        self.high_output = None

    def __str__(self):
        return "Bot #{}, low => {} {}, high => {} {}".format(self.id, type(self.low_output), self.low_output.id, type(self.high_output), self.high_output.id)

    def put(self, value):
        self.microchips.append(value)

    def step(self, target_low=None, target_high=None):
        if len(self.microchips) == 2:
            minval, maxval = min(self.microchips), max(self.microchips)
            self.low_output.put(minval)
            self.high_output.put(maxval)
            if DEBUG:
                print("Bot {} gives low value {} to {} {} and high value {} to {} {}".format(
                    self.id,
                    minval, type(self.low_output), self.low_output.id,
                    maxval, type(self.high_output), self.high_output.id
                ))
            self.microchips = []
            if minval == target_low and maxval == target_high:
                return True, True
            else:
                return True, False
        return False, False


@day(10)
class Day10(AOCDay):
    test_input = """value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2""".split("\n")

    inputs: Dict[int, Input] = {}
    bots: Dict[int, Bot] = {}
    outputs: Dict[int, Output] = {}

    def common(self, input_data):
        # input_data = self.test_input
        self.inputs = {}
        self.bots = {}
        self.outputs = {}
        for fullline in input_data:
            line = fullline.split(" ")
            if line[0] == "value":
                value = int(line[1])
                bot = int(line[5])
                if bot not in self.bots.keys():
                    self.bots[bot] = Bot(bot)
                if value not in self.inputs.keys():
                    self.inputs[value] = Input(None)
                    self.inputs[value].value = value
                    self.inputs[value].output = self.bots[bot]
            elif line[0] == "bot":
                src_bot = int(line[1])
                if src_bot not in self.bots.keys():
                    self.bots[src_bot] = Bot(src_bot)

                # Low output
                target = int(line[6])
                if line[5] == "bot":
                    if target not in self.bots.keys():
                        self.bots[target] = Bot(target)
                    self.bots[src_bot].low_output = self.bots[target]
                elif line[5] == "output":
                    if target not in self.outputs.keys():
                        self.outputs[target] = Output(target)
                    self.bots[src_bot].low_output = self.outputs[target]
                else:
                    raise ValueError("Unknown low out in line "+fullline)

                # High output
                target = int(line[11])
                if line[10] == "bot":
                    if target not in self.bots.keys():
                        self.bots[target] = Bot(target)
                    self.bots[src_bot].high_output = self.bots[target]
                elif line[10] == "output":
                    if target not in self.outputs.keys():
                        self.outputs[target] = Output(target)
                    self.bots[src_bot].high_output = self.outputs[target]
                else:
                    raise ValueError("Unknown high out in line "+fullline)
            else:
                raise ValueError("Unknown line "+fullline)

    def part1(self, input_data):
        target_low, target_high = 17, 61
        while True:
            actioned = False
            target_reached = False
            for input in self.inputs.values():
                action, target_reached = input.step(target_low, target_high)
                actioned = actioned or action
            for bot in self.bots.values():
                action, target_reached = bot.step(target_low, target_high)
                if target_reached:
                    yield bot.id
                    break
                actioned = actioned or action
            if target_reached:
                break
            for output in self.outputs.values():
                action, target_reached = output.step(target_low, target_high)
                actioned = actioned or action
            if not actioned:
                # Complete
                if DEBUG:
                    print("Done!")
                break

    def part2(self, input_data):
        while True:
            actioned = False
            target_reached = False
            for input in self.inputs.values():
                action, target_reached = input.step()
                actioned = actioned or action
            for bot in self.bots.values():
                action, target_reached = bot.step()
                actioned = actioned or action
            for output in self.outputs.values():
                action, target_reached = output.step()
                actioned = actioned or action
            if not actioned:
                # Complete
                if DEBUG:
                    print("Done!")
                break

        yield self.outputs[0].values[0] * self.outputs[1].values[0] * self.outputs[2].values[0]