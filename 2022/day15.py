"""Advent of Code 2022, Day 15."""

import doctest
import re
from collections import namedtuple
from collections.abc import Callable, Iterable

Point = namedtuple("Point", ["x", "y"])


def part1(problem_input: Iterable[str], row_y: int) -> int:
    """Solution to part 1.

    >>> part1(sample_input, 10)
    26
    """
    sensor_beacons: dict[Point, tuple[Point, int]] = {
        Point(int(sx), int(sy)): (
            Point(int(bx), int(by)),
            distance(Point(int(sx), int(sy)), Point(int(bx), int(by))),
        )
        for sx, sy, bx, by in [
            re.match(
                r"Sensor at x=([0-9-]+), y=([0-9-]+): closest beacon is at x=([0-9-]+), y=([0-9-]+)",
                line,
            ).groups()  # type: ignore
            for line in problem_input
        ]
    }

    min_x = min(s.x - d for s, (_, d) in sensor_beacons.items())
    max_x = max(s.x + d for s, (_, d) in sensor_beacons.items())

    ruled_out: set[Point] = set()
    for x in range(min_x, max_x + 1):
        p = Point(x, row_y)
        for s, (b, d) in sensor_beacons.items():
            if distance(s, p) <= d and p != b:
                ruled_out.add(p)
                break
    return len(ruled_out)


def distance(a: Point, b: Point) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def solve(func: Callable[[Iterable[str], int], int], x: int) -> None:
    with open("problem_input/day15.txt") as f:
        print(func(f, x))


if __name__ == "__main__":
    sample_input = """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
""".strip().splitlines()

    doctest.testmod(verbose=True)
    solve(part1, 2000000)
    # solve(part2, 4000000)
