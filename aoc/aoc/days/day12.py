import collections
import typing

from ._base import BaseSolver


class Cave(typing.NamedTuple):
    connected: set[str]
    name: str

    @property
    def is_small(self) -> bool:
        return self.name.islower()

    @property
    def is_end(self) -> bool:
        return self.name == 'end'

    @property
    def is_start(self) -> bool:
        return self.name == 'start'


class Solver(BaseSolver):
    _INPUT_FILENAME = 'caves.txt'

    def __init__(self) -> None:
        super().__init__()
        caves: typing.DefaultDict[str, set[str]] = collections.defaultdict(set)
        for left, right in self._input:
            caves[left].add(right)
            caves[right].add(left)
        self.caves = {
            name: Cave(name=name, connected=connected)
            for name, connected in caves.items()
        }

    @staticmethod
    def _preprocess_line(line: str) -> tuple[str, str]:
        left, _, right = line.partition('-')
        return left, right

    def find_exit_paths(
        self,
        cave: Cave,
        visited: set[str],
        visited_twice: bool,
    ) -> int:
        if cave.is_end:
            return 1
        if cave.name in visited:
            if visited_twice or cave.is_start:
                return 0
            visited_twice = True
        if cave.is_small:
            visited.add(cave.name)
        return sum(
            self.find_exit_paths(
                cave=self.caves[name], visited=set(visited), visited_twice=visited_twice
            )
            for name in cave.connected
        )

    def solve1(self) -> int:
        start = self.caves['start']
        return self.find_exit_paths(cave=start, visited=set(), visited_twice=True)

    def solve2(self) -> int:
        start = self.caves['start']
        return self.find_exit_paths(cave=start, visited=set(), visited_twice=False)
