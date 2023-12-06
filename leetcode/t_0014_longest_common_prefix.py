from typing import List


class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        result = ""
        for letters in zip(*strs):
            s = set(letters)
            if len(s) > 1:
                return result
            result += s.pop()
        return result
