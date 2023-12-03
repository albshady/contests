import functools
import pathlib
import typing

import utils


INPUT_TXT = pathlib.Path('inputs/day02.txt')

CONSTRAINTS = {
    'red': 12,
    'green': 13,
    'blue': 14,
}


class CubeSet(typing.NamedTuple):
    red: int = 0
    green: int = 0
    blue: int = 0


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


def check_constraints(game_info: GameInfo, constraints: dict[str, int]) -> bool:
    for color, max_amount in constraints.items():
        for cube_set in game_info.sets:
            if getattr(cube_set, color) > max_amount:
                return False
    return True


def main() -> None:
    answer = (
        utils.read_lines(INPUT_TXT)
        .map(parse_line)
        .where(functools.partial(check_constraints, constraints=CONSTRAINTS))
        # TODO: reduce() has typing issues
        .reduce(lambda valid_sum, game_info: valid_sum + game_info.game_id, initial=0)
    )
    print(answer)


if __name__ == "__main__":
    main()
