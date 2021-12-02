import collections
import typing

from . import _base


class Solver(_base.BaseSolver):
    _INPUT_FILENAME = 'measurements.txt'

    @staticmethod
    def _preprocess_line(line: str) -> int:
        return int(line)

    def _count_measurement_increases(self, to_consider: int) -> int:
        measurements: typing.Deque[int] = collections.deque(maxlen=to_consider)
        count = 0

        for measurement in self._input:
            if len(measurements) < to_consider:
                measurements.append(measurement)
                continue

            prev_sum = sum(measurements)
            measurements.append(measurement)

            if sum(measurements) > prev_sum:
                count += 1

        return count

    def solve1(self) -> int:
        """In the first task we are comparing only one last measurement"""
        return self._count_measurement_increases(to_consider=1)


    def solve2(self) -> int:
        """In the second task we are comparing groups of three last measurements"""
        return self._count_measurement_increases(to_consider=3)
