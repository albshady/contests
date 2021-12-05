import collections
import re
import typing

from . import _base


VENT_REGEXP = re.compile(r'^(?P<x0>\d*),(?P<y0>\d*) -> (?P<x1>\d*),(?P<y1>\d*)$')


class Coordinate(typing.NamedTuple):
    x: int
    y: int

    def __add__(self, other: typing.Any) -> 'Coordinate':
        if type(self) is not type(other):
            raise ValueError(f"Not able to perform + with {type(other)}")
        return Coordinate(x=self.x + other.x, y=self.y + other.y)


class VentLine(typing.NamedTuple):
    x0: int
    y0: int
    x1: int
    y1: int

    @property
    def is_straight(self) -> bool:
        return self.x0 == self.x1 or self.y0 == self.y1

    @property
    def covered_coordinates(self) -> typing.Iterator[Coordinate]:
        if self.is_straight:
            return self._covered_straight_coordinates
        return self._covered_diagonal_coordinates

    @property
    def _covered_straight_coordinates(self) -> typing.Iterator[Coordinate]:
        if self.x0 == self.x1:
            start = Coordinate(x=self.x0, y=min(self.y0, self.y1))
            distance = abs(self.y0 - self.y1)
            return (start + Coordinate(x=0, y=y) for y in range(distance + 1))

        if self.y0 == self.y0:
            start = Coordinate(x=min(self.x0, self.x1), y=self.y0)
            distance = abs(self.x0 - self.x1)
            return (start + Coordinate(x=x, y=0) for x in range(distance + 1))

        raise ValueError("Is not straight")

    @property
    def _covered_diagonal_coordinates(self) -> typing.Iterator[Coordinate]:
        if (self.y1 - self.y0) * (self.x1 - self.x0) > 0:
            return self._covered_right_down_coordinates
        return self._covered_right_up_coordinates

    @property
    def _covered_right_down_coordinates(self) -> typing.Iterator[Coordinate]:
        start = Coordinate(x=min(self.x0, self.x1), y=min(self.y0, self.y1))
        distance = abs(self.x0 - self.x1)
        return (start + Coordinate(x=d, y=d) for d in range(distance + 1))

    @property
    def _covered_right_up_coordinates(self) -> typing.Iterator[Coordinate]:
        start = (
            Coordinate(x=self.x0, y=self.y0)
            if self.x0 < self.x1
            else Coordinate(x=self.x1, y=self.y1)
        )
        distance = abs(self.x0 - self.x1)
        return (start + Coordinate(x=d, y=-d) for d in range(distance + 1))


    def __repr__(self) -> str:
        return f'{self.x0},{self.y0} -> {self.x1},{self.y1}'


class Solver(_base.BaseSolver):
    _INPUT_FILENAME = 'vents.txt'

    @staticmethod
    def _preprocess_line(line: str) -> VentLine:
        coordinates = re.match(VENT_REGEXP, line)
        assert coordinates is not None, line
        return VentLine(
            x0=int(coordinates['x0']),
            y0=int(coordinates['y0']),
            x1=int(coordinates['x1']),
            y1=int(coordinates['y1']),
        )

    def solve1(self) -> int:
        vents_counter: typing.Counter[Coordinate] = collections.Counter()
        for vent_line in self._input:
            if not vent_line.is_straight:
                continue
            for coordinate in vent_line.covered_coordinates:
                vents_counter[coordinate] += 1
        return len(vents_counter) - list(vents_counter.values()).count(1)

    def solve2(self) -> int:
        vents_counter: typing.Counter[Coordinate] = collections.Counter()
        for vent_line in self._input:
            for coordinate in vent_line.covered_coordinates:
                vents_counter[coordinate] += 1
        return len(vents_counter) - list(vents_counter.values()).count(1)
