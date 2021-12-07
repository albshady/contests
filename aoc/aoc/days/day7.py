from . import _base


class Solver(_base.BaseSolver):
    _INPUT_FILENAME = 'crabs.txt'

    @staticmethod
    def _preprocess_line(line: str) -> list[int]:
        return [int(pos) for pos in line.split(',')]

    @property
    def _initial_positions(self) -> list[int]:
        return list(self._input)[0]

    def solve1(self) -> int:
        positions = self._initial_positions
        costs = {}
        for aim in range(min(positions), max(positions)):
            costs[aim] = sum(abs(pos - aim) for pos in positions)
        return min(costs.values())

    def solve2(self) -> int:
        positions = self._initial_positions
        costs = {}
        for aim in range(min(positions), max(positions)):
            costs[aim] = sum(
                (dist := abs(pos - aim)) * (dist + 1) // 2 for pos in positions
            )
        return min(costs.values())
