"""Advent of Code 2022, Day 22."""

import doctest
import re
from collections import namedtuple
from collections.abc import Callable


Point = namedtuple("Point", ["x", "y"])
right_facing = 0
down_facing = 1
left_facing = 2
up_facing = 3


def part1(problem_input: str) -> int:
    """Solution to part 1.

    >>> part1(sample_input)
    6032
    """
    board_map, dir_str = problem_input.split("\n\n")

    board_map = board_map.split("\n")
    board: dict[Point, bool] = {}
    for y in range(len(board_map)):
        for x in range(len(board_map[y])):
            c = board_map[y][x]
            if c != " ":
                board[Point(x + 1, y + 1)] = c == "."

    directions = [m[1] for m in re.finditer(r"(\d+|[LR])", dir_str)]

    loc = Point(min(x for x, y in board if y == 1), 1)
    facing = right_facing
    for d in directions:
        if d == "L":
            facing = (facing - 1) % 4
        elif d == "R":
            facing = (facing + 1) % 4
        elif facing == up_facing:
            for _ in range(int(d)):
                next = Point(loc.x, loc.y - 1)
                if next not in board:
                    wrap_y = max(y for x, y in board if x == loc.x)
                    next = Point(loc.x, wrap_y)
                if board[next]:
                    loc = next
        elif facing == down_facing:
            for _ in range(int(d)):
                next = Point(loc.x, loc.y + 1)
                if next not in board:
                    wrap_y = min(y for x, y in board if x == loc.x)
                    next = Point(loc.x, wrap_y)
                if board[next]:
                    loc = next
        elif facing == left_facing:
            for _ in range(int(d)):
                next = Point(loc.x - 1, loc.y)
                if next not in board:
                    wrap_x = max(x for x, y in board if y == loc.y)
                    next = Point(wrap_x, loc.y)
                if board[next]:
                    loc = next
        elif facing == right_facing:
            for _ in range(int(d)):
                next = Point(loc.x + 1, loc.y)
                if next not in board:
                    wrap_x = min(x for x, y in board if y == loc.y)
                    next = Point(wrap_x, loc.y)
                if board[next]:
                    loc = next
        else:
            raise Exception

    return 1000 * loc.y + 4 * loc.x + facing


def part2(problem_input: str) -> int:
    """Solution to part 2.

    >>> part2(sample_input)
    0
    """
    return 0


def solve(func: Callable[[str], int]) -> None:
    with open("problem_input/day22.txt") as f:
        print(func(f.read()))


if __name__ == "__main__":
    sample_input = """\
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""

    doctest.testmod(verbose=True)
    solve(part1)
    # solve(part2)
