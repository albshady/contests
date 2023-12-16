from __future__ import annotations

import dataclasses
import itertools
import pathlib
import typing

import iters
import utils
import wraps


INPUT_TXT = pathlib.Path('inputs/day10.txt')


@dataclasses.dataclass
class Coordinate:
    x: int
    y: int

    def __add__(self, other: Coordinate) -> Coordinate:
        return Coordinate(self.x + other.x, self.y + other.y)


LEFT = Coordinate(0, -1)
RIGHT = Coordinate(0, 1)
TOP = Coordinate(-1, 0)
BOTTOM = Coordinate(1, 0)
SYMBOL_TO_DIRECTIONS = {
    '-': (LEFT, RIGHT),
    '|': (TOP, BOTTOM),
    'L': (TOP, RIGHT),
    'F': (RIGHT, BOTTOM),
    '7': (LEFT, BOTTOM),
    'J': (LEFT, TOP),
}


@dataclasses.dataclass
class Sketch:
    field: list[str]

    def find(self, coordinate: Coordinate) -> wraps.Option[str]:
        if coordinate.x < 0 or coordinate.x > len(self.field):
            return wraps.Null()
        row = self.field[coordinate.x]
        if coordinate.y < 0 or coordinate.y > len(row):
            return wraps.Null()
        return wraps.Some(row[coordinate.y])

    def __str__(self) -> str:
        return '\n'.join(self.field)


def main() -> None:
    sketch = Sketch(field=utils.read_lines(INPUT_TXT).map(str.strip).list())
    pipes = find_pipes(sketch)
    answer_1 = len(pipes) // 2
    print(answer_1, None, sep='\n')


def find_pipes(sketch: Sketch) -> list[Coordinate]:
    start = next(
        Coordinate(i, line.find('S'))
        for i, line in enumerate(sketch.field)
        if 'S' in line
    )
    for pipe in SYMBOL_TO_DIRECTIONS:
        potential_sketch = Sketch(
            field=[line.replace('S', pipe) for line in sketch.field]
        )
        pipes = traverse(sketch=potential_sketch, start=start)
        if pipes:
            return pipes
    raise ValueError("Not found")


def traverse(sketch: Sketch, start: Coordinate) -> list[Coordinate]:
    pipe_symbol = sketch.find(start).early()
    _, target = SYMBOL_TO_DIRECTIONS[pipe_symbol]
    pipes = [start]
    while True:
        position = pipes[-1] + target
        pipe_symbol = sketch.find(position).early()
        if pipe_symbol not in SYMBOL_TO_DIRECTIONS:
            return []
        source, target = SYMBOL_TO_DIRECTIONS[pipe_symbol]
        if position + target == pipes[-1]:
            source, target = target, source
        elif position + source != pipes[-1]:
            return []
        if position == start:
            return pipes
        pipes.append(position)


if __name__ == "__main__":
    main()
