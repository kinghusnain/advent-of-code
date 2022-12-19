"""Advent of Code 2022, Day 17."""

import doctest
from collections import namedtuple
from collections.abc import Callable

Point = namedtuple("Point", ["x", "y"])


def part1(problem_input: str) -> int:
    """Solution to part 1.

    >>> part1(">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>")
    3068
    """
    wind = problem_input.strip()
    shapes: list[set[Point]] = [
        set([Point(2, 0), Point(3, 0), Point(4, 0), Point(5, 0)]),  # -
        set([Point(3, 2), Point(2, 1), Point(3, 1), Point(4, 1), Point(3, 0)]),  # +
        set([Point(4, 2), Point(4, 1), Point(2, 0), Point(3, 0), Point(4, 0)]),  # J
        set([Point(2, 0), Point(2, 1), Point(2, 2), Point(2, 3)]),  # I
        set([Point(2, 0), Point(2, 1), Point(3, 0), Point(3, 1)]),  # o
    ]
    cavern: set[Point] = set(
        [Point(x, y) for y in range(6) for x in [-1, 7]]
        + [Point(x, -1) for x in range(7)]
    )
    peak = -1

    t = 0
    for r in range(2022):
        rock = set(Point(p.x, p.y + peak + 4) for p in shapes[r % len(shapes)])
        while True:
            dx = -1 if wind[t % len(wind)] == "<" else 1
            t += 1
            rock_dx = set(Point(p.x + dx, p.y) for p in rock)
            if cavern.isdisjoint(rock_dx):
                rock = rock_dx
            rock_dy = set(Point(p.x, p.y - 1) for p in rock)
            if cavern.isdisjoint(rock_dy):
                rock = rock_dy
            else:
                break
        cavern |= rock
        new_peak = max(y for x, y in cavern if x not in [-1, 7])
        cavern |= set(
            Point(x, y) for y in range(peak + 1, new_peak + 7) for x in [-1, 7]
        )
        peak = new_peak

    return peak + 1


def solve(func: Callable[[str], int]) -> None:
    with open("problem_input/day17.txt") as f:
        print(func(f.read()))


if __name__ == "__main__":
    doctest.testmod(verbose=True)
    solve(part1)
    # solve(part2)
