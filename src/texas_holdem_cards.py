"""
https://www.codewars.com/kata/524c74f855025e2495000262/python

Texas Hold'em Hands

Texas Hold'em is a Poker variant in which each player is given two "hole cards".
Players then proceed to make a series of bets while five "community cards" are dealt.
If there are more than one player remaining when the betting stops,
a showdown takes place in which players reveal their cards.
Each player makes the best poker hand possible using five of the seven available cards
(community cards + the player's hole cards).

Possible hands are, in descending order of value:

- Straight-flush (five consecutive ranks of the same suit). Higher rank is better.
- Four-of-a-kind (four cards with the same rank).
  Tiebreaker is first the rank, then the rank of the remaining card.
- Full house (three cards with the same rank, two with another).
  Tiebreaker is first the rank of the three cards, then rank of the pair.
- Flush (five cards of the same suit).
  Higher ranks are better, compared from high to low rank.
- Straight (five consecutive ranks). Higher rank is better.
- Three-of-a-kind (three cards of the same rank).
  Tiebreaker is first the rank of the three cards, then the highest other rank,
  then the second highest other rank.
- Two pair (two cards of the same rank, two cards of another rank).
  Tiebreaker is first the rank of the high pair, then the rank of the low pair
  and then the rank of the remaining card.
- Pair (two cards of the same rank).
  Tiebreaker is first the rank of the two cards, then the three other ranks.
- Nothing. Tiebreaker is the rank of the cards from high to low.

Given hole cards and community cards, complete the function hand
to return the type of hand (as written above, you can ignore case)
and a list of ranks in decreasing order of significance,
to use for comparison against other hands of the same type, of the best possible hand.

hand(["A♠", "A♦"], ["J♣", "5♥", "10♥", "2♥", "3♦"])
# ...should return ("pair", ranks: ["A", "J", "10", "5"]})
hand(["A♠", "K♦"], ["J♥", "5♥", "10♥", "Q♥", "3♥"])
# ...should return ("flush", ["Q", "J", "10", "5", "3"])

EDIT: for Straights with an Ace, only the ace-high straight is accepted.
An ace-low straight is invalid (ie. A,2,3,4,5 is invalid).
This is consistent with the author's reference solution. ~docgunthrop
"""


import collections
import dataclasses
import enum
import typing


class CombinationName(str, enum.Enum):
    NOTHING = 'nothing'
    PAIR = 'pair'
    TWO_PAIR = 'two pair'
    THREE_OF_A_KIND = 'three-of-a-kind'
    STRAIGHT = 'straight'
    FLUSH = 'flush'
    FULL_HOUSE = 'full house'
    FOUR_OF_A_KIND = 'four-of-a-kind'
    STRAIGHT_FLUSH = 'straight-flush'


@dataclasses.dataclass
class Card:
    _HIGHER_CARDS_VALUES = {
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14,
    }

    rank: str
    suit: str
    value: int

    @classmethod
    def from_str(cls, card_representation: str) -> 'Card':
        rank = card_representation[:-1]
        suit = card_representation[-1]
        value = cls.get_value(rank=rank)
        return cls(rank=rank, suit=suit, value=value)

    @classmethod
    def get_value(cls, rank: str) -> int:
        return cls._HIGHER_CARDS_VALUES.get(rank) or int(rank)

    def __lt__(self, other: object) -> bool:
        assert isinstance(other, Card)

        return self.value < other.value

    def __eq__(self, other: object) -> bool:
        assert isinstance(other, Card)

        return repr(self) == repr(other)

    def __repr__(self) -> str:
        return f'{self.rank}{self.suit}'

    def __hash__(self) -> int:
        return hash(repr(self))


@dataclasses.dataclass
class Combination:
    cards: typing.Set[Card]
    name: CombinationName = CombinationName.NOTHING

    @property
    def is_sufficient(self) -> bool:
        return len(self.cards) >= 5

    def add_greatest_cards(self, ordered_cards: typing.List[Card]) -> None:
        for greatest_card in ordered_cards:
            self.cards.add(greatest_card)
            if self.is_sufficient:
                return

    @property
    def ranks(self) -> typing.List[str]:
        return self._ranks_ordered_by_occurencies

    @property
    def _ranks_ordered_by_occurencies(self) -> typing.List[str]:
        occurencies: typing.Counter[str] = collections.Counter()
        for card in self.cards:
            occurencies[card.rank] += 1
        return sorted(
            list(occurencies.keys()),
            key=lambda rank: (occurencies[rank], Card.get_value(rank)),
            reverse=True,
        )


class Hand:
    def __init__(self, cards: typing.List[Card]) -> None:
        self._cards = sorted(cards, reverse=True)

    @property
    def best_hand(self) -> Combination:
        combination = self._find_winning_cards()
        if not combination.is_sufficient:
            combination.add_greatest_cards(ordered_cards=self._cards)
        return combination

    def _find_winning_cards(self) -> Combination:
        straight = self._find_straight()
        flush = self._find_flush()

        if len(straight_flush := straight & flush) == 5:
            return Combination(
                name=CombinationName.STRAIGHT_FLUSH, cards=straight_flush
            )
        if flush:
            return Combination(name=CombinationName.FLUSH, cards=flush)
        if straight:
            return Combination(name=CombinationName.STRAIGHT, cards=straight)
        return self._find_most_of_a_kind()

    def _find_straight(self) -> typing.Set[Card]:
        progression = [self._cards[0]]

        for card in self._cards[1:]:
            if card.value == progression[-1].value:
                continue  # skip same rank
            if card.value + 1 != progression[-1].value:
                progression = [card]
                continue  # progression stopped
            progression.append(card)
            if len(progression) == 5:
                return set(progression)
        return set()

    def _find_flush(self) -> typing.Set[Card]:
        suits = collections.defaultdict(set)
        for card in self._cards:
            suits[card.suit].add(card)
        for cards in suits.values():
            if len(cards) >= 5:
                return cards
        return set()

    def _find_most_of_a_kind(self) -> Combination:
        combination = Combination(cards=set())
        for cards_with_same_kind in self._greatest_cards_with_same_kind:
            combination.cards |= cards_with_same_kind
            if len(cards_with_same_kind) == 4:
                combination.name = CombinationName.FOUR_OF_A_KIND
                break
            if len(cards_with_same_kind) == 3:
                if combination.name == CombinationName.THREE_OF_A_KIND:
                    combination.name = CombinationName.FULL_HOUSE
                    break
                combination.name = CombinationName.THREE_OF_A_KIND
                continue
            if len(cards_with_same_kind) == 2:
                if combination.name == CombinationName.THREE_OF_A_KIND:
                    combination.name = CombinationName.FULL_HOUSE
                    break
                if combination.name == CombinationName.PAIR:
                    combination.name = CombinationName.TWO_PAIR
                    break
                combination.name = CombinationName.PAIR
        return combination

    @property
    def _greatest_cards_with_same_kind(self) -> typing.Iterator[typing.Set[Card]]:
        ranks = collections.defaultdict(set)
        for card in self._cards:
            ranks[card.value].add(card)
        for rank in sorted(ranks, key=lambda r: (len(ranks[r]), r), reverse=True):
            if len(ranks[rank]) < 2:
                return
            yield ranks[rank]


HAND_T = typing.Tuple[CombinationName, typing.List[str]]


def hand(hole_cards: typing.List[str], community_cards: typing.List[str]) -> HAND_T:
    cards = Hand(
        cards=[Card.from_str(raw_card) for raw_card in hole_cards + community_cards]
    )
    combination = cards.best_hand

    return combination.name, combination.ranks
