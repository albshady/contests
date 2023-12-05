from __future__ import annotations

import functools
import operator
import pathlib
import typing

import iter_model
import utils


INPUT_TXT = pathlib.Path('inputs/day05.txt')


class Range(typing.NamedTuple):
    start: int
    length: int

    @property
    def end(self) -> int:
        return self.start + self.length - 1

    def __lt__(self, other: Range) -> bool:
        return self.start < other.start

    def __sub__(self, other: Range) -> typing.Iterable[Range]:
        if not self & other:
            yield self
            return
        if self.start < other.start:
            yield Range(
                start=self.start, length=min(other.start - self.start, self.length)
            )
        if other.end < self.end:
            yield Range(
                start=other.end + 1,
                length=self.end - other.end,
            )

    def __and__(self, other: Range) -> bool:
        return (
            self.start <= other.start <= self.end
            or other.start <= self.start <= other.end
        )

    def intersect(self, other: Range) -> Range | None:
        if not self & other:
            return None
        start = max(other.start, self.start)
        end = min(self.end, other.end)
        return Range(start=self.start, length=end - start + 1)


class RangeMap(typing.NamedTuple):
    destination_start: int
    source_start: int
    length: int

    def __contains__(self, value: int) -> bool:
        return self.source_start <= value < self.source_start + self.length

    def find(self, value: int) -> int | None:
        if value not in self:
            return None
        shift = value - self.source_start
        return self.destination_start + shift

    def overlap(self, other: Range) -> tuple[Range | None, list[Range]]:
        intersection = self.source_range.intersect(other)
        if intersection is None:
            return None, [other]
        leftover = list(other - intersection)
        start_shift = intersection.start - self.source_start
        overlap = Range(
            start=self.destination_start + start_shift, length=intersection.length
        )
        return overlap, leftover

    @property
    def source_range(self) -> Range:
        return Range(start=self.source_start, length=self.length)


class LazyMapping(typing.NamedTuple):
    range_maps: list[RangeMap]

    def map(self, value: int) -> int:
        try:
            found = (
                iter_model.SyncIter(self.range_maps)
                .map(lambda instruction: instruction.find(value))
                .where(lambda value: value is not None)
                .first()
            )
        except StopIteration:
            found = None
        found = found or value
        return found

    # @iter_model.sync_iter
    def map_range(self, rng: Range) -> typing.Iterable[Range]:
        unmapped = [rng]
        mapped = []
        for instruction in self.range_maps:
            unmapped_still = []
            for subrange in unmapped:
                overlap, leftover = instruction.overlap(subrange)
                if overlap is not None:
                    mapped.append(overlap)
                unmapped_still.extend(leftover)
            unmapped = unmapped_still
        return mapped + unmapped


class Almanac(typing.NamedTuple):
    seeds: list[int]
    maps: list[LazyMapping]

    def find_seed_location(self, seed: int) -> int:
        return iter_model.SyncIter(self.maps).reduce(
            lambda value, func: func.map(value), initial=seed
        )

    # @iter_model.sync_iter
    def extrapolate_range(self, initial_range: Range) -> typing.Iterable[Range]:
        ranges = [initial_range]
        for mapping in self.maps:
            next_layer = []
            for rng in ranges:
                next_layer.extend(mapping.map_range(rng))
            ranges = next_layer
        return ranges


def main() -> None:
    almanac = deserialize_almanac(utils.read_lines(INPUT_TXT))
    # print(almanac)
    answer_1 = iter_model.SyncIter(almanac.seeds).map(almanac.find_seed_location).min()
    answer_2 = (
        iter_model.SyncIter(almanac.seeds)
        .batches(2)
        .map(lambda pair: Range(start=pair[0], length=pair[1]))
        .map(almanac.extrapolate_range)
        .map(list)
        .flatten()
        .map(operator.attrgetter('start'))
        .min()
    )
    answer_2_alt = (
        iter_model.SyncIter(almanac.seeds)
        .batches(2)
        .map(lambda pair: range(pair[0], pair[0] + pair[1]))
        .flatten()
        .map(almanac.find_seed_location)
        .min()
    )
    print(answer_1, answer_2, answer_2_alt, sep='\n')


def print_with_context(context):
    return functools.partial(print_identity, context=context)


def print_identity(x, context=None):
    if context is None:
        print(x)
    else:
        print(context, x)
    return x


def deserialize_almanac(lines: typing.Iterable[str]) -> Almanac:
    maps: list[LazyMapping] = []
    current_range_maps = []
    seeds: list[int] = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        elif ':' not in line:
            destination_start, source_start, length = list(map(int, line.split()))
            current_range_maps.append(
                RangeMap(
                    destination_start=destination_start,
                    source_start=source_start,
                    length=length,
                )
            )
        elif line.startswith('seeds:'):
            *_, values = line.partition(':')
            seeds = list(map(int, values.strip().split()))
        elif not current_range_maps:
            continue
        else:
            maps.append(LazyMapping(current_range_maps))
            current_range_maps = []

    if current_range_maps:
        maps.append(LazyMapping(current_range_maps))

    return Almanac(seeds=seeds, maps=maps)


if __name__ == "__main__":
    main()
