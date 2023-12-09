from __future__ import annotations

import pathlib
import typing

import iters
import utils


INPUT_TXT = pathlib.Path('inputs/day06.txt')


def main() -> None:
    records = parse_records(utils.read_lines(INPUT_TXT))
    answer_1 = records.map(number_of_ways_to_beat).product().unwrap()
    record = parse_record(utils.read_lines(INPUT_TXT))
    answer_2 = number_of_ways_to_beat(record)
    print(answer_1, answer_2, sep='\n')


class Record(typing.NamedTuple):
    time: int
    distance: int


def parse_records(lines: typing.Iterable[str]) -> iters.Iter[Record]:
    def _parse_values(line: str) -> iters.Iter[int]:
        return iters.Iter(line.split()).skip(1).map(int)

    times, distances = lines
    times = _parse_values(times)
    distances = _parse_values(distances)
    return times.zip(distances).map(lambda td: Record(time=td[0], distance=td[1]))


def parse_record(lines: typing.Iterable[str]) -> Record:
    def _parse_value(line: str) -> int:
        *_, parts = line.partition(':')
        values = parts.strip().split()
        return int(''.join(values))

    raw_time, raw_distance = lines
    return Record(time=_parse_value(raw_time), distance=_parse_value(raw_distance))


def number_of_ways_to_beat(record: Record) -> int:
    first_winning = (
        iters.Iter(range(record.time))
        .map(lambda x: x * (record.time - x))
        .enumerate()
        .filter(lambda p: p[1] > record.distance)
        .first()
    )
    if first_winning.is_null():
        return 0
    first_winning = first_winning.unwrap()[0]
    last_winning = record.time - first_winning
    return last_winning - first_winning + 1


if __name__ == "__main__":
    main()
