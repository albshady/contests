from __future__ import annotations

import collections
import pathlib
import typing

import utils


INPUT_TXT = pathlib.Path('inputs/day04.txt')


class Coordinate(typing.NamedTuple):
    row: int
    column: int


class Card(typing.NamedTuple):
    id: int
    winning_numbers: set[int]
    given_numbers: list[int]

    def scratchcards_copied(self) -> typing.Iterator[int]:
        return (self.id + i for i in range(1, self.numbers_matching + 1))

    def calculate_points(self) -> int:
        total = self.numbers_matching
        return 2 ** (total - 1) if total > 0 else 0

    @property
    def numbers_matching(self) -> int:
        counter = collections.Counter(self.given_numbers)
        return sum(counter.get(num, 0) for num in self.winning_numbers)


def main() -> None:
    answer_1 = (
        utils.read_lines(INPUT_TXT)
        .map(parse_line)
        .map(Card.calculate_points)
        .sum()
        .unwrap()
    )

    occurencies: collections.Counter[int] = collections.Counter()
    for line in utils.read_lines(INPUT_TXT):
        card = parse_line(line)
        occurencies[card.id] += 1
        for copied_card_id in card.scratchcards_copied():
            occurencies[copied_card_id] += occurencies[card.id]
    answer_2 = sum(occurencies.values())
    print(answer_1, answer_2, sep='\n')


def parse_line(line: str) -> Card:
    card_id, _, all_numbers = line.partition(':')
    id = int(card_id.strip().split()[1])
    raw_winning_numbers, _, raw_given_numbers = all_numbers.partition('|')
    winning_numbers = {int(n) for n in raw_winning_numbers.strip().split()}
    given_numbers = [int(n) for n in raw_given_numbers.strip().split()]
    return Card(id=id, winning_numbers=winning_numbers, given_numbers=given_numbers)


if __name__ == "__main__":
    main()
