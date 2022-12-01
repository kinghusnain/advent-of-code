"""Advent of Code 2022, Day 1."""

import doctest
from typing import Callable, Iterable


def part1(problem_input: str) -> int:
    """Solution to part 1.

    >>> part1(sample_input)
    24000
    """
    caloric_inventory = [sum(v) for v in chunked(problem_input)]
    return max(caloric_inventory)


def part2(problem_input: str) -> int:
    """Solution to part 2.

    >>> part2(sample_input)
    45000
    """
    caloric_inventory = [sum(v) for v in chunked(problem_input)]
    caloric_inventory.sort()
    return sum(caloric_inventory[-3:])


def chunked(input: str) -> Iterable[list[int]]:
    chunk = []
    for s in input.splitlines():
        if s == "":
            yield chunk
            chunk = []
        else:
            chunk.append(int(s))
    if len(chunk) > 0:
        yield chunk


def solve(func: Callable[[str], None]) -> None:
    with open("problem_input/day01.txt") as f:
        problem_input = f.read()
    print(func(problem_input))


if __name__ == "__main__":
    sample_input = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""

    doctest.testmod(verbose=True)
    solve(part1)
    solve(part2)
