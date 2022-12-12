"""Advent of Code 2022, Day 11."""

import doctest
from collections.abc import Callable, Iterable
from math import sqrt


def part1(problem_input: Iterable[str]) -> int:
    """Solution to part 1.

    >>> part1(sample_input)
    10605
    """
    monkeys = [Monkey(s) for s in problem_input]
    inspections = [0 for _ in range(len(monkeys))]
    for _ in range(20):
        for i in range(len(monkeys)):
            for item in monkeys[i].items:
                inspections[i] += 1
                worry = monkeys[i].op(item)
                worry //= 3
                if worry % monkeys[i].test_divisor == 0:
                    monkeys[monkeys[i].true_target].items.append(worry)
                else:
                    monkeys[monkeys[i].false_target].items.append(worry)
            monkeys[i].items = []
    inspections.sort(reverse=True)
    return inspections[0] * inspections[1]


def part2(problem_input: Iterable[str]) -> int:
    """Solution to part 2.

    >>> part2(sample_input)
    0
    """
    return 0


class Monkey:
    def __init__(self, monkey_notes: str) -> None:
        notes = [s.strip() for s in monkey_notes.splitlines()]

        self.items: list[int] = [
            int(n) for n in notes[1].lstrip("Starting items: ").split(",")
        ]
        self.test_divisor: int = int(notes[3][-2:])
        self.true_target: int = int(notes[4][-1])
        self.false_target: int = int(notes[5][-1])

        if notes[2] == "Operation: new = old * old":
            self.op: Callable[[int], int] = lambda n: n * n
        elif notes[2].startswith("Operation: new = old *"):
            self.op: Callable[[int], int] = lambda n: n * int(notes[2][-2:])
        elif notes[2].startswith("Operation: new = old +"):
            self.op: Callable[[int], int] = lambda n: n + int(notes[2][-2:])
        else:
            raise ValueError


def solve(func: Callable[[Iterable[str]], int]) -> None:
    with open("problem_input/day11.txt") as f:
        print(func(f.read().split("\n\n")))


if __name__ == "__main__":
    sample_input = """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
""".strip().split(
        "\n\n"
    )

    doctest.testmod(verbose=True)
    solve(part1)
    solve(part2)
