import collections
import typing

from . import _base


class Solver(_base.BaseSolver):
    _INPUT_FILENAME = 'lanternfish.txt'

    @property
    def _initial_state(self) -> list[int]:
        return list(self._input)[0]

    @staticmethod
    def _preprocess_line(line) -> list[int]:
        return [int(timer) for timer in line.split(',')]

    def solve1(self) -> int:
        return self._predict_lanterfish_population(days=80)

    def solve2(self) -> int:
        return self._predict_lanterfish_population(days=256)

    def _predict_lanterfish_population(self, /, days: int) -> int:
        timers: typing.Counter[int] = collections.Counter(self._initial_state)

        for day in range(days):
            print(f"counting {day=}")
            newborns = 0

            for timer in sorted(timers):
                if timer == 0:
                    newborns = timers[timer]
                    continue

                timers[timer - 1] = timers[timer]
                timers[timer] = 0

            timers[8] = newborns
            timers[6] += newborns

        return sum(timers.values())
