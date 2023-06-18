import pytest


class Solution:
    def romanToInt(self, s: str) -> int:
        mapping = {
            "I": 1,
            "V": 5,
            "X": 10,
            "L": 50,
            "C": 100,
            "D": 500,
            "M": 1000,
        }
        result = 0
        previous = 0
        for numeric in s:
            current = mapping[numeric]
            if not previous:
                pass
            elif current <= previous:
                result += previous
            else:
                result -= previous
            previous = current
        result += previous
        return result


@pytest.mark.parametrize(
    "roman_input, expected_output",
    [
        pytest.param("III", 3),
        pytest.param("LVIII", 58),
        pytest.param("MCMXCIV", 1994),
    ],
)
def test_solution(roman_input: str, expected_output: int):
    solution = Solution()
    assert solution.romanToInt(roman_input) == expected_output
