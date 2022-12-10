"""Advent of Code 2022, Day 9."""

import doctest
from collections import namedtuple
from collections.abc import Callable, Iterable


def part1(problem_input: Iterable[str]) -> int:
    """Solution to part 1.

    >>> part1(sample_input)
    13
    """
    Point = namedtuple("Point", ["x", "y"])
    head = Point(0, 0)
    tail = Point(0, 0)
    visited = set([tail])

    steps = "".join([d * int(n) for d, n in [s.split() for s in problem_input]])
    for step in steps:
        if step == "U":
            head = Point(head.x, head.y + 1)
        elif step == "D":
            head = Point(head.x, head.y - 1)
        elif step == "L":
            head = Point(head.x - 1, head.y)
        elif step == "R":
            head = Point(head.x + 1, head.y)
        else:
            raise ValueError

        xdiff = head.x - tail.x
        ydiff = head.y - tail.y

        if abs(xdiff) > 1 and ydiff == 0:
            tail = Point(tail.x + xdiff // abs(xdiff), tail.y)
        elif abs(ydiff) > 1 and xdiff == 0:
            tail = Point(tail.x, tail.y + ydiff // abs(ydiff))
        elif abs(xdiff) > 1 or abs(ydiff) > 1:
            tail = Point(tail.x + xdiff // abs(xdiff), tail.y)
            tail = Point(tail.x, tail.y + ydiff // abs(ydiff))

        visited.add(tail)

    return len(visited)


def part2(problem_input: Iterable[str]) -> int:
    """Solution to part 2.

    >>> part2(sample_input)
    1
    >>> part2(sample_input2)
    36
    """
    Point = namedtuple("Point", ["x", "y"])
    knots = [Point(0, 0) for _ in range(10)]
    visited = set([knots[-1]])

    def follow(h: int, t: int) -> None:
        head = knots[h]
        tail = knots[t]

        xdiff = head.x - tail.x
        ydiff = head.y - tail.y

        if abs(xdiff) > 1 and ydiff == 0:
            tail = Point(tail.x + xdiff // abs(xdiff), tail.y)
        elif abs(ydiff) > 1 and xdiff == 0:
            tail = Point(tail.x, tail.y + ydiff // abs(ydiff))
        elif abs(xdiff) > 1 or abs(ydiff) > 1:
            tail = Point(tail.x + xdiff // abs(xdiff), tail.y)
            tail = Point(tail.x, tail.y + ydiff // abs(ydiff))

        knots[h] = head
        knots[t] = tail

    steps = "".join([d * int(n) for d, n in [s.split() for s in problem_input]])
    for step in steps:
        if step == "U":
            knots[0] = Point(knots[0].x, knots[0].y + 1)
        elif step == "D":
            knots[0] = Point(knots[0].x, knots[0].y - 1)
        elif step == "L":
            knots[0] = Point(knots[0].x - 1, knots[0].y)
        elif step == "R":
            knots[0] = Point(knots[0].x + 1, knots[0].y)
        else:
            raise ValueError

        for h in range(len(knots) - 1):
            follow(h, h + 1)

        visited.add(knots[-1])

    return len(visited)


def solve(func: Callable[[Iterable[str]], int]) -> None:
    with open("problem_input/day09.txt") as f:
        print(func(f))


if __name__ == "__main__":
    sample_input = """
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
""".strip().splitlines()

    sample_input2 = """
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
""".strip().splitlines()

    doctest.testmod(verbose=True)
    solve(part1)
    solve(part2)
