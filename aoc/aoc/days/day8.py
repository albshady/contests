import typing

from ._base import BaseSolver


ALL_SEGMENTS = set('abcdefg')


# class Pattern:
#     def __init__(self, value: str) -> None:
#         self.value = ''.join(sorted(value))
#         self.value_set = set(value)
#
#     def __sub__(self, other: Pattern | str) -> 'Pattern':
#         return Pattern(value)


class Display(typing.NamedTuple):
    digits: list[int]

    @property
    def value(self) -> int:
        return int(''.join(map(str, self.digits)))

    @classmethod
    def from_line(cls, line: str) -> 'Display':
        pattern_input, control_input = line.strip().split('|')
        patterns = {''.join(sorted(pattern)) for pattern in pattern_input.split()}
        digits_map = cls.decode_digits(patterns=patterns)

        print(digits_map)
        digits = [digits_map[''.join(sorted(p))] for p in control_input.split()]
        return cls(digits=digits)

    @classmethod
    def decode_digits(cls, patterns: set[str]) -> dict[str, int]:
        print(patterns)
        for pattern in patterns:
            match len(pattern):
                case 2:
                    cf = set(pattern)
                case 3:
                    acf = set(pattern)
                case 4:
                    bcdf = set(pattern)

        a = acf - cf
        eg = ALL_SEGMENTS - bcdf
        if (ALL_SEGMENTS - (g := {eg.pop()})) in patterns:  # 9
            e = eg
        else:
            e, g = g, eg
        bd = bcdf - cf
        if (ALL_SEGMENTS - e - (b := {bd.pop()})) in patterns:  # 3
            d = bd
        else:
            d, b = b, bd
        if (ALL_SEGMENTS - (c := {cf.pop()})) in patterns:  # 6
            f = cf
        else:
            f = c
            c = cf

        return cls.digits_map_from_segments(a, b, c, d, e, f)

    @staticmethod
    def digits_map_from_segments(
        a: set[str], b: set[str], c: set[str], d: set[str], e: set[str], f: set[str]
    ) -> dict[str, int]:
        print(f'{a=},{b=},{c=},{d=},{e=},{f=}')
        return {
            ''.join(sorted(ALL_SEGMENTS - d)): 0,
            ''.join(sorted(c | f)): 1,
            ''.join(sorted(ALL_SEGMENTS - b - f)): 2,
            ''.join(sorted(ALL_SEGMENTS - b - e)): 3,
            ''.join(sorted(b | c | d | f)): 4,
            ''.join(sorted(ALL_SEGMENTS - c - e)): 5,
            ''.join(sorted(ALL_SEGMENTS - c)): 6,
            ''.join(sorted(a | c | f)): 7,
            ''.join(sorted(ALL_SEGMENTS)): 8,
            ''.join(sorted(ALL_SEGMENTS - e)): 9,
        }

    @staticmethod
    def guess_digit_by_length(pattern: str) -> int | None:
        match len(pattern):
            case 2:
                return 1
            case 3:
                return 7
            case 4:
                return 4
            case 7:
                return 8
            case _:
                return None


class Solver(BaseSolver):
    _INPUT_FILENAME = 'segments.txt'

    @staticmethod
    def _preprocess_line(line: str) -> Display:
        return Display.from_line(line=line)

    def solve1(self) -> int:
        digits_with_unique_number_of_segments = 0

        for display in self._input:
            for digit in display.digits:
                if digit in (1, 4, 7, 8):
                    digits_with_unique_number_of_segments += 1

        return digits_with_unique_number_of_segments

    def sovle2(self) -> int:
        print("Running")

        s = 0
        for display in self._input:
            print(display)
            s += display.value
        return s
