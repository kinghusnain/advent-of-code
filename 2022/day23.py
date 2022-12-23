"""Advent of Code 2022, Day 23."""

import doctest
from collections import namedtuple
from collections.abc import Callable, Iterable


Point = namedtuple("Point", ["x", "y"])


def part1(problem_input: Iterable[str]) -> int:
    """Solution to part 1.

    >>> part1(sample_input)
    110
    """
    elf_positions: set[Point] = set()
    y = 0
    for row in problem_input:
        for x in range(len(row)):
            if row[x] == "#":
                elf_positions.add(Point(x, y))
        y -= 1

    directions = [Point(0, 1), Point(0, -1), Point(-1, 0), Point(1, 0)]
    for _round in range(10):
        # print("    3210123456789")
        # for y in range(-2, 11):
        #     print(f"{-y:3} ", end="")
        #     for x in range(-3, 11):
        #         if Point(x, -y) in elf_positions:
        #             print("#", end="")
        #         else:
        #             print(".", end="")
        #     print()
        # print()

        proposed_moves: dict[Point, Point] = {}
        for e in elf_positions:
            if (
                set(
                    [
                        Point(e.x - 1, e.y + 1),
                        Point(e.x, e.y + 1),
                        Point(e.x + 1, e.y + 1),
                        Point(e.x - 1, e.y),
                        Point(e.x + 1, e.y),
                        Point(e.x - 1, e.y - 1),
                        Point(e.x, e.y - 1),
                        Point(e.x + 1, e.y - 1),
                    ]
                )
                & elf_positions
                == set()
            ):
                continue
            for d in directions:
                if d.x == 0:
                    to_examine = set(Point(e.x + dx, e.y + d.y) for dx in [-1, 0, 1])
                    if elf_positions & to_examine == set():
                        proposed_moves[e] = Point(e.x + d.x, e.y + d.y)
                        break
                else:
                    to_examine = set(Point(e.x + d.x, e.y + dy) for dy in [-1, 0, 1])
                    if elf_positions & to_examine == set():
                        proposed_moves[e] = Point(e.x + d.x, e.y + d.y)
                        break
        new_positions: set[Point] = set()
        for e in elf_positions:
            if (
                e in proposed_moves
                and len(
                    [
                        dest
                        for dest in proposed_moves.values()
                        if dest == proposed_moves[e]
                    ]
                )
                == 1
            ):
                new_positions.add(proposed_moves[e])
            else:
                new_positions.add(e)
        elf_positions = new_positions
        directions = directions[1:] + [directions[0]]

    min_x = min(x for x, y in elf_positions)
    max_x = max(x for x, y in elf_positions)
    min_y = min(y for x, y in elf_positions)
    max_y = max(y for x, y in elf_positions)
    total_tiles = (max_x+1 - min_x) * (max_y+1 - min_y)

    # print("    ", end='')
    # for x in range(min_x, max_x+1):
    #     print(abs(x), end='')
    # print()
    # for y in range(max_y, min_y -1,-1):
    #     print(f"{y:3} ", end="")
    #     for x in range(min_x, max_x+1):
    #         if Point(x, y) in elf_positions:
    #             print("#", end="")
    #         else:
    #             print(".", end="")
    #     print()
    # print()

    return total_tiles - len(elf_positions)


def part2(problem_input: Iterable[str]) -> int:
    """Solution to part 2.

    >>> part2(sample_input)
    20
    """
    elf_positions: set[Point] = set()
    y = 0
    for row in problem_input:
        for x in range(len(row)):
            if row[x] == "#":
                elf_positions.add(Point(x, y))
        y -= 1

    directions = [Point(0, 1), Point(0, -1), Point(-1, 0), Point(1, 0)]
    round = 0
    while True:
        round += 1

        proposed_moves: dict[Point, Point] = {}
        for e in elf_positions:
            if (
                set(
                    [
                        Point(e.x - 1, e.y + 1),
                        Point(e.x, e.y + 1),
                        Point(e.x + 1, e.y + 1),
                        Point(e.x - 1, e.y),
                        Point(e.x + 1, e.y),
                        Point(e.x - 1, e.y - 1),
                        Point(e.x, e.y - 1),
                        Point(e.x + 1, e.y - 1),
                    ]
                )
                & elf_positions
                == set()
            ):
                continue
            for d in directions:
                if d.x == 0:
                    to_examine = set(Point(e.x + dx, e.y + d.y) for dx in [-1, 0, 1])
                    if elf_positions & to_examine == set():
                        proposed_moves[e] = Point(e.x + d.x, e.y + d.y)
                        break
                else:
                    to_examine = set(Point(e.x + d.x, e.y + dy) for dy in [-1, 0, 1])
                    if elf_positions & to_examine == set():
                        proposed_moves[e] = Point(e.x + d.x, e.y + d.y)
                        break
        new_positions: set[Point] = set()
        for e in elf_positions:
            if (
                e in proposed_moves
                and len(
                    [
                        dest
                        for dest in proposed_moves.values()
                        if dest == proposed_moves[e]
                    ]
                )
                == 1
            ):
                new_positions.add(proposed_moves[e])
            else:
                new_positions.add(e)
        if elf_positions == new_positions:
            break
        else:
            elf_positions = new_positions
            directions = directions[1:] + [directions[0]]

    return round


def solve(func: Callable[[Iterable[str]], int]) -> None:
    with open("problem_input/day23.txt") as f:
        print(func(f))


if __name__ == "__main__":
    sample_input = """
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
""".strip().splitlines()

    doctest.testmod(verbose=True)
    solve(part1)
    solve(part2)
