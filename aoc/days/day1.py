import argparse
import collections
import typing

import config


def read_measurements() -> typing.Iterator[int]:
    with open(config.DATA_DIR / 'measurements.txt', 'r') as input_file:
        while line := input_file.readline():
            yield int(line.strip())

def count_measurement_increases(to_consider: int) -> int:
    measurements: typing.Deque[int] = collections.deque(maxlen=to_consider)
    count = 0

    for measurement in read_measurements():
        if len(measurements) < to_consider:
            measurements.append(measurement)
            continue

        prev_sum = sum(measurements)
        measurements.append(measurement)

        if sum(measurements) > prev_sum:
            count += 1

    return count

def task1() -> None:
    """In the first task we are comparing only one last measurement"""
    count = count_measurement_increases(to_consider=1)

    print(f"{count} measurements are larger than the previous ones")


def task2() -> None:
    """In the second task we are comparing groups of three last measurements"""
    count = count_measurement_increases(to_consider=3)

    print(f"{count} measurement groups are larger than the previous ones")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('task', help='Task number, 1 or 2', choices=('1', '2'))
    args = parser.parse_args()

    if int(args.task) == 1:
        task1()
    else:
        task2()
