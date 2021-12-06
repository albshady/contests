import typing

from . import _base


class Command(typing.NamedTuple):
    direction: str
    distance: int


class Solver(_base.BaseSolver):
    _INPUT_FILENAME = 'commands.txt'

    @staticmethod
    def _preprocess_line(line: str) -> Command:
        direction, distance = line.split()
        return Command(direction=direction, distance=int(distance))

    def solve1(self) -> int:
        """In the first task we are moving straighforward"""

        horizontal = 0
        depth = 0

        for command in self._input:
            match command.direction:
                case 'forward':
                    horizontal += command.distance
                case 'up':
                    depth -= command.distance
                case 'down':
                    depth += command.distance
                case other:
                    raise ValueError(f"Unknown direction: {other}")

        return horizontal * depth

    def solve2(self) -> int:
        """In the second task we are considering aim when moving"""

        horizontal = 0
        depth = 0
        aim = 0

        for command in self._input:
            match command.direction:
                case 'forward':
                    horizontal += command.distance
                    depth += aim * command.distance
                case 'up':
                    aim -= command.distance
                case 'down':
                    aim += command.distance
                case other:
                    raise ValueError(f"Unknown direction: {other}")

        return horizontal * depth
