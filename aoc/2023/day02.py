from __future__ import annotations

import collections
import functools
import math
import operator
import pathlib
import typing

import iters
import utils


INPUT_TXT = pathlib.Path('inputs/day02.txt')

CONSTRAINTS: CubeSet = {
    'red': 12,
    'green': 13,
    'blue': 14,
}


class CubeSet(typing.TypedDict):
    red: typing.NotRequired[int]
    green: typing.NotRequired[int]
    blue: typing.NotRequired[int]


class GameInfo(typing.NamedTuple):
    game_id: int
    sets: list[CubeSet]


def parse_line(line: str) -> GameInfo:
    name, _, sets_string = line.partition(':')
    game_id = int(name.split()[1])
    raw_sets = sets_string.split(';')
    cube_sets = []
    for raw_set in raw_sets:
        cubeset_data = {}
        for count_and_color in raw_set.strip().split(','):
            count, _, color = count_and_color.strip().partition(' ')
            cubeset_data[color] = int(count)
        cube_sets.append(CubeSet(**cubeset_data))
    return GameInfo(game_id=game_id, sets=cube_sets)


def check_constraints(game_info: GameInfo, constraints: CubeSet) -> bool:
    return not (
        iters.Iter(game_info.sets)
        .map(lambda cube_set: cube_set.items())
        .flatten()
        .filter(lambda color_count: color_count[1] > constraints[color_count[0]])
        .any()
    )


def calculate_power(game_info: GameInfo) -> int:
    required_cubes = (
        iters.Iter(game_info.sets)
        .map(collections.Counter)
        .reduce(operator.or_)
        .unwrap()
    )
    return math.prod(required_cubes.values())


def main() -> None:
    answer_1 = (
        utils.read_lines(INPUT_TXT)
        .map(parse_line)
        .filter(functools.partial(check_constraints, constraints=CONSTRAINTS))
        .map(operator.attrgetter('game_id'))
        .sum()
    )
    answer_2 = utils.read_lines(INPUT_TXT).map(parse_line).map(calculate_power).sum()
    print(answer_1, answer_2, sep='\n')


if __name__ == "__main__":
    main()
