import typing

from ._base import BaseSolver


ALL_SEGMENTS = 'abcdefg'

SEGMENTS = {
    0: 'abcefg',
    1: 'cf',
    2: 'acdeg',
    3: 'acdfg',
    4: 'bcdf',
    5: 'abdfg',
    6: 'abdefg',
    7: 'acf',
    8: ALL_SEGMENTS,
    9: 'abcdfg',
}


class Display(typing.NamedTuple):
    digits: list[int]

    @property
    def value(self) -> int:
        return int(''.join(map(str, self.digits)))

    @property
    def with_unique_number_of_segments(self) -> int:
        return len([digit for digit in self.digits if digit in (1, 4, 7, 8)])

    @classmethod
    def from_line(cls, line: str) -> 'Display':
        pattern_input, control_input = line.strip().split('|')
        patterns = {''.join(sorted(pattern)) for pattern in pattern_input.split()}
        digits_map = cls.decode_digits(patterns=patterns)

        digits = [digits_map[''.join(sorted(p))] for p in control_input.split()]
        return cls(digits=digits)

    @classmethod
    def decode_digits(cls, patterns: set[str]) -> dict[str, int]:
        for pattern in patterns:
            match len(pattern):
                case 2:
                    cf = pattern
                case 3:
                    acf = pattern
                case 4:
                    bcdf = pattern

        c, f = cf
        a = acf.replace(c, '').replace(f, '')
        b, d = bcdf.replace(c, '').replace(f, '')
        e, g = [letter for letter in ALL_SEGMENTS if letter not in bcdf + a]
        if ALL_SEGMENTS.replace(g, '') in patterns:  # 9
            e, g = g, e
        if ALL_SEGMENTS.replace(d, '').replace(e, '') in patterns:  # 3
            b, d = d, b
        if ALL_SEGMENTS.replace(f, '') in patterns:  # 6
            c, f = f, c

        return cls.build_pattern_digit_map(a=a, b=b, c=c, d=d, e=e, f=f, g=g)

    @staticmethod
    def build_pattern_digit_map(**segments: str) -> dict[str, int]:
        return {''.join(sorted(segments[s] for s in SEGMENTS[d])): d for d in range(10)}


class Solver(BaseSolver):
    _INPUT_FILENAME = 'segments.txt'
    _input: typing.Iterator[Display]

    @staticmethod
    def _preprocess_line(line: str) -> Display:
        return Display.from_line(line=line)

    def solve1(self) -> int:
        return sum(display.with_unique_number_of_segments for display in self._input)

    def solve2(self) -> int:
        return sum(display.value for display in self._input)
