"""Advent of Code 2022, Day 4."""

import doctest
from collections.abc import Callable, Iterable


def part1(problem_input: Iterable[str]) -> int:
    """Solution to part 1.

    >>> part1(sample_input)
    2
    """
    ranges = (assignments(p) for p in problem_input)
    return len(
        [1 for a, b in ranges if set(a).issubset(set(b)) or set(b).issubset(set(a))]
    )


def part2(problem_input: Iterable[str]) -> int:
    """Solution to part 2.

    >>> part2(sample_input)
    4
    """
    ranges = (assignments(p) for p in problem_input)
    return len([1 for a, b in ranges if set(a) & set(b) != set()])


def assignments(ranges_str: str) -> tuple[range, range]:
    """
    >>> assignments("12-99,3-8000") == (range(12,100), range(3,8001))
    True
    """
    ranges = [rs.split("-") for rs in ranges_str.strip().split(",")]
    ranges = [(int(l), int(u) + 1) for l, u in ranges]
    return (range(*ranges[0]), range(*ranges[1]))


def solve(func: Callable[[Iterable[str]], int]) -> None:
    with open("problem_input/day04.txt") as f:
        print(func(f))


if __name__ == "__main__":
    sample_input = """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
""".strip().splitlines()

    doctest.testmod(verbose=True)
    solve(part1)
    solve(part2)
