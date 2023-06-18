import collections

import pytest


class Solution:
    def isValid(self, s: str) -> bool:
        brackets_map = {"(": ")", "[": "]", "{": "}"}
        stack = collections.deque()
        for char in s:
            if char in brackets_map.keys():
                stack.append(char)
            elif char in brackets_map.values():
                if not stack:
                    return False
                last_bracket = stack.pop()
                if not brackets_map[last_bracket] == char:
                    return False
        return not stack


@pytest.mark.parametrize(
    "s, expected",
    (
        pytest.param("()", True),
        pytest.param("()[]{}", True),
        pytest.param("(]", False),
        pytest.param("][", False),
    ),
)
def test_solution(s, expected):
    solution = Solution()
    assert solution.isValid(s) is expected
