import operator
import pathlib
import typing

import iter_model


INPUT_TXT = pathlib.Path('inputs/day01.txt')


SPELLED_DIGITS = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}


def read_lines(filepath: pathlib.Path) -> typing.Iterable[str]:
    return filter(None, filepath.read_text().split('\n'))


@iter_model.sync_iter
def find_digits(line: str) -> typing.Iterator[int]:
    # TODO: max() has issues with typing
    longest_spelled = iter_model.SyncIter(SPELLED_DIGITS).map(len).max()
    for start, start_letter in enumerate(line):
        if start_letter.isdigit():
            yield int(start_letter)
        for end in range(start, min(start + longest_spelled, len(line))):
            if line[start : end + 1] in SPELLED_DIGITS:
                yield SPELLED_DIGITS[line[start : end + 1]]


def find_first_digit(line: str) -> int:
    return find_digits(line).first()


def find_last_digit(line: str) -> int:
    return find_digits(line).last()


def main() -> None:
    answer = (
        iter_model.SyncIter(read_lines(INPUT_TXT))
        .map(lambda line: find_digits(line).to_list())
        .map(lambda numbers: numbers[0] * 10 + numbers[-1])
        .reduce(operator.add, initial=0)  # TODO: sum() would be useful
    )
    print(answer)


if __name__ == "__main__":
    main()
