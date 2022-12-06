"""Advent of Code 2022, Day 5."""

import doctest
import re
from collections.abc import Callable


def part1(problem_input: str) -> str:
    """Solution to part 1.

    >>> part1(sample_input)
    'CMZ'
    """
    stack_cfg, procedure = problem_input.split("\n\n")
    stacks = parse_stacks(stack_cfg)
    for step in procedure.splitlines():
        m = re.match(r"move (\d+) from (\d+) to (\d+)", step)
        if m:
            count, src, dest = [int(n) for n in m.groups()]
            for _ in range(count):
                stacks[dest].append(stacks[src].pop())
    return "".join([s[-1] for s in stacks if len(s) > 0])


def part2(problem_input: str) -> str:
    """Solution to part 2.

    >>> part2(sample_input)
    'MCD'
    """
    stack_cfg, procedure = problem_input.split("\n\n")
    stacks = parse_stacks(stack_cfg)
    for step in procedure.splitlines():
        m = re.match(r"move (\d+) from (\d+) to (\d+)", step)
        if m:
            count, src, dest = [int(n) for n in m.groups()]
            stacks[dest] += stacks[src][-count:]
            stacks[src] = stacks[src][:-count]
    return "".join([s[-1] for s in stacks if len(s) > 0])


def parse_stacks(cfg: str) -> list[list[str]]:
    r"""
    >>> parse_stacks(sample_input.split("\n\n")[0])
    [[], ['Z', 'N'], ['M', 'C', 'D'], ['P'], [], [], [], [], [], []]
    """
    labels = cfg.splitlines()[-1]
    lines = cfg.splitlines()[:-1]

    stacks = [[] for _ in range(0, 10)]
    for n in range(1, 10):
        try:
            i = labels.index(str(n))
        except ValueError:
            continue
        for line in lines:
            if len(line) > i and line[i] != " ":
                stacks[n].insert(0, line[i])
    return stacks


def solve(func: Callable[[str], str]) -> None:
    with open("problem_input/day05.txt") as f:
        print(func(f.read()))


if __name__ == "__main__":
    sample_input = """
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
""".strip(
        "\n"
    )

    doctest.testmod(verbose=True)
    solve(part1)
    solve(part2)
