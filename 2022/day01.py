"""Advent of Code 2022, Day 1."""

import doctest
from collections.abc import Callable, Generator, Iterable


def part1(problem_input: Iterable[str]) -> int:
    """Solution to part 1.

    >>> part1(sample_input)
    24000
    """
    caloric_inventory = [sum(v) for v in chunked(problem_input)]
    return max(caloric_inventory)


def part2(problem_input: Iterable[str]) -> int:
    """Solution to part 2.

    >>> part2(sample_input)
    45000
    """
    caloric_inventory = [sum(v) for v in chunked(problem_input)]
    caloric_inventory.sort()
    return sum(caloric_inventory[-3:])


def chunked(input: Iterable[str]) -> Generator[list[int], None, None]:
    chunk = []
    for s in input:
        if s.strip() == "":
            yield chunk
            chunk = []
        else:
            chunk.append(int(s))
    if len(chunk) > 0:
        yield chunk


def solve(func: Callable[[Iterable[str]], int]) -> None:
    with open("problem_input/day01.txt") as f:
        print(func(f))


if __name__ == "__main__":
    sample_input = """
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
""".splitlines()

    doctest.testmod(verbose=True)
    solve(part1)
    solve(part2)
