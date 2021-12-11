import dataclasses
import itertools
import typing

from rich import print

from . import _base


FIELD_SIZE: tuple[int, int] = (10, 10)


class Coordinate(typing.NamedTuple):
    x: int
    y: int

    @property
    def adjacents(self) -> typing.Iterator['Coordinate']:
        if self.x > 0:
            yield Coordinate(x=self.x - 1, y=self.y)
        if self.x + 1 < FIELD_SIZE[0]:
            yield Coordinate(x=self.x + 1, y=self.y)
        if self.y > 0:
            yield Coordinate(x=self.x, y=self.y - 1)
        if self.y + 1 < FIELD_SIZE[1]:
            yield Coordinate(x=self.x, y=self.y + 1)
        if self.x > 0 and self.y > 0:
            yield Coordinate(x=self.x - 1, y=self.y - 1)
        if self.x > 0 and self.y + 1 < FIELD_SIZE[1]:
            yield Coordinate(x=self.x - 1, y=self.y + 1)
        if self.x + 1 < FIELD_SIZE[0] and self.y > 0:
            yield Coordinate(x=self.x + 1, y=self.y - 1)
        if self.x + 1 < FIELD_SIZE[0] and self.y + 1 < FIELD_SIZE[1]:
            yield Coordinate(x=self.x + 1, y=self.y + 1)


@dataclasses.dataclass
class Octopus:
    energy: int
    coordinate: Coordinate

    def energize(self) -> None:
        self.energy = (self.energy + 1) % 10

    @property
    def flashed(self) -> bool:
        return not self.energy

    @property
    def rich(self) -> str:
        color = 'green' if self.energy == 0 else "red"
        return f"[{color}]{self.energy}[/{color}]"


class Solver(_base.BaseSolver):
    _INPUT_FILENAME = 'octopuses.txt'

    def __init__(self) -> None:
        super().__init__()
        self.octopuses = [
            [
                Octopus(energy=energy, coordinate=Coordinate(x=x, y=y))
                for x, energy in enumerate(line)
            ]
            for y, line in enumerate(self._input)
        ]

    @staticmethod
    def _preprocess_line(line: str) -> list[int]:
        return [int(energy) for energy in line]

    @property
    def rich(self) -> str:
        return "\n".join(["".join(oc.rich for oc in line) for line in self.octopuses])

    def flashed_octopuses_after_being_energized(self) -> int:
        flashed = 0
        to_visit: set[Coordinate] = set()

        for octopus in itertools.chain(*self.octopuses):
            octopus.energize()
            if octopus.flashed:
                to_visit.add(octopus.coordinate)

        while to_visit:
            flashed += 1
            coordinate = to_visit.pop()
            for adjacent in coordinate.adjacents:
                octopus = self.octopuses[adjacent.y][adjacent.x]
                if octopus.flashed:
                    continue
                octopus.energize()
                if octopus.flashed:
                    to_visit.add(adjacent)

        return flashed

    def solve1(self) -> int:
        flashed = 0

        for step in range(100):
            print(f"After step {step + 1}:\n{self.rich}")
            flashed += self.flashed_octopuses_after_being_energized()

        return flashed

    def solve2(self) -> int:
        step = 1

        while self.flashed_octopuses_after_being_energized() != 100:
            print(f"After step {step + 1}:\n{self.rich}")
            step += 1

        return step
