"""Advent of Code 2022, Day 6."""

import doctest
from collections.abc import Callable, Iterable


def part1(problem_input: str) -> int:
    """Solution to part 1.

    >>> part1("mjqjpqmgbljsphdztnvjfqwrcgsmlb")
    7
    """
    for i in range(len(problem_input) - 4):
        if len(set(problem_input[i : i + 4])) == 4:
            return i + 4
    raise ValueError


def part2(problem_input: str) -> int:
    """Solution to part 2.

    >>> part2("mjqjpqmgbljsphdztnvjfqwrcgsmlb")
    19
    """
    for i in range(len(problem_input) - 14):
        if len(set(problem_input[i : i + 14])) == 14:
            return i + 14
    raise ValueError


def solve(func: Callable[[str], int]) -> None:
    with open("problem_input/day06.txt") as f:
        print(func(f.read()))


if __name__ == "__main__":
    doctest.testmod(verbose=True)
    solve(part1)
    solve(part2)
