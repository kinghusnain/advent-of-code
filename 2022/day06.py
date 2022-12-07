"""Advent of Code 2022, Day 6."""

import doctest
from collections.abc import Callable


def part1(problem_input: str) -> int:
    """Solution to part 1.

    >>> part1("mjqjpqmgbljsphdztnvjfqwrcgsmlb")
    7
    >>> part1("bvwbjplbgvbhsrlpgdmjqwftvncz")
    5
    >>> part1("nppdvjthqldpwncqszvftbrmjlhg")
    6
    >>> part1("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg")
    10
    >>> part1("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw")
    11
    """
    for i in range(4, len(problem_input)):
        if len(set(problem_input[i - 4 : i])) == 4:
            return i
    raise ValueError


def part2(problem_input: str) -> int:
    """Solution to part 2.

    >>> part2("mjqjpqmgbljsphdztnvjfqwrcgsmlb")
    19
    >>> part2("bvwbjplbgvbhsrlpgdmjqwftvncz")
    23
    >>> part2("nppdvjthqldpwncqszvftbrmjlhg")
    23
    >>> part2("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg")
    29
    >>> part2("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw")
    26
    """
    for i in range(14, len(problem_input)):
        if len(set(problem_input[i - 14 : i])) == 14:
            return i
    raise ValueError


def solve(func: Callable[[str], int]) -> None:
    with open("problem_input/day06.txt") as f:
        print(func(f.read()))


if __name__ == "__main__":
    doctest.testmod(verbose=True)
    solve(part1)
    solve(part2)
