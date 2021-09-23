"""
https://www.codewars.com/kata/59ccf051dcc4050f7800008f

Buddy pairs

You know what divisors of a number are.
The divisors of a positive integer n are said to be proper
when you consider only the divisors other than n itself.
In the following description, divisors will mean proper divisors.
For example for 100 they are 1, 2, 4, 5, 10, 20, 25, and 50.

Let s(n) be the sum of these proper divisors of n.
Call buddy two positive integers such that
the sum of the proper divisors of each number is one more than the other number:

(n, m) are a pair of buddy if s(m) = n + 1 and s(n) = m + 1

For example 48 & 75 is such a pair:

Divisors of 48 are: 1, 2, 3, 4, 6, 8, 12, 16, 24 --> sum: 76 = 75 + 1
Divisors of 75 are: 1, 3, 5, 15, 25 --> sum: 49 = 48 + 1

Task
Given two positive integers start and limit, the function buddy(start, limit)
should return the first pair (n m) of buddy pairs such that
n (positive integer) is between start (inclusive) and limit (inclusive);
m can be greater than limit and has to be greater than n

If there is no buddy pair satisfying the conditions, then return "Nothing"
"""


import math
import typing


BUDDY_PAIR = typing.List[int]
BUDDY_PAIR_OR_NOTHING = typing.Union[BUDDY_PAIR, str]


def get_divisors_sum(number: int) -> int:
    divisor_sum = 1

    for divisor in range(2, int(math.sqrt(number)) + 1):
        if number % divisor != 0:
            continue

        if (partnered_divisor := number // divisor) != divisor:
            divisor_sum += partnered_divisor
        divisor_sum += divisor

    return divisor_sum


def find_buddy_pairs(start: int, limit: int) -> typing.Iterator[BUDDY_PAIR]:
    for lower_partner in range(start, limit + 1):
        divisors_sum = get_divisors_sum(lower_partner)
        if lower_partner > divisors_sum:
            continue
        greater_partner = divisors_sum - 1
        if get_divisors_sum(greater_partner) == lower_partner + 1:
            yield [lower_partner, greater_partner]


def buddy(start: int, limit: int) -> BUDDY_PAIR_OR_NOTHING:
    for buddy_pair in find_buddy_pairs(start, limit):
        return buddy_pair
    return "Nothing"


if __name__ == '__main__':
    assert buddy(10, 50) == [48, 75]
    assert buddy(2177, 4357) == "Nothing"
    assert buddy(57345, 90061) == [62744, 75495]
    assert buddy(1071625, 1103735) == [1081184, 1331967]
    print("Tests passed!")
