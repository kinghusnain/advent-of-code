"""Advent of Code 2022, Day 13."""

import doctest
import functools
from collections.abc import Callable
from typing import Optional, Union


def part1(problem_input: str) -> int:
    """Solution to part 1.

    >>> part1(sample_input)
    13
    """
    pairs: list[list[Packet]] = [
        [eval(s) for s in ps.splitlines()] for ps in problem_input.split("\n\n")
    ]
    return sum(pairs.index([l, r]) + 1 for l, r in pairs if lt(l, r))


def part2(problem_input: str) -> int:
    """Solution to part 2.

    >>> part2(sample_input)
    140
    """
    packets: list[Packet] = [
        eval(s) for s in problem_input.splitlines() if s.strip() != ""
    ]
    packets.append([[2]])
    packets.append([[6]])
    packets.sort(key=functools.cmp_to_key(cmp))
    packets.insert(0, [])
    return packets.index([[2]]) * packets.index([[6]])


Packet = Union[int, list["Packet"]]


def lt(left: Packet, right: Packet) -> Optional[bool]:
    """
    >>> lt([9], [[8,7,6]])
    False
    >>> lt([[1],[2,3,4]], [[1],4])
    True
    """
    if type(left) == int and type(right) == int:
        if left < right:  # type: ignore
            return True
        elif left > right:  # type: ignore
            return False
        else:
            return None
    elif type(left) == list and type(right) == list:
        l: list[Packet] = left  # type: ignore
        r: list[Packet] = right  # type: ignore
        for i in range(len(l)):
            if i not in range(len(r)):
                return False
            is_less = lt(l[i], r[i])
            if is_less is not None:
                return is_less
        if len(l) < len(r):
            return True
        else:
            return None
    elif type(left) == int and type(right) == list:
        return lt([left], right)
    elif type(left) == list and type(right) == int:
        return lt(left, [right])
    else:
        raise ValueError


def cmp(left: Packet, right: Packet) -> int:
    is_less = lt(left, right)
    if is_less == True:
        return -1
    elif is_less == False:
        return 1
    else:
        return 0


def solve(func: Callable[[str], int]) -> None:
    with open("problem_input/day13.txt") as f:
        print(func(f.read()))


if __name__ == "__main__":
    sample_input = """
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
""".strip()

    doctest.testmod(verbose=True)
    solve(part1)
    solve(part2)
