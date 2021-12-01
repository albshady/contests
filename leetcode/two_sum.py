import typing


def two_sum(nums: typing.List[int], target: int) -> typing.List[int]:
    hashmap = {}

    for pos, num in enumerate(nums):
        complement = target - num
        if complement_pos := hashmap.get(complement):
            return [complement_pos, pos]
        hashmap[num] = pos

    raise ValueError("No solution found!")

