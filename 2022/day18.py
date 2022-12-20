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
    droplet = [
        Point(int(x), int(y), int(z))
        for x, y, z in (l.split(",") for l in problem_input)
    ]
    total_surface: frozenset[tuple[Point, tuple]] = frozenset()
    for p in droplet:
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
        total_surface = total_surface ^ p_surfaces

    bubbles: set[Point] = set()
    for z in range(20):
        for y in range(20):
            min_x = min((p.x for p in droplet if p.y == y and p.z == z), default=999)
            max_x = max((p.x for p in droplet if p.y == y and p.z == z), default=-999)
            for x in range(min_x, max_x):
                if Point(x, y, z) not in droplet:
                    bubbles.add(Point(x, y, z))

    # Remove non-bubbles
    checked: set[Point] = set()
    to_check: set[Point] = set([Point(-1, 0, 0)])
    while len(to_check) > 0:
        p = to_check.pop()
        if p in bubbles:
            bubbles.remove(p)
        checked.add(p)
        adjacent = [
            Point(p.x - 1, p.y, p.z),
            Point(p.x + 1, p.y, p.z),
            Point(p.x, p.y - 1, p.z),
            Point(p.x, p.y + 1, p.z),
            Point(p.x, p.y, p.z - 1),
            Point(p.x, p.y, p.z + 1),
        ]
        to_check |= set(
            p
            for p in adjacent
            if p.x in range(0, 20)
            and p.y in range(0, 20)
            and p.z in range(0, 20)
            and p not in checked
            and p not in droplet
        )

    bubbles_surface: frozenset[tuple[Point, tuple]] = frozenset()
    for p in bubbles:
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
        bubbles_surface = bubbles_surface ^ p_surfaces

    return len(total_surface - bubbles_surface)


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
    solve(part2)
