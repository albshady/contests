from src.texas_holdem_cards import hand


def test_nothing():
    assert hand(["K♠", "A♦"], ["J♣", "Q♥", "9♥", "2♥", "3♦"]) == (
        "nothing",
        ["A", "K", "Q", "J", "9"],
    )


def test_pair():
    assert hand(["K♠", "Q♦"], ["J♣", "Q♥", "9♥", "2♥", "3♦"]) == (
        "pair",
        ["Q", "K", "J", "9"],
    )


def test_two_pair():
    assert hand(["K♠", "J♦"], ["J♣", "K♥", "9♥", "2♥", "3♦"]) == (
        "two pair",
        ["K", "J", "9"],
    )


def test_three_of_a_kind():
    assert hand(["4♠", "9♦"], ["J♣", "Q♥", "Q♠", "2♥", "Q♦"]) == (
        "three-of-a-kind",
        ["Q", "J", "9"],
    )


def test_straight():
    assert hand(["Q♠", "2♦"], ["J♣", "10♥", "9♥", "K♥", "3♦"]) == (
        "straight",
        ["K", "Q", "J", "10", "9"],
    )


def test_flush():
    assert hand(["A♠", "K♦"], ["J♥", "5♥", "10♥", "Q♥", "3♥"]) == (
        "flush",
        ["Q", "J", "10", "5", "3"],
    )


def test_full_house():
    assert hand(["A♠", "A♦"], ["K♣", "K♥", "A♥", "Q♥", "3♦"]) == (
        "full house",
        ["A", "K"],
    )


def test_four_of_a_kind():
    assert hand(["2♠", "3♦"], ["2♣", "2♥", "3♠", "3♥", "2♦"]) == (
        "four-of-a-kind",
        ["2", "3"],
    )


def test_straight_flush():
    assert hand(["8♠", "6♠"], ["7♠", "5♠", "9♠", "J♠", "10♠"]) == (
        "straight-flush",
        ["J", "10", "9", "8", "7"],
    )
