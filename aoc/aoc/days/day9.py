import bisect
import math
import typing

from ._base import BaseSolver


class Point(typing.NamedTuple):
    row: int
    col: int
    height: int

    @property
    def risk(self) -> int:
        return self.height + 1


class Solver(BaseSolver):
    _INPUT_FILENAME = 'heights.txt'

    def __init__(self) -> None:
        super().__init__()
        self._map: list[list[Point]] = [
            [
                Point(row=row, col=col, height=height)
                for col, height in enumerate(heights)
            ]
            for row, heights in enumerate(self._input)
        ]

    @staticmethod
    def _preprocess_line(line: str) -> list[int]:
        return [int(n) for n in line]

    def find_low_points(self) -> list[Point]:
        low_points = []
        for row in self._map:
            for point in row:
                if all(
                    point.height < neighbor.height
                    for neighbor in self.get_neighbors(point=point)
                ):
                    low_points.append(point)

        return low_points

    def get_neighbors(self, point: Point) -> typing.Iterator[Point]:
        if point.row > 0:
            yield self._map[point.row - 1][point.col]
        if point.row < len(self._map) - 1:
            yield self._map[point.row + 1][point.col]
        if point.col > 0:
            yield self._map[point.row][point.col - 1]
        if point.col < len(self._map[0]) - 1:
            yield self._map[point.row][point.col + 1]

    def solve1(self) -> int:
        return sum(point.risk for point in self.find_low_points())

    def solve2(self) -> int:
        basin_lengths: list[int] = []
        low_points = self.find_low_points()

        for low_point in low_points:
            basin = self.find_basin(point=low_point)
            bisect.insort(basin_lengths, len(basin))

        assert len(basin_lengths) == len(low_points), "Insufficient amount of basins"
        return math.prod(basin_lengths[-3:])

    def find_basin(self, point: Point) -> set[Point]:
        basin = {point}
        to_visit = {point}
        while to_visit:
            point = to_visit.pop()
            for neighbor in self.get_greater_neighbors(point):
                basin.add(neighbor)
                to_visit.add(neighbor)
        return basin

    def get_greater_neighbors(self, point: Point) -> typing.Iterator[Point]:
        return filter(lambda n: 9 > n.height > point.height, self.get_neighbors(point))
