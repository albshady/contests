from __future__ import annotations

import math
import operator
import pathlib
import re
import typing

import iters
import utils


INPUT_TXT = pathlib.Path('inputs/day08.txt')
NODE_REGEXP = re.compile(r'^(\w{3}) = \((\w{3}), (\w{3})\)$')


def main() -> None:
    navigation = parse_navigation()
    answer_1 = navigation.find_route('AAA', lambda position: position == 'ZZZ')
    answer_2 = solve_2(navigation)
    print(answer_1, answer_2, sep='\n')


class Navigation(typing.NamedTuple):
    instructions: tuple[int, ...]
    nodes: dict[str, tuple[str, str]]

    def find_route(
        self, start: str, finish_predicate: typing.Callable[[str], bool]
    ) -> int:
        position = start
        for step, instruction in iters.Iter(self.instructions).cycle().enumerate():
            position = self.nodes[position][instruction]
            if finish_predicate(position):
                return step + 1
        raise ValueError("Unable to solve_1")


def parse_navigation() -> Navigation:
    lines = utils.read_lines(INPUT_TXT)
    raw_instructions = lines.first().map(str.strip).unwrap()
    nodes_map = lines.skip(1).map(parse_node).reduce(operator.or_).unwrap()
    instructions = (
        iters.Iter(raw_instructions).map(lambda ins: {'L': 0, 'R': 1}[ins]).tuple()
    )
    return Navigation(instructions=instructions, nodes=nodes_map)


def parse_node(line: str) -> dict[str, tuple[str, str]]:
    m = NODE_REGEXP.match(line)
    assert m is not None
    return {m.group(1): (m.group(2), m.group(3))}


def solve_2(navigation: Navigation) -> int:
    distances = (
        navigation.find_route(start, lambda position: position.endswith('Z'))
        for start in navigation.nodes.keys()
        if start.endswith('A')
    )
    return math.lcm(*distances)


if __name__ == "__main__":
    main()
