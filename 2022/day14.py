"""Advent of Code 2022, Day 14."""

import doctest
from collections import namedtuple
from collections.abc import Callable, Iterable

Point = namedtuple("Point", ["x", "y"])


def part1(problem_input: Iterable[str]) -> int:
    """Solution to part 1.

    >>> part1(sample_input)
    24
    """
    rock_formations = [
        [Point(*[int(n) for n in p.split(",")]) for p in f.split("->")]
        for f in problem_input
    ]
    occupied_space: dict[Point, str] = {}
    for formation in rock_formations:
        while len(formation) >= 2:
            start, end = formation[:2]
            if start.x == end.x:
                for y in range(min(start.y, end.y), max(start.y, end.y) + 1):
                    occupied_space[Point(start.x, y)] = "#"
            else:
                for x in range(min(start.x, end.x), max(start.x, end.x) + 1):
                    occupied_space[Point(x, start.y)] = "#"
            formation = formation[1:]

    origin = Point(500, 0)
    floor_y = max(p.y for p in occupied_space)
    is_void_breached = False
    while not is_void_breached:
        sand = origin
        while True:
            if sand.y > floor_y:
                is_void_breached = True
                break
            if Point(sand.x, sand.y + 1) not in occupied_space:
                sand = Point(sand.x, sand.y + 1)
            elif Point(sand.x - 1, sand.y + 1) not in occupied_space:
                sand = Point(sand.x - 1, sand.y + 1)
            elif Point(sand.x + 1, sand.y + 1) not in occupied_space:
                sand = Point(sand.x + 1, sand.y + 1)
            else:
                occupied_space[sand] = "o"
                break
        if origin in occupied_space:
            break
    return len([x for x in occupied_space.values() if x == "o"])


def part2(problem_input: Iterable[str]) -> int:
    """Solution to part 2.

    >>> part2(sample_input)
    93
    """
    rock_formations = [
        [Point(*[int(n) for n in p.split(",")]) for p in f.split("->")]
        for f in problem_input
    ]
    occupied_space: dict[Point, str] = {}
    for formation in rock_formations:
        while len(formation) >= 2:
            start, end = formation[:2]
            if start.x == end.x:
                for y in range(min(start.y, end.y), max(start.y, end.y) + 1):
                    occupied_space[Point(start.x, y)] = "#"
            else:
                for x in range(min(start.x, end.x), max(start.x, end.x) + 1):
                    occupied_space[Point(x, start.y)] = "#"
            formation = formation[1:]

    origin = Point(500, 0)
    floor_y = max(p.y for p in occupied_space) + 2
    while True:
        sand = origin
        while True:
            down = Point(sand.x, sand.y + 1)
            down_left = Point(sand.x - 1, sand.y + 1)
            down_right = Point(sand.x + 1, sand.y + 1)
            if down not in occupied_space and down.y != floor_y:
                sand = down
            elif down_left not in occupied_space and down_left.y != floor_y:
                sand = down_left
            elif down_right not in occupied_space and down_right.y != floor_y:
                sand = down_right
            else:
                occupied_space[sand] = "o"
                break
        if origin in occupied_space:
            break
    return len([x for x in occupied_space.values() if x == "o"])


def solve(func: Callable[[Iterable[str]], int]) -> None:
    with open("problem_input/day14.txt") as f:
        print(func(f))


if __name__ == "__main__":
    sample_input = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
""".strip().splitlines()

    doctest.testmod(verbose=True)
    solve(part1)
    solve(part2)
