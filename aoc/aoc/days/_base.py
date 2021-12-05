import abc
import typing

from aoc import config


class BaseSolver:
    _INPUT_FILENAME: str

    def __init__(self) -> None:
        self._input_filepath = config.DATA_DIR / self._INPUT_FILENAME

    def solve(self, task: int) -> int:
        match task:
            case 1:
                return self.solve1()
            case 2:
                return self.solve2()
            case _:
                raise RuntimeError

    @abc.abstractmethod
    def solve1(self) -> int:
        ...

    @abc.abstractmethod
    def solve2(self) -> int:
        ...

    @property
    def _input(self) -> typing.Iterator[typing.Any]:
        with open(self._input_filepath, 'r') as input_file:
            for line in input_file:
                yield self._preprocess_line(line=line.strip())

    @staticmethod
    def _preprocess_line(line: str) -> typing.Any:
        return line
