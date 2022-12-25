"""Advent of Code 2022, Day 25."""

import doctest
from collections.abc import Callable, Iterable


def part1(problem_input: Iterable[str]) -> str:
    """Solution to part 1.

    >>> part1(sample_input)
    '2=-1=0'
    """
    sum = "0"
    for n in (s.strip() for s in problem_input):
        sum = snafu_add(sum, n)
    return sum


def snafu_add(a: str, b: str) -> str:
    if a == "":
        return b
    if b == "":
        return a
    offset = "=-012".index(a[-1]) + "=-012".index(b[-1]) - 2
    ones = "=-012"[offset % 5]
    if offset < 0:
        rest = snafu_add(snafu_add(a[:-1], "-"), b[:-1])
    elif offset > 4:
        rest = snafu_add(snafu_add(a[:-1], "1"), b[:-1])
    else:
        rest = snafu_add(a[:-1], b[:-1])
    return rest + ones


def solve(func: Callable[[Iterable[str]], str]) -> None:
    with open("problem_input/day25.txt") as f:
        print(func(f))


if __name__ == "__main__":
    sample_input = """
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
""".strip().splitlines()

    doctest.testmod(verbose=True)
    solve(part1)
