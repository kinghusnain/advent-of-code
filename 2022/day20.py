"""Advent of Code 2022, Day 20."""

import doctest
from collections.abc import Callable, Iterable


def part1(problem_input: Iterable[str]) -> int:
    """Solution to part 1.

    >>> part1(sample_input)
    3
    """
    original_numbers: list[int] = [int(n) for n in problem_input]
    length = len(original_numbers)
    mixed_order = [i for i in range(length)]
    mixed = [original_numbers[i] for i in mixed_order]
    for orig_i in range(length):
        n = original_numbers[orig_i]
        i = mixed_order.index(orig_i)

        if n > 0:
            for k in range(n):
                m = mixed_order[(i + k + 1) % length]
                mixed_order[(i + k + 1) % length] = mixed_order[(i + k) % length]
                mixed_order[(i + k) % length] = m
        elif n < 0:
            for k in range(abs(n)):
                m = mixed_order[(i - k - 1) % length]
                mixed_order[(i - k - 1) % length] = mixed_order[(i - k) % length]
                mixed_order[(i - k) % length] = m

        mixed = [original_numbers[i] for i in mixed_order]
    zi = mixed.index(0)
    return (
        mixed[(zi + 1000) % length]
        + mixed[(zi + 2000) % length]
        + mixed[(zi + 3000) % length]
    )


def solve(func: Callable[[Iterable[str]], int]) -> None:
    with open("problem_input/day20.txt") as f:
        print(func(f.read().strip().splitlines()))


if __name__ == "__main__":
    sample_input = """
1
2
-3
3
-2
0
4
""".strip().splitlines()

    doctest.testmod(verbose=True)
    solve(part1)
    # solve(part2)
