from __future__ import annotations

import functools
import operator
import pathlib
import typing

import iters
import utils


INPUT_TXT = pathlib.Path('inputs/day11.txt')


class Coordinate(typing.NamedTuple):
    x: int
    y: int


def main() -> None:
    original_universe = utils.read_lines(INPUT_TXT).map(str.strip).list()
    empty_rows = []
    empty_cols = []
    universe = (
        iters.Iter(original_universe)
        .enumerate()
        .inspect(functools.partial(append_index_if_empty_row, collection=empty_rows))
        .map(operator.itemgetter(1))
        .transpose()
        .enumerate()
        .inspect(functools.partial(append_index_if_empty_row, collection=empty_cols))
        .map(operator.itemgetter(1))
        .transpose()
        .list()
    )
    calculate_distance_curried = functools.partial(
        calculate_distance,
        empty_rows=empty_rows,
        empty_cols=empty_cols,
    )
    answer_1 = (
        iters.Iter(universe)
        .enumerate()
        .flat_map(locate_galaxies_in_row)
        .combinations(2)
        .map(functools.partial(calculate_distance_curried, empty_multiplier=2))
        .sum()
        .unwrap_or(0)
    )
    answer_2 = (
        iters.Iter(universe)
        .enumerate()
        .flat_map(locate_galaxies_in_row)
        .combinations(2)
        .map(functools.partial(calculate_distance_curried, empty_multiplier=1_000_000))
        .sum()
        .unwrap_or(0)
    )
    print(answer_1, answer_2, sep='\n')


def append_index_if_empty_row(
    indexed_row: tuple[int, typing.Sequence[str]], collection: list[int]
) -> None:
    index, row = indexed_row
    if '#' not in row:
        collection.append(index)


def calculate_distance(
    galaxies: tuple[Coordinate, Coordinate],
    empty_multiplier: int,
    empty_rows: typing.Sequence[int],
    empty_cols: typing.Sequence[int],
) -> int:
    start, finish = galaxies
    rows = range(min(start.x, finish.x), max(start.x, finish.x))
    cols = range(min(start.y, finish.y), max(start.y, finish.y))
    empty_in_rows = sum(empty_multiplier - 1 for row in empty_rows if row in rows)
    empty_in_cols = sum(empty_multiplier - 1 for col in empty_cols if col in cols)
    return len(rows) + len(cols) + empty_in_rows + empty_in_cols


def locate_galaxies_in_row(
    index_and_row: tuple[int, typing.Sequence[str]]
) -> typing.Iterator[Coordinate]:
    x, row = index_and_row
    y = -1
    while True:
        try:
            y = row.index('#', y + 1)
        except ValueError:
            return
        yield Coordinate(x, y)


if __name__ == "__main__":
    main()
