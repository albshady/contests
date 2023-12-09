from __future__ import annotations

import collections
import dataclasses
import enum
import functools
import pathlib

import iters
import utils


INPUT_TXT = pathlib.Path('inputs/day07.txt')

JOKER_VALUE = 1
CARD_TO_VALUE_1 = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
CARD_TO_VALUE_2 = CARD_TO_VALUE_1 | {'J': JOKER_VALUE}


def main() -> None:
    answer_1 = (
        iters.Iter(utils.read_lines(INPUT_TXT))
        .map(functools.partial(parse_hand, card_to_value=CARD_TO_VALUE_1))
        .sort()
        .enumerate_from(1)
        .map(lambda rank_hand: rank_hand[0] * rank_hand[1].bid)
        .sum()
        .unwrap()
    )
    answer_2 = (
        iters.Iter(utils.read_lines(INPUT_TXT))
        .map(functools.partial(parse_hand, card_to_value=CARD_TO_VALUE_2))
        .sort()
        .enumerate_from(1)
        .map(lambda rank_hand: rank_hand[0] * rank_hand[1].bid)
        .sum()
        .unwrap()
    )
    print(answer_1, answer_2, sep='\n')


class Combo(enum.IntEnum):
    HIGH_CARD = enum.auto()
    ONE_PAIR = enum.auto()
    TWO_PAIR = enum.auto()
    THREE_OF_A_KIND = enum.auto()
    FULL_HOUSE = enum.auto()
    FOUR_OF_A_KIND = enum.auto()
    FIVE_OF_A_KIND = enum.auto()


@functools.total_ordering
@dataclasses.dataclass(frozen=True, eq=False)
class Hand:
    cards: list[int]
    bid: int

    @functools.cached_property
    def combo(self) -> Combo:
        counter = collections.Counter(self.cards)
        jokers = counter.pop(JOKER_VALUE, 0)
        most_duplicates = (
            most_common[0][1] + jokers
            if (most_common := counter.most_common(1))
            else jokers
        )
        match len(counter) or 1, most_duplicates:
            case 5, 1:
                return Combo.HIGH_CARD
            case 4, 2:
                return Combo.ONE_PAIR
            case 3, 2:
                return Combo.TWO_PAIR
            case 3, 3:
                return Combo.THREE_OF_A_KIND
            case 2, 3:
                return Combo.FULL_HOUSE
            case 2, 4:
                return Combo.FOUR_OF_A_KIND
            case 1, 5:
                return Combo.FIVE_OF_A_KIND
            case _:
                raise ValueError(f"Impossible to find a combo for {self}")

    def __lt__(self, other: Hand) -> bool:
        if self.combo == other.combo:
            return self.cards < other.cards
        return self.combo < other.combo

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Hand):
            return self.cards == other.cards
        return NotImplemented


def parse_hand(line: str, card_to_value: dict[str, int]) -> Hand:
    labels, bid = line.split()
    values = [card_to_value.get(label) or int(label) for label in labels]
    return Hand(cards=values, bid=int(bid))


if __name__ == "__main__":
    main()
