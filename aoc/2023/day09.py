from __future__ import annotations

import pathlib

import iters
import utils


INPUT_TXT = pathlib.Path('inputs/day09.txt')


def main() -> None:
    answer_1 = (
        utils.read_lines(INPUT_TXT)
        .map(lambda line: iters.Iter(line.split()).map(int).list())
        .map(extrapolate)
        .sum()
        .unwrap()
    )
    answer_2 = (
        utils.read_lines(INPUT_TXT)
        .map(lambda line: iters.Iter(line.split()).map(int).reverse().list())
        .map(extrapolate)
        .sum()
        .unwrap()
    )
    print(answer_1, answer_2, sep='\n')


def extrapolate(progression: list[int]) -> int:
    if all(n == 0 for n in progression):
        return 0
    return progression[-1] + extrapolate(
        iters.Iter(progression)
        .pairs_windows()
        .map(lambda pair: pair[1] - pair[0])
        .list()
    )


if __name__ == "__main__":
    main()
