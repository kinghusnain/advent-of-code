"""Advent of Code 2022, Day 7."""

from dataclasses import dataclass
import doctest
from collections.abc import Callable, Generator, Iterable
from typing import Optional, Union


def part1(problem_input: Iterable[str]) -> int:
    """Solution to part 1.

    >>> part1(sample_input)
    95437
    """
    root = tree_from_log(problem_input)
    return sum(d.size() for d in root.walk_dirs() if d.size() <= 100000)


def part2(problem_input: Iterable[str]) -> int:
    """Solution to part 2.

    >>> part2(sample_input)
    24933642
    """
    root = tree_from_log(problem_input)
    free = 70000000 - root.size()
    needed = 30000000 - free
    dir_sizes = (d.size() for d in root.walk_dirs())
    return min(ds for ds in dir_sizes if ds >= needed)


@dataclass
class FileLike:
    name: str
    parent: Union["Directory", None]


@dataclass
class File(FileLike):
    size: int


class Directory(FileLike):
    def __init__(self, name: str, parent: "Directory"):
        self.name = name
        self.parent = parent
        self.contents: list[FileLike] = []
        self._size: Optional[int] = None

    def size(self) -> int:
        if self._size is None:
            direct_size = sum(f.size for f in self.contents if isinstance(f, File))
            indirect_size = sum(
                d.size() for d in self.contents if isinstance(d, Directory)
            )
            self._size = direct_size + indirect_size
        return self._size

    def walk_dirs(self) -> Generator["Directory", None, None]:
        yield self
        for d in [x for x in self.contents if isinstance(x, Directory)]:
            for sub in d.walk_dirs():
                yield sub


def tree_from_log(log: Iterable[str]) -> Directory:
    root = Directory(name="/", parent=None)
    pwd = root
    for line in log:
        line = line.strip()
        if line == "$ cd ..":
            pwd = pwd.parent
        elif line == "$ cd /":
            pwd = root
        elif line.startswith("$ cd "):
            dirname = line[len("$ cd ") :]
            matches = [
                x
                for x in pwd.contents
                if isinstance(x, Directory) and x.name == dirname
            ]
            if len(matches) == 0:
                pwd.contents.append(Directory(name=dirname, parent=pwd))
                pwd = pwd.contents[-1]
            else:
                pwd = matches[0]
        elif line[0].isdigit():
            size, filename = line.split()
            pwd.contents.append(File(name=filename, parent=pwd, size=int(size)))
        else:
            pass
    return root


def solve(func: Callable[[Iterable[str]], int]) -> None:
    with open("problem_input/day07.txt") as f:
        print(func(f))


if __name__ == "__main__":
    sample_input = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
""".strip().splitlines()

    doctest.testmod(verbose=True)
    solve(part1)
    solve(part2)
