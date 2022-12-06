"""Advent of Code 2022, Day 3."""

import doctest
from collections.abc import Callable, Generator, Iterable, Iterator


def part1(problem_input: Iterable[str]) -> int:
    """Solution to part 1.

    >>> part1(sample_input)
    157
    """
    halves = ((r[: len(r) // 2], r[len(r) // 2 :]) for r in problem_input)
    return sum(prio((set(a) & set(b)).pop()) for a, b in halves)


def part2(problem_input: Iterable[str]) -> int:
    """Solution to part 2.

    >>> part2(sample_input)
    70
    """
    thirds = threes(r.strip() for r in problem_input)
    return sum(prio((set(a) & set(b) & set(c)).pop()) for a, b, c in thirds)


def prio(item: str) -> int:
    return " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".index(item)


def threes(iter: Iterator[str]) -> Generator[list[str], None, None]:
    while True:
        try:
            yield [next(iter), next(iter), next(iter)]
        except StopIteration:
            break


def solve(func: Callable[[Iterable[str]], int]) -> None:
    with open("problem_input/day03.txt") as f:
        print(func(f))


if __name__ == "__main__":
    sample_input = """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
""".strip().splitlines()

    doctest.testmod(verbose=True)
    solve(part1)
    solve(part2)
