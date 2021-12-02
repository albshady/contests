import argparse
import typing

import config


class Command(typing.NamedTuple):
    direction: str
    distance: int


def read_commands() -> typing.Iterator[Command]:
    with open(config.DATA_DIR / 'commands.txt', 'r') as input_file:
        for line in input_file:
            direction, distance = line.split()
            yield Command(direction=direction, distance=int(distance))


def task1() -> None:
    """In the first task we are moving straighforward"""

    horizontal = 0
    depth = 0

    for command in read_commands():
        match command.direction:
            case 'forward':
                horizontal += command.distance
            case 'up':
                depth -= command.distance
            case 'down':
                depth += command.distance
            case other:
                raise ValueError(f"Unknown direction: {other}")

    print(f"{horizontal * depth = } (not considering aim)")


def task2() -> None:
    """In the second task we are considering aim when moving"""

    horizontal = 0
    depth = 0
    aim = 0

    for command in read_commands():
        match command.direction:
            case 'forward':
                horizontal += command.distance
                depth += aim * command.distance
            case 'up':
                aim -= command.distance
            case 'down':
                aim += command.distance
            case other:
                raise ValueError(f"Unknown direction: {other}")

    print(f"{horizontal * depth = } (when considering aim)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('task', help='Task number, 1 or 2', choices=('1', '2'))
    args = parser.parse_args()

    match int(args.task):
        case 1:
            task1()
        case 2:
            task2()
        case _:
            raise RuntimeError


if __name__ == '__main__':
    main()
