import bisect
import typing

from . import _base


class Bracket(str):
    _KNOWN_BRACKETS = {'(', ')', '{', '}', '<', '>', '[', ']'}
    _OPEN_CLOSED_MAP = typing.cast(
        dict['Bracket', 'Bracket'],
        {
            '(': ')',
            '{': '}',
            '<': '>',
            '[': ']',
        },
    )

    def __init__(self, char: str) -> None:
        if len(char) != 1:
            raise ValueError(f'{char} is not one char!')
        if char not in self._KNOWN_BRACKETS:
            raise ValueError(f'{char} is not a bracket!')
        super().__init__()

    @property
    def is_open(self) -> bool:
        return self in self._OPEN_CLOSED_MAP.keys()

    def is_paired_to(self, other: typing.Any) -> bool:
        if not isinstance(other, Bracket):
            raise ValueError("A bracket cannot be paired to a non-bracket")
        return self.pair == other

    @property
    def pair(self) -> 'Bracket':
        return self._OPEN_CLOSED_MAP[self]


class IncorrectBucketSequence(Exception):
    pass


class Corrupted(IncorrectBucketSequence):
    def __init__(self, unexpected_bracket: Bracket) -> None:
        self.unexpected_bracket = unexpected_bracket


class Incomplete(IncorrectBucketSequence):
    def __init__(self, open_brackets: list[Bracket]) -> None:
        self.closing_brackets = [b.pair for b in reversed(open_brackets)]


class Solver(_base.BaseSolver):
    _INPUT_FILENAME = 'brackets.debug'

    @staticmethod
    def _preprocess_line(line: str) -> typing.Iterator[Bracket]:
        return (Bracket(char) for char in line)

    @staticmethod
    def validate_bracket_line(line: typing.Iterator[Bracket]) -> None:
        open_brackets: list[Bracket] = []
        for bracket in line:
            if bracket.is_open:
                open_brackets.append(bracket)
                continue
            if open_brackets[-1].is_paired_to(bracket):
                open_brackets.pop()
                continue
            raise Corrupted(unexpected_bracket=bracket)
        if open_brackets:
            raise Incomplete(open_brackets=open_brackets)

    def solve1(self) -> int:
        SCORES_MAP = {
            ')': 3,
            ']': 57,
            '}': 1197,
            '>': 25137,
        }

        score = 0
        for line in self._input:
            try:
                self.validate_bracket_line(line)
            except Corrupted as corrupted:
                score += SCORES_MAP[corrupted.unexpected_bracket]
            except IncorrectBucketSequence:
                continue

        return score

    def solve2(self) -> int:
        SCORES_MAP = {
            ')': 1,
            ']': 2,
            '}': 3,
            '>': 4,
        }

        scores: list[int] = []
        for line in self._input:
            try:
                self.validate_bracket_line(line)
            except Incomplete as incomplete:
                score = 0
                for closing_bracket in incomplete.closing_brackets:
                    score = score * 5 + SCORES_MAP[closing_bracket]
                bisect.insort(scores, score)
            except IncorrectBucketSequence:
                pass

        return scores[len(scores) // 2]
