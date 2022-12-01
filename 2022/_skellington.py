"""Advent of Code 2022, Day 00."""

import doctest


def part1(problem_input: list[int]) -> int:
    """Solution to part 1.

    >>> part1(sample_input)
    0
    """
    return 0


def part2(problem_input: list[int]) -> int:
    """Solution to part 2.

    >>> part2(sample_input)
    0
    """
    return 0


def solve():
    with open("problem_input/day00.txt") as f:
        problem_input = [int(n) for n in f.readlines()]
    print(part1(problem_input))
    print(part2(problem_input))


if __name__ == "__main__":
    sample_input = [
        int(n)
        for n in """
1
2
3
    """.strip().split()
    ]

    doctest.testmod(verbose=True)
    solve()
