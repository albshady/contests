from __future__ import annotations

import collections
import functools
import math
import operator
import pathlib
import typing

import iter_model
import utils


INPUT_TXT = pathlib.Path('inputs/day03.txt')


class Coordinate(typing.NamedTuple):
    row: int
    column: int


class Number(typing.NamedTuple):
    value: int
    row: int
    start: int
    end: int

    @property
    @iter_model.sync_iter
    def adjacent_coordinates(self) -> typing.Iterable[Coordinate]:
        for row in range(self.row - 1, self.row + 2):
            for column in range(self.start - 1, self.end + 2):
                yield Coordinate(row, column)


def main() -> None:
    schematic = utils.read_lines(INPUT_TXT).to_list()
    symbols = locate_symbols(schematic, predicate=is_symbol)
    answer_1 = (
        locate_numbers(schematic)
        .where(functools.partial(is_adjacent_to_symbol, symbols=symbols))
        .map(operator.attrgetter('value'))
        .reduce(operator.add, initial=0)
    )

    asterisks = locate_symbols(schematic, predicate=lambda s: s == '*')
    asterisks_to_numbers = (
        locate_numbers(schematic)
        .map(
            lambda number: {
                coordinate: [number.value]
                for coordinate in number.adjacent_coordinates
                if asterisks[coordinate]
            }
        )
        .reduce(
            lambda d1, d2: {
                key: d1.get(key, []) + d2.get(key, []) for key in d1.keys() | d2.keys()
            },
            initial={},
        )
    )
    answer_2 = (
        iter_model.SyncIter(asterisks_to_numbers.values())
        .where(lambda v: len(v) == 2)
        .map(math.prod)
        .reduce(operator.add, initial=0)
    )
    print(answer_1, answer_2, sep='\n')


@iter_model.sync_iter
def locate_numbers(schematic: list[str]) -> typing.Iterator[Number]:
    for row_ix, row in enumerate(schematic):
        start: int | None = None
        for position, char in enumerate(row):
            if char.isdigit():
                if start is None:
                    start = position
            else:
                if start is not None:
                    yield Number(
                        value=int(row[start:position]),
                        row=row_ix,
                        start=start,
                        end=position - 1,
                    )
                start = None

        if start is not None:
            yield Number(
                value=int(row[start:]),
                row=row_ix,
                start=start,
                end=len(row) - 1,
            )


def locate_symbols(
    schematic: list[str], predicate: typing.Callable[[str], bool]
) -> collections.defaultdict[Coordinate, bool]:
    mapping = collections.defaultdict(bool)
    for row_ix, row in enumerate(schematic):
        for column_ix, char in enumerate(row):
            if not char.isspace() and predicate(char):
                mapping[Coordinate(row_ix, column_ix)] = True
    return mapping


def is_symbol(char: str) -> bool:
    return char != '.' and not char.isdigit()


def is_adjacent_to_symbol(
    number: Number, symbols: collections.defaultdict[Coordinate, bool]
) -> bool:
    return number.adjacent_coordinates.where(lambda c: symbols[c]).any()


if __name__ == "__main__":
    main()
