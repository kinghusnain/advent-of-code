"""Advent of Code 2022, Day 8."""

import doctest
from collections.abc import Callable, Iterable


def part1(problem_input: Iterable[str]) -> int:
    """Solution to part 1.

    >>> part1(sample_input)
    21
    """
    height_map = [[int(n) for n in s.strip()] for s in problem_input]
    visible: set[tuple[int, int]] = set()

    # From the West
    for y in range(0, len(height_map)):
        visible.add((0, y))
        for x in range(1, len(height_map[0])):
            if height_map[y][x] > max(height_map[y][:x]):
                visible.add((x, y))

    # From the East
    for y in range(0, len(height_map)):
        visible.add((len(height_map[0]) - 1, y))
        for x in range(len(height_map[0]) - 2, -1, -1):
            if height_map[y][x] > max(height_map[y][x + 1 :]):
                visible.add((x, y))

    # From the North
    for x in range(0, len(height_map[0])):
        visible.add((x, 0))
        for y in range(1, len(height_map)):
            if height_map[y][x] > max(c[x] for c in height_map[:y]):
                visible.add((x, y))

    # From the South
    for x in range(0, len(height_map[0])):
        visible.add((x, len(height_map) - 1))
        for y in range(len(height_map) - 2, -1, -1):
            if height_map[y][x] > max(c[x] for c in height_map[y + 1 :]):
                visible.add((x, y))

    return len(visible)


def part2(problem_input: Iterable[str]) -> int:
    """Solution to part 2.

    >>> part2(sample_input)
    8
    """
    height_map = [[int(n) for n in s.strip()] for s in problem_input]

    def view_north(x: int, y: int) -> int:
        if y == 0:
            return 0
        v = 0
        for yy in range(y - 1, -1, -1):
            v += 1
            if height_map[yy][x] >= height_map[y][x]:
                break
        return v

    def view_south(x: int, y: int) -> int:
        if y == len(height_map) - 1:
            return 0
        v = 0
        for yy in range(y + 1, len(height_map)):
            v += 1
            if height_map[yy][x] >= height_map[y][x]:
                break
        return v

    def view_west(x: int, y: int) -> int:
        if x == 0:
            return 0
        v = 0
        for xx in range(x - 1, -1, -1):
            v += 1
            if height_map[y][xx] >= height_map[y][x]:
                break
        return v

    def view_east(x: int, y: int) -> int:
        if x == len(height_map[0]):
            return 0
        v = 0
        for xx in range(x + 1, len(height_map[0])):
            v += 1
            if height_map[y][xx] >= height_map[y][x]:
                break
        return v

    return max(
        view_north(x, y) * view_south(x, y) * view_west(x, y) * view_east(x, y)
        for x in range(len(height_map[0]))
        for y in range(len(height_map))
    )


def solve(func: Callable[[Iterable[str]], int]) -> None:
    with open("problem_input/day08.txt") as f:
        print(func(f))


if __name__ == "__main__":
    sample_input = """
30373
25512
65332
33549
35390
""".strip().splitlines()

    doctest.testmod(verbose=True)
    solve(part1)
    solve(part2)
