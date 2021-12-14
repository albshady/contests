import collections
import typing

from . import _base


class Rule(typing.NamedTuple):
    pair: str
    insertion: str


class Solver(_base.BaseSolver):
    _INPUT_FILENAME = 'polymer.txt'

    def __init__(self) -> None:
        super().__init__()
        self.rules = {}
        for line in self._input:
            if isinstance(line, str):
                self.polymer = line
            elif isinstance(line, Rule):
                self.rules[line.pair] = line.insertion

    @property
    def polymer_pairs(self) -> typing.Iterator[str]:
        for offset in range(len(self.polymer) - 1):
            yield self.polymer[offset : offset + 2]

    @staticmethod
    def _preprocess_line(line: str) -> str | Rule | None:
        if not line:
            return None

        if '->' not in line:
            return line

        pair, _, insertion = line.partition('->')
        return Rule(pair=pair.strip(), insertion=insertion.strip())

    def solve1(self) -> int:
        return self.calculate_difference_after(steps=10)

    def solve2(self) -> int:
        return self.calculate_difference_after(steps=10)

    def calculate_difference_after(self, steps: int) -> int:
        pairs = collections.Counter(self.polymer_pairs)

        for step in range(steps):
            pairs = self.do_step(pairs)

        return self.calculate_difference_between_most_common_and_least_common(pairs)

    def do_step(self, pairs: typing.Counter[str]) -> typing.Counter[str]:
        new_pairs = collections.Counter()

        for pair, count in pairs.items():
            if to_insert := self.rules[pair]:
                new_pairs[f'{pair[0]}{to_insert}'] += count
                new_pairs[f'{to_insert}{pair[1]}'] += count

        return new_pairs

    def calculate_difference_between_most_common_and_least_common(
        self, pairs: collections.Counter[str]
    ) -> int:
        counter: typing.Counter[str] = collections.Counter()
        for pair, count in pairs.items():
            for letter in pair:
                counter[letter] += count / 2
        counter[self.polymer[1]] += 0.5
        counter[self.polymer[-1]] += 0.5
        return int(counter.most_common()[0][1] - counter.most_common()[-1][1])
