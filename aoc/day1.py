import collections
import typing

import config


def read_measurements() -> typing.Iterator[int]:
    with open(config.DATA_DIR / 'measurements.txt', 'r') as input_file:
        while line := input_file.readline():
            yield int(line.strip())

def task1() -> None:
    prev_measurement = None
    counter = 0

    for measurement in read_measurements():
        if prev_measurement and measurement > prev_measurement:
            counter += 1
        prev_measurement = measurement

    print(f"Nubmer of measurements larger than the previous ones: {counter}")


def task2() -> None:
    measurements: typing.Deque[int] = collections.deque(maxlen=3)
    counter = 0

    for measurement in read_measurements():
        if len(measurements) < 3:
            measurements.append(measurement)
            continue

        prev_sum = sum(measurements)
        measurements.append(measurement)

        if sum(measurements) > prev_sum:
            counter += 1

    print(f"Nubmer of sums larger than the previous ones: {counter}")


if __name__ == '__main__':
    task2()
