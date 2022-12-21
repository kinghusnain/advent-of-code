"""Advent of Code 2022, Day 21."""

import doctest
import operator
from collections.abc import Callable, Iterable
from typing import Optional


def part1(problem_input: Iterable[str]) -> int:
    """Solution to part 1.

    >>> part1(sample_input)
    152
    """
    Monkey.directory = {}
    defs = {k: v for k, v in [s.split(": ") for s in problem_input]}
    root = Monkey("root", defs["root"], None)
    unloaded_dependencies = [root]
    solved: list[Monkey] = []
    while len(unloaded_dependencies) > 0:
        node = unloaded_dependencies.pop()
        for id in [node.left_dependency, node.right_dependency]:
            if id is None:
                continue
            assert id not in Monkey.directory
            dep = Monkey(id, defs[id], node)
            if Monkey.directory[id].value is None:
                unloaded_dependencies.append(dep)
            else:
                solved.append(dep)

    while root.value is None:
        for m in solved:
            parent = m.dependency_of
            if (
                parent is not None
                and parent.value is None
                and parent.is_solvable()
            ):
                parent.solve()
                solved.append(parent)

    return root.value


def part2(problem_input: Iterable[str]) -> int:
    """Solution to part 2.

    >>> part2(sample_input)
    0
    """
    return 0


class Monkey:
    op_fn = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.floordiv,
    }
    directory: dict[str, "Monkey"] = {}

    def __init__(
        self, id: str, def_str: str, dependency_of: Optional["Monkey"]
    ) -> None:
        Monkey.directory[id] = self
        self.id = id
        self.value: Optional[int]
        self.operation: Optional[Callable]
        self.left_dependency: Optional[str]
        self.right_dependency: Optional[str]
        self.dependency_of: Optional[Monkey] = dependency_of
        try:
            self.value = int(def_str)
            self.operation = None
            self.left_dependency = None
            self.right_dependency = None
        except ValueError:
            left, op, right = def_str.split()
            self.value = None
            self.operation = Monkey.op_fn[op.strip()]
            self.left_dependency = left.strip()
            self.right_dependency = right.strip()

    def is_solvable(self) -> bool:
        return (
            self.operation is not None
            and self.left_dependency in Monkey.directory
            and Monkey.directory[self.left_dependency].value is not None
            and self.right_dependency in Monkey.directory
            and Monkey.directory[self.right_dependency].value is not None
        )

    def solve(self) -> None:
        if (
            self.operation is not None
            and self.left_dependency in Monkey.directory
            and Monkey.directory[self.left_dependency].value is not None
            and self.right_dependency in Monkey.directory
            and Monkey.directory[self.right_dependency].value is not None
        ):
            self.value = self.operation(
                Monkey.directory[self.left_dependency].value,
                Monkey.directory[self.right_dependency].value,
            )


def solve(func: Callable[[Iterable[str]], int]) -> None:
    with open("problem_input/day21.txt") as f:
        print(func(f))


if __name__ == "__main__":
    sample_input = """
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
""".strip().splitlines()

    doctest.testmod(verbose=True)
    solve(part1)
    # solve(part2)
