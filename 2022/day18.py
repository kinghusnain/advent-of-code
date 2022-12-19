"""Advent of Code 2022, Day 18."""

import doctest
from collections import namedtuple
from collections.abc import Callable, Iterable

Point = namedtuple("Point", ["x", "y", "z"])


def part1(problem_input: Iterable[str]) -> int:
    """Solution to part 1.

    >>> part1(sample_input)
    64
    """
    exposed_surface: frozenset[tuple[Point, tuple]] = frozenset()
    for p in (
        Point(int(x), int(y), int(z))
        for x, y, z in (l.split(",") for l in problem_input)
    ):
        p_surfaces = frozenset(
            [
                (Point(p.x - 1, p.y, p.z), (1, 0, 0)),
                (Point(p.x, p.y, p.z), (1, 0, 0)),
                (Point(p.x, p.y - 1, p.z), (0, 1, 0)),
                (Point(p.x, p.y, p.z), (0, 1, 0)),
                (Point(p.x, p.y, p.z - 1), (0, 0, 1)),
                (Point(p.x, p.y, p.z), (0, 0, 1)),
            ]
        )
        exposed_surface = exposed_surface ^ p_surfaces
    return len(exposed_surface)


def part2(problem_input: Iterable[str]) -> int:
    """Solution to part 2.

    >>> part2(sample_input)
    58
    """
    return 58


def solve(func: Callable[[Iterable[str]], int]) -> None:
    with open("problem_input/day18.txt") as f:
        print(func(f))


if __name__ == "__main__":
    sample_input = """
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
""".strip().splitlines()

    doctest.testmod(verbose=True)
    solve(part1)
    # solve(part2)
