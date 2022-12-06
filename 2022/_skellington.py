"""Advent of Code 2022, Day 00."""

import doctest
from collections.abc import Callable, Iterable


def part1(problem_input: Iterable[str]) -> int:
    """Solution to part 1.

    >>> part1(sample_input)
    0
    """
    return 0


def part2(problem_input: Iterable[str]) -> int:
    """Solution to part 2.

    >>> part2(sample_input)
    0
    """
    return 0


def solve(func: Callable[[Iterable[str]], int]) -> None:
    with open("problem_input/day00.txt") as f:
        print(func(f))


if __name__ == "__main__":
    sample_input = """
1
2
3
""".strip().splitlines()

    doctest.testmod(verbose=True)
    # solve(part1)
    # solve(part2)
