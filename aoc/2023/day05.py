from __future__ import annotations

import operator
import pathlib
import typing

import iter_model
import utils


INPUT_TXT = pathlib.Path('inputs/day05.txt')


class Range(typing.NamedTuple):
    start: int
    length: int


class RangeMap(typing.NamedTuple):
    destination_start: int
    source_start: int
    length: int

    def map_single(self, value: int) -> int | None:
        shift = value - self.source_start
        if 0 <= shift < self.length:
            return self.destination_start + shift
        return None

    def map_range(self, rng: Range) -> tuple[Range | None, list[Range]]:
        start = max(self.source_start, rng.start)
        end = min(self.source_start + self.length, rng.start + rng.length)
        if start >= end:
            return None, [rng]
        intersection = Range(start, end - start)
        leftover = []
        start_shift = intersection.start - rng.start
        if start_shift > 0:
            leftover.append(Range(rng.start, start_shift))
        end_shift = rng.start + rng.length - intersection.start - intersection.length
        if end_shift > 0:
            leftover.append(Range(intersection.start + intersection.length, end_shift))
        target = Range(
            intersection.start - self.source_start + self.destination_start,
            intersection.length,
        )
        return target, leftover


class LazyMapping(typing.NamedTuple):
    range_maps: list[RangeMap]

    def map(self, value: int) -> int:
        try:
            found = (
                iter_model.SyncIter(self.range_maps)
                .map(lambda range_map: range_map.map_single(value))
                .where(lambda value: value is not None)
                .first()
            )
        except StopIteration:
            found = None
        found = found or value
        return found

    def map_range(self, rng: Range) -> list[Range]:
        unmapped = [rng]
        mapped = []
        for range_map in self.range_maps:
            still_unmapped = []
            for unmapped_range in unmapped:
                target, leftover = range_map.map_range(unmapped_range)
                if target is not None:
                    mapped.append(target)
                still_unmapped.extend(leftover)
            unmapped = still_unmapped
        return mapped + unmapped


class Almanac(typing.NamedTuple):
    seeds: list[int]
    maps: list[LazyMapping]

    def find_seed_location(self, seed: int) -> int:
        value = seed
        for map in self.maps:
            value = map.map(value)
        return value

    def find_locations(self, rng: Range) -> list[Range]:
        source_ranges = [rng]
        for map in self.maps:
            target_ranges = []
            for source_range in source_ranges:
                target_ranges.extend(map.map_range(source_range))
            source_ranges = target_ranges
        return source_ranges


def main() -> None:
    almanac = deserialize_almanac(utils.read_lines(INPUT_TXT))
    answer_1 = iter_model.SyncIter(almanac.seeds).map(almanac.find_seed_location).min()
    answer_2 = (
        iter_model.SyncIter(almanac.seeds)
        .batches(2)
        .map(lambda pair: Range(start=pair[0], length=pair[1]))
        .map(almanac.find_locations)
        .flatten()
        .map(operator.attrgetter('start'))
        .min()
    )
    print(answer_1, answer_2, sep='\n')


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
