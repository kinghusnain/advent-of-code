"""Advent of Code 2022, Day 2."""

import doctest
from collections.abc import Callable, Generator, Iterable


def part1(problem_input: Iterable[str]) -> int:
    """Solution to part 1.

    >>> part1(["A Y", "B X", "C Z"])
    15
    """
    strategy = [x.split() for x in problem_input]
    scores = [round_outcome(them, you) + shape_value[you] for them, you in strategy]
    return sum(scores)


shape_value = {"A": 1, "B": 2, "C": 3, "X": 1, "Y": 2, "Z": 3}


def round_outcome(them, you):
    if shape_value[you] - shape_value[them] in (1, -2):
        return 6
    elif shape_value[you] == shape_value[them]:
        return 3
    else:
        return 0


def part2(problem_input: Iterable[str]) -> int:
    """Solution to part 2.

    >>> part2(["A Y", "B X", "C Z"])
    12
    """
    strategy = [x.split() for x in problem_input]
    scores = [
        outcome_value[outcome] + round_move(them, outcome) for them, outcome in strategy
    ]
    return sum(scores)


outcome_value = {"X": 0, "Y": 3, "Z": 6}


def round_move(them, outcome):
    themval = shape_value[them]
    if outcome == "X":  # lose
        return themval - 1 if themval >= 2 else 3
    elif outcome == "Y":  # draw
        return themval
    else:  # win
        return themval + 1 if themval <= 2 else 1


def solve(func: Callable[[Iterable[str]], int]) -> None:
    with open("problem_input/day02.txt") as f:
        print(func(f))


if __name__ == "__main__":
    doctest.testmod(verbose=True)
    solve(part1)
    solve(part2)
