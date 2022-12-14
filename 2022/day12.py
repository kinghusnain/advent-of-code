"""Advent of Code 2022, Day 12."""

import doctest
from collections.abc import Callable, Iterable


def part1(problem_input: Iterable[str]) -> int:
    """Solution to part 1.

    >>> part1(sample_input)
    31
    """
    strings = list(problem_input)
    start = end = (-1, -1)
    for y in range(len(strings)):
        for x in range(len(strings[0])):
            if strings[y][x] == "S":
                start = (x, y)
            if strings[y][x] == "E":
                end = (x, y)
        strings[y] = strings[y].translate({ord("S"): "a", ord("E"): "z"})
    height_map: list[list[int]] = [[ord(c) - ord("a") for c in r] for r in strings]

    path_ends: set[tuple[int, int]] = set([start])
    is_path_found = False
    steps_explored = 0
    while not is_path_found:
        for p in path_ends.copy():
            x, y = p
            path_ends.remove(p)
            exits = [
                (u, v)
                for u, v in [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
                if u in range(0, len(height_map[0]))
                and v in range(0, len(height_map))
                and height_map[v][u] <= height_map[y][x] + 1
            ]
            for e in exits:
                path_ends.add(e)
                if e == end:
                    is_path_found = True
        steps_explored += 1
    return steps_explored


def part2(problem_input: Iterable[str]) -> int:
    """Solution to part 2.

    >>> part2(sample_input)
    29
    """
    strings = list(problem_input)
    end = (-1, -1)
    low_points = []
    for y in range(len(strings)):
        for x in range(len(strings[0])):
            if strings[y][x] in ["S", "a"]:
                low_points.append((x, y))
            if strings[y][x] == "E":
                end = (x, y)
        strings[y] = strings[y].translate({ord("S"): "a", ord("E"): "z"})
    height_map: list[list[int]] = [[ord(c) - ord("a") for c in r] for r in strings]

    path_ends: set[tuple[int, int]] = set(low_points)
    is_path_found = False
    steps_explored = 0
    while not is_path_found:
        for p in path_ends.copy():
            x, y = p
            path_ends.remove(p)
            exits = [
                (u, v)
                for u, v in [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
                if u in range(0, len(height_map[0]))
                and v in range(0, len(height_map))
                and height_map[v][u] <= height_map[y][x] + 1
            ]
            for e in exits:
                path_ends.add(e)
                if e == end:
                    is_path_found = True
        steps_explored += 1
    return steps_explored


def solve(func: Callable[[Iterable[str]], int]) -> None:
    with open("problem_input/day12.txt") as f:
        print(func(f))


if __name__ == "__main__":
    sample_input = """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
""".strip().splitlines()

    doctest.testmod(verbose=True)
    solve(part1)
    solve(part2)
