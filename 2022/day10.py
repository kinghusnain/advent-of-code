"""Advent of Code 2022, Day 10."""

import doctest
from collections.abc import Callable, Iterable


def part1(problem_input: Iterable[str]) -> int:
    """Solution to part 1.

    >>> part1(sample_input)
    13140
    """
    cycles = [
        c
        for p in [
            ["addx...", i] if i.startswith("addx") else [i] for i in problem_input
        ]
        for c in p
    ]

    def x(cycle):
        return 1 + sum(
            int(i.split()[1]) for i in cycles[: cycle - 1] if i.startswith("addx ")
        )

    return sum(x(cycle) * cycle for cycle in [20, 60, 100, 140, 180, 220])


def part2(problem_input: Iterable[str]) -> int:
    """Solution to part 2.

    >>> part2(sample_input)
    ##..##..##..##..##..##..##..##..##..##..
    ###...###...###...###...###...###...###.
    ####....####....####....####....####....
    #####.....#####.....#####.....#####.....
    ######......######......######......####
    #######.......#######.......#######.....
    0
    """
    cycles = [
        c
        for p in [
            ["addx...", i] if i.startswith("addx") else [i] for i in problem_input
        ]
        for c in p
    ]

    def x(cycle):
        return 1 + sum(
            int(i.split()[1]) for i in cycles[: cycle - 1] if i.startswith("addx ")
        )

    output = ""
    for cycle in range(1, 241):
        px = (cycle - 1) % 40
        sprite_pos = x(cycle)
        output += "#" if px in [sprite_pos - 1, sprite_pos, sprite_pos + 1] else "."
        if cycle % 40 == 0:
            output += "\n"
    print(output.strip())

    return 0


def solve(func: Callable[[Iterable[str]], int]) -> None:
    with open("problem_input/day10.txt") as f:
        print(func(f))


if __name__ == "__main__":
    sample_input = """
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
""".strip().splitlines()

    doctest.testmod(verbose=True)
    solve(part1)
    solve(part2)
