"""
https://www.codewars.com/kata/55c45be3b2079eccff00010f

Your order, please

Your task is to sort a given string.
Each word in the string will contain a single number.
This number is the position the word should have in the result.

Note: Numbers can be from 1 to 9. So 1 will be the first word (not 0).

If the input string is empty, return an empty string.
The words in the input String will only contain valid consecutive numbers.

Examples
```
"is2 Thi1s T4est 3a"  -->  "Thi1s is2 3a T4est"
"4of Fo1r pe6ople g3ood th5e the2"  -->  "Fo1r the2 g3ood 4of th5e pe6ople"
""  -->  ""
```
"""


import typing


def order(sentence: str) -> str:
    if not sentence:
        return sentence

    words_positions = {}

    for word in sentence.split():
        position = _get_number_from_word(word)
        words_positions[position] = word

    return _build_sentence(words_positions)


def _get_number_from_word(word: str) -> int:
    for letter in word:
        try:
            return int(letter)
        except ValueError:
            continue
    raise ValueError(f"No number in word {word}!")


def _build_sentence(words_positions: typing.Mapping[int, str]) -> str:
    return " ".join([words_positions[position] for position in sorted(words_positions)])


if __name__ == '__main__':
    assert order("is2 Thi1s T4est 3a") == "Thi1s is2 3a T4est"
    assert (
        order("4of Fo1r pe6ople g3ood th5e the2") == "Fo1r the2 g3ood 4of th5e pe6ople"
    )
    assert order("") == ""
    print("Tests passed!")
