"""Advent of Code 2022, Day 24."""

import doctest
from collections.abc import Callable
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def part1(problem_input: str) -> int:
    """Solution to part 1.

    >>> part1(sample_input)
    18
    """
    valley_map = list(problem_input.strip().splitlines())
    valley_x_size = len(valley_map[0]) - 2
    valley_y_size = len(valley_map) - 2
    northward_blizzards: set[Point] = set()
    southward_blizzards: set[Point] = set()
    westward_blizzards: set[Point] = set()
    eastward_blizzards: set[Point] = set()
    for y in range(valley_y_size):
        for x in range(valley_x_size):
            c = valley_map[valley_y_size - y][x + 1]
            if c == "^":
                northward_blizzards.add(Point(x, y))
            elif c == "v":
                southward_blizzards.add(Point(x, y))
            elif c == "<":
                westward_blizzards.add(Point(x, y))
            elif c == ">":
                eastward_blizzards.add(Point(x, y))
    entrance = Point(valley_map[0].index(".") - 1, valley_y_size)
    exit = Point(valley_map[-1].index(".") - 1, -1)
    walls = (
        set(
            Point(x, y)
            for x in range(-1, len(valley_map[0]) - 1)
            for y in [-1, len(valley_map) - 2]
        )
        | set(
            Point(x, y)
            for x in [-1, len(valley_map[0]) - 2]
            for y in range(-1, len(valley_map) - 1)
        )
    ) - set([entrance, exit])

    possible_locations: set[Point] = set([entrance])
    minute = 0
    while exit not in possible_locations:
        minute += 1

        northward_blizzards = set(
            Point(x, (y + 1) % valley_y_size) for x, y in northward_blizzards
        )
        southward_blizzards = set(
            Point(x, (y - 1) % valley_y_size) for x, y in southward_blizzards
        )
        westward_blizzards = set(
            Point((x - 1) % valley_x_size, y) for x, y in westward_blizzards
        )
        eastward_blizzards = set(
            Point((x + 1) % valley_x_size, y) for x, y in eastward_blizzards
        )

        future_locations: set[Point] = set()
        for loc in possible_locations:
            valid_moves = (
                set(
                    Point(x, y)
                    for x, y in [
                        loc,
                        (loc.x - 1, loc.y),
                        (loc.x + 1, loc.y),
                        (loc.x, loc.y - 1),
                        (loc.x, loc.y + 1),
                    ]
                    if 0 <= x < valley_x_size and -1 <= y <= valley_y_size
                )
                - walls
                - northward_blizzards
                - southward_blizzards
                - westward_blizzards
                - eastward_blizzards
            )
            future_locations |= valid_moves
        possible_locations = future_locations

        # print(f"Minute {minute}:")
        # for y in range(valley_y_size,-2,-1):
        #     for x in range(-1,valley_x_size+1):
        #         p = Point(x,y)
        #         if p in walls:
        #             print('#', end='')
        #         elif p in northward_blizzards:
        #             print('^', end='')
        #         elif p in southward_blizzards:
        #             print('v', end='')
        #         elif p in westward_blizzards:
        #             print('<', end='')
        #         elif p in eastward_blizzards:
        #             print('>', end='')
        #         else:
        #             print('.', end='')
        #     print()
        # print()

    return minute


def part2(problem_input: str) -> int:
    """Solution to part 2.

    >>> part2(sample_input)
    54
    """
    valley_map = list(problem_input.strip().splitlines())
    valley_x_size = len(valley_map[0]) - 2
    valley_y_size = len(valley_map) - 2
    northward_blizzards: set[Point] = set()
    southward_blizzards: set[Point] = set()
    westward_blizzards: set[Point] = set()
    eastward_blizzards: set[Point] = set()
    for y in range(valley_y_size):
        for x in range(valley_x_size):
            c = valley_map[valley_y_size - y][x + 1]
            if c == "^":
                northward_blizzards.add(Point(x, y))
            elif c == "v":
                southward_blizzards.add(Point(x, y))
            elif c == "<":
                westward_blizzards.add(Point(x, y))
            elif c == ">":
                eastward_blizzards.add(Point(x, y))
    entrance = Point(valley_map[0].index(".") - 1, valley_y_size)
    exit = Point(valley_map[-1].index(".") - 1, -1)
    walls = (
        set(
            Point(x, y)
            for x in range(-1, len(valley_map[0]) - 1)
            for y in [-1, len(valley_map) - 2]
        )
        | set(
            Point(x, y)
            for x in [-1, len(valley_map[0]) - 2]
            for y in range(-1, len(valley_map) - 1)
        )
    ) - set([entrance, exit])

    minute = 0

    possible_locations: set[Point] = set([entrance])
    while exit not in possible_locations:
        minute += 1

        northward_blizzards = set(
            Point(x, (y + 1) % valley_y_size) for x, y in northward_blizzards
        )
        southward_blizzards = set(
            Point(x, (y - 1) % valley_y_size) for x, y in southward_blizzards
        )
        westward_blizzards = set(
            Point((x - 1) % valley_x_size, y) for x, y in westward_blizzards
        )
        eastward_blizzards = set(
            Point((x + 1) % valley_x_size, y) for x, y in eastward_blizzards
        )

        future_locations: set[Point] = set()
        for loc in possible_locations:
            valid_moves = (
                set(
                    Point(x, y)
                    for x, y in [
                        loc,
                        (loc.x - 1, loc.y),
                        (loc.x + 1, loc.y),
                        (loc.x, loc.y - 1),
                        (loc.x, loc.y + 1),
                    ]
                    if 0 <= x < valley_x_size and -1 <= y <= valley_y_size
                )
                - walls
                - northward_blizzards
                - southward_blizzards
                - westward_blizzards
                - eastward_blizzards
            )
            future_locations |= valid_moves
        possible_locations = future_locations

    possible_locations: set[Point] = set([exit])
    while entrance not in possible_locations:
        minute += 1

        northward_blizzards = set(
            Point(x, (y + 1) % valley_y_size) for x, y in northward_blizzards
        )
        southward_blizzards = set(
            Point(x, (y - 1) % valley_y_size) for x, y in southward_blizzards
        )
        westward_blizzards = set(
            Point((x - 1) % valley_x_size, y) for x, y in westward_blizzards
        )
        eastward_blizzards = set(
            Point((x + 1) % valley_x_size, y) for x, y in eastward_blizzards
        )

        future_locations: set[Point] = set()
        for loc in possible_locations:
            valid_moves = (
                set(
                    Point(x, y)
                    for x, y in [
                        loc,
                        (loc.x - 1, loc.y),
                        (loc.x + 1, loc.y),
                        (loc.x, loc.y - 1),
                        (loc.x, loc.y + 1),
                    ]
                    if 0 <= x < valley_x_size and -1 <= y <= valley_y_size
                )
                - walls
                - northward_blizzards
                - southward_blizzards
                - westward_blizzards
                - eastward_blizzards
            )
            future_locations |= valid_moves
        possible_locations = future_locations

    possible_locations: set[Point] = set([entrance])
    while exit not in possible_locations:
        minute += 1

        northward_blizzards = set(
            Point(x, (y + 1) % valley_y_size) for x, y in northward_blizzards
        )
        southward_blizzards = set(
            Point(x, (y - 1) % valley_y_size) for x, y in southward_blizzards
        )
        westward_blizzards = set(
            Point((x - 1) % valley_x_size, y) for x, y in westward_blizzards
        )
        eastward_blizzards = set(
            Point((x + 1) % valley_x_size, y) for x, y in eastward_blizzards
        )

        future_locations: set[Point] = set()
        for loc in possible_locations:
            valid_moves = (
                set(
                    Point(x, y)
                    for x, y in [
                        loc,
                        (loc.x - 1, loc.y),
                        (loc.x + 1, loc.y),
                        (loc.x, loc.y - 1),
                        (loc.x, loc.y + 1),
                    ]
                    if 0 <= x < valley_x_size and -1 <= y <= valley_y_size
                )
                - walls
                - northward_blizzards
                - southward_blizzards
                - westward_blizzards
                - eastward_blizzards
            )
            future_locations |= valid_moves
        possible_locations = future_locations

    return minute


def solve(func: Callable[[str], int]) -> None:
    with open("problem_input/day24.txt") as f:
        print(func(f.read()))


if __name__ == "__main__":
    sample_input = """
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
"""

    doctest.testmod(verbose=True)
    solve(part1)
    solve(part2)
