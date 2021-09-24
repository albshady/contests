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
- Tiebreaker is first the rank, then the rank of the remaining card.
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


@dataclasses.dataclass
class CardRank:
    HIGHER_CARDS_VALUES = {
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14,
    }

    def __init__(self, name: str) -> None:
        self.name = name
        self.value = self.get_value(rank=name)

    @classmethod
    def get_value(cls, rank: str) -> int:
        return cls.HIGHER_CARDS_VALUES.get(rank) or int(rank)

    def __lt__(self, other: typing.Any) -> bool:
        assert isinstance(other, CardRank)

        return self.value < other.value


@dataclasses.dataclass
class Card:
    rank: CardRank
    suit: str

    @classmethod
    def from_str(cls, representation: str) -> 'Card':
        rank = CardRank(name=representation[:-1])
        suit = representation[-1]
        return cls(rank=rank, suit=suit)

    def __lt__(self, other: object) -> bool:
        assert isinstance(other, Card)

        return self.rank < other.rank

    def __eq__(self, other: object) -> bool:
        assert isinstance(other, Card)

        return repr(self) == repr(other)

    def __repr__(self) -> str:
        return f'{self.rank.name}{self.suit}'


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


@dataclasses.dataclass(frozen=True)
class Combination:
    name: CombinationName
    cards: typing.List[Card]

    @property
    def ranks(self) -> typing.List[str]:
        return self._order_ranks_by_occurencies()

    def _order_ranks_by_occurencies(self) -> typing.List[str]:
        occurencies: typing.Counter[str] = collections.Counter()
        for card in self.cards:
            occurencies[card.rank.name] += 1
        return sorted(
            list(occurencies.keys()),
            key=lambda rank: (occurencies[rank], CardRank.get_value(rank)),
            reverse=True,
        )


class Hand:
    def __init__(self, cards: typing.List[Card]) -> None:
        self.cards = sorted(cards, reverse=True)

    @property
    def best_hand(self) -> Combination:
        return self._fill_up_to_5_cards(combination=self._best_combination)

    @property
    def _best_combination(self) -> Combination:
        if flush := self.flush:
            if Hand(cards=flush).straight:
                return Combination(name=CombinationName.STRAIGHT_FLUSH, cards=flush)
            return Combination(name=CombinationName.FLUSH, cards=flush)

        most_of_a_kind = self.most_of_a_kind
        most_of_another_kind = self._other_hand_left(
            cards_used=most_of_a_kind
        ).most_of_a_kind

        if len(most_of_a_kind) == 4:
            return Combination(
                name=CombinationName.FOUR_OF_A_KIND, cards=most_of_a_kind
            )
        if len(most_of_a_kind) == 3 and len(most_of_another_kind) >= 2:
            return Combination(
                name=CombinationName.FULL_HOUSE,
                cards=most_of_a_kind + most_of_another_kind,
            )
        if straight := self.straight:
            return Combination(name=CombinationName.STRAIGHT, cards=straight)
        if len(most_of_a_kind) == 3:
            return Combination(
                name=CombinationName.THREE_OF_A_KIND,
                cards=most_of_a_kind,
            )
        if len(most_of_a_kind) == 2:
            if len(most_of_another_kind) == 2:
                return Combination(
                    name=CombinationName.TWO_PAIR,
                    cards=most_of_a_kind + most_of_another_kind,
                )
            return Combination(name=CombinationName.PAIR, cards=most_of_a_kind)
        return Combination(name=CombinationName.NOTHING, cards=self.cards[:5])

    @property
    def most_of_a_kind(self) -> typing.List[Card]:
        ranks = collections.defaultdict(list)
        for card in self.cards:
            ranks[card.rank.value].append(card)
        most_with_same_rank = sorted(ranks.values(), key=lambda cards: len(cards))[-1]
        return most_with_same_rank if len(most_with_same_rank) >= 2 else []

    @property
    def straight(self) -> typing.List[Card]:
        progression = [self.cards[0]]

        for card in self.cards[1:]:
            if card.rank.value == progression[-1].rank.value:
                continue  # skip same rank
            if card.rank.value + 1 != progression[-1].rank.value:
                progression = [card]
                continue  # progression stopped
            progression.append(card)
            if len(progression) == 5:
                return progression
        return []

    @property
    def flush(self) -> typing.List[Card]:
        suits = collections.defaultdict(list)
        for card in self.cards:
            suits[card.suit].append(card)
        for cards in suits.values():
            if len(cards) >= 5:
                return cards
        return []

    def _fill_up_to_5_cards(self, combination: Combination) -> Combination:
        number_of_cards_to_fill = 5 - len(combination.cards)
        if number_of_cards_to_fill == 0:
            return combination
        if number_of_cards_to_fill < 0:
            return Combination(name=combination.name, cards=combination.cards[:5])

        hand_left = self._other_hand_left(cards_used=combination.cards)

        return Combination(
            name=combination.name,
            cards=combination.cards + hand_left.cards[:number_of_cards_to_fill],
        )

    def _other_hand_left(self, cards_used: typing.List[Card]) -> 'Hand':
        cards = []
        for card in self.cards:
            if card in cards_used:
                continue
            cards.append(card)
        return Hand(cards=cards)


HAND_T = typing.Tuple[CombinationName, typing.List[str]]


def hand(hole_cards: typing.List[str], community_cards: typing.List[str]) -> HAND_T:
    cards = Hand(
        cards=[
            Card.from_str(representation=card) for card in hole_cards + community_cards
        ]
    )
    combination = cards.best_hand

    return combination.name, combination.ranks
