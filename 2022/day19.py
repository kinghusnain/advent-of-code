"""Advent of Code 2022, Day 19."""

import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from math import prod


@dataclass(frozen=True, eq=True)
class RobotCost:
    ore: int
    clay: int
    obsdian: int


@dataclass(frozen=True, eq=True)
class EconomicState:
    ore: int
    clay: int
    obsdian: int
    geodes: int
    ore_robots: int
    clay_robots: int
    obsdian_robots: int
    geode_robots: int


def part1(problem_input: Iterable[str]) -> int:
    """Solution to part 1.

    >>> part1(sample_input)
    33
    """
    blueprints: dict[int, tuple[RobotCost, RobotCost, RobotCost, RobotCost]] = {}
    for s in problem_input:
        num = re.search(r"Blueprint (\d+):", s)[1]  # type: ignore
        r_r = re.search(r"Each ore robot costs (\d+) ore.", s)[1]  # type: ignore
        c_r = re.search(r"Each clay robot costs (\d+) ore.", s)[1]  # type: ignore
        _, b_r, b_c = re.search(r"Each obsidian robot costs (\d+) ore and (\d+) clay.", s)  # type: ignore
        _, g_r, g_b = re.search(r"Each geode robot costs (\d+) ore and (\d+) obsidian.", s)  # type: ignore
        blueprints[int(num)] = (
            RobotCost(int(r_r), 0, 0),
            RobotCost(int(c_r), 0, 0),
            RobotCost(int(b_r), int(b_c), 0),
            RobotCost(int(g_r), 0, int(g_b)),
        )

    def max_geodes_harvested(blueprint: int, time: int) -> int:
        orebot_cost, claybot_cost, obsidianbot_cost, geodebot_cost = blueprints[
            blueprint
        ]
        initial_state = EconomicState(0, 0, 0, 0, 1, 0, 0, 0)
        end_states = set([initial_state])
        for t in range(time):
            print(f"{blueprint} {t}..")
            future_states: set[EconomicState] = set()
            for s in end_states:
                future_states.add(
                    EconomicState(
                        ore=s.ore + s.ore_robots,
                        clay=s.clay + s.clay_robots,
                        obsdian=s.obsdian + s.obsdian_robots,
                        geodes=s.geodes + s.geode_robots,
                        ore_robots=s.ore_robots,
                        clay_robots=s.clay_robots,
                        obsdian_robots=s.obsdian_robots,
                        geode_robots=s.geode_robots,
                    )
                )
                if (
                    geodebot_cost.ore <= s.ore
                    and geodebot_cost.clay <= s.clay
                    and geodebot_cost.obsdian <= s.obsdian
                ):
                    future_states.add(
                        EconomicState(
                            ore=s.ore - geodebot_cost.ore + s.ore_robots,
                            clay=s.clay - geodebot_cost.clay + s.clay_robots,
                            obsdian=s.obsdian
                            - geodebot_cost.obsdian
                            + s.obsdian_robots,
                            geodes=s.geodes + s.geode_robots,
                            ore_robots=s.ore_robots,
                            clay_robots=s.clay_robots,
                            obsdian_robots=s.obsdian_robots,
                            geode_robots=s.geode_robots + 1,
                        )
                    )
                if (
                    obsidianbot_cost.ore <= s.ore
                    and obsidianbot_cost.clay <= s.clay
                    and obsidianbot_cost.obsdian <= s.obsdian
                ):
                    future_states.add(
                        EconomicState(
                            ore=s.ore - obsidianbot_cost.ore + s.ore_robots,
                            clay=s.clay - obsidianbot_cost.clay + s.clay_robots,
                            obsdian=s.obsdian
                            - obsidianbot_cost.obsdian
                            + s.obsdian_robots,
                            geodes=s.geodes + s.geode_robots,
                            ore_robots=s.ore_robots,
                            clay_robots=s.clay_robots,
                            obsdian_robots=s.obsdian_robots + 1,
                            geode_robots=s.geode_robots,
                        )
                    )
                if (
                    claybot_cost.ore <= s.ore
                    and claybot_cost.clay <= s.clay
                    and claybot_cost.obsdian <= s.obsdian
                ):
                    future_states.add(
                        EconomicState(
                            ore=s.ore - claybot_cost.ore + s.ore_robots,
                            clay=s.clay - claybot_cost.clay + s.clay_robots,
                            obsdian=s.obsdian - claybot_cost.obsdian + s.obsdian_robots,
                            geodes=s.geodes + s.geode_robots,
                            ore_robots=s.ore_robots,
                            clay_robots=s.clay_robots + 1,
                            obsdian_robots=s.obsdian_robots,
                            geode_robots=s.geode_robots,
                        )
                    )
                if (
                    orebot_cost.ore <= s.ore
                    and orebot_cost.clay <= s.clay
                    and orebot_cost.obsdian <= s.obsdian
                ):
                    future_states.add(
                        EconomicState(
                            ore=s.ore - orebot_cost.ore + s.ore_robots,
                            clay=s.clay - orebot_cost.clay + s.clay_robots,
                            obsdian=s.obsdian - orebot_cost.obsdian + s.obsdian_robots,
                            geodes=s.geodes + s.geode_robots,
                            ore_robots=s.ore_robots + 1,
                            clay_robots=s.clay_robots,
                            obsdian_robots=s.obsdian_robots,
                            geode_robots=s.geode_robots,
                        )
                    )
            end_states = future_states
            if t > 20:
                high_score = max(s.geodes for s in end_states)
                if high_score > 0:
                    end_states = set(s for s in end_states if s.geodes > high_score * 0.67)
        return max(s.geodes for s in end_states)

    return sum(n * max_geodes_harvested(n, 24) for n in blueprints.keys())


def part2(problem_input: Iterable[str]) -> int:
    """Solution to part 2."""

    blueprints: dict[int, tuple[RobotCost, RobotCost, RobotCost, RobotCost]] = {}
    for s in problem_input:
        num = re.search(r"Blueprint (\d+):", s)[1]  # type: ignore
        r_r = re.search(r"Each ore robot costs (\d+) ore.", s)[1]  # type: ignore
        c_r = re.search(r"Each clay robot costs (\d+) ore.", s)[1]  # type: ignore
        _, b_r, b_c = re.search(r"Each obsidian robot costs (\d+) ore and (\d+) clay.", s)  # type: ignore
        _, g_r, g_b = re.search(r"Each geode robot costs (\d+) ore and (\d+) obsidian.", s)  # type: ignore
        blueprints[int(num)] = (
            RobotCost(int(r_r), 0, 0),
            RobotCost(int(c_r), 0, 0),
            RobotCost(int(b_r), int(b_c), 0),
            RobotCost(int(g_r), 0, int(g_b)),
        )

    def max_geodes_harvested(blueprint: int, time: int) -> int:
        orebot_cost, claybot_cost, obsidianbot_cost, geodebot_cost = blueprints[
            blueprint
        ]
        initial_state = EconomicState(0, 0, 0, 0, 1, 0, 0, 0)
        end_states = set([initial_state])
        for t in range(time):
            print(f"{blueprint} {t}..")
            future_states: set[EconomicState] = set()
            for s in end_states:
                future_states.add(
                    EconomicState(
                        ore=s.ore + s.ore_robots,
                        clay=s.clay + s.clay_robots,
                        obsdian=s.obsdian + s.obsdian_robots,
                        geodes=s.geodes + s.geode_robots,
                        ore_robots=s.ore_robots,
                        clay_robots=s.clay_robots,
                        obsdian_robots=s.obsdian_robots,
                        geode_robots=s.geode_robots,
                    )
                )
                if (
                    geodebot_cost.ore <= s.ore
                    and geodebot_cost.clay <= s.clay
                    and geodebot_cost.obsdian <= s.obsdian
                ):
                    future_states.add(
                        EconomicState(
                            ore=s.ore - geodebot_cost.ore + s.ore_robots,
                            clay=s.clay - geodebot_cost.clay + s.clay_robots,
                            obsdian=s.obsdian
                            - geodebot_cost.obsdian
                            + s.obsdian_robots,
                            geodes=s.geodes + s.geode_robots,
                            ore_robots=s.ore_robots,
                            clay_robots=s.clay_robots,
                            obsdian_robots=s.obsdian_robots,
                            geode_robots=s.geode_robots + 1,
                        )
                    )
                if (
                    obsidianbot_cost.ore <= s.ore
                    and obsidianbot_cost.clay <= s.clay
                    and obsidianbot_cost.obsdian <= s.obsdian
                ):
                    future_states.add(
                        EconomicState(
                            ore=s.ore - obsidianbot_cost.ore + s.ore_robots,
                            clay=s.clay - obsidianbot_cost.clay + s.clay_robots,
                            obsdian=s.obsdian
                            - obsidianbot_cost.obsdian
                            + s.obsdian_robots,
                            geodes=s.geodes + s.geode_robots,
                            ore_robots=s.ore_robots,
                            clay_robots=s.clay_robots,
                            obsdian_robots=s.obsdian_robots + 1,
                            geode_robots=s.geode_robots,
                        )
                    )
                if (
                    claybot_cost.ore <= s.ore
                    and claybot_cost.clay <= s.clay
                    and claybot_cost.obsdian <= s.obsdian
                ):
                    future_states.add(
                        EconomicState(
                            ore=s.ore - claybot_cost.ore + s.ore_robots,
                            clay=s.clay - claybot_cost.clay + s.clay_robots,
                            obsdian=s.obsdian - claybot_cost.obsdian + s.obsdian_robots,
                            geodes=s.geodes + s.geode_robots,
                            ore_robots=s.ore_robots,
                            clay_robots=s.clay_robots + 1,
                            obsdian_robots=s.obsdian_robots,
                            geode_robots=s.geode_robots,
                        )
                    )
                if (
                    orebot_cost.ore <= s.ore
                    and orebot_cost.clay <= s.clay
                    and orebot_cost.obsdian <= s.obsdian
                ):
                    future_states.add(
                        EconomicState(
                            ore=s.ore - orebot_cost.ore + s.ore_robots,
                            clay=s.clay - orebot_cost.clay + s.clay_robots,
                            obsdian=s.obsdian - orebot_cost.obsdian + s.obsdian_robots,
                            geodes=s.geodes + s.geode_robots,
                            ore_robots=s.ore_robots + 1,
                            clay_robots=s.clay_robots,
                            obsdian_robots=s.obsdian_robots,
                            geode_robots=s.geode_robots,
                        )
                    )
            end_states = future_states
            if t >= 25:
                high_score = max(s.geodes for s in end_states)
                if high_score > 0:
                    end_states = set(s for s in end_states if s.geodes > high_score * 0.67)
        g = max(s.geodes for s in end_states)
        print(f"{blueprint} >>>{g}<<<")
        return g

    return prod(max_geodes_harvested(n, 32) for n in [1,2,3])


def solve(func: Callable[[Iterable[str]], int]) -> None:
    with open("problem_input/day19.txt") as f:
        print(func(f))


if __name__ == "__main__":
    sample_input = """
Blueprint 1:
  Each ore robot costs 4 ore.
  Each clay robot costs 2 ore.
  Each obsidian robot costs 3 ore and 14 clay.
  Each geode robot costs 2 ore and 7 obsidian.

Blueprint 2:
  Each ore robot costs 2 ore.
  Each clay robot costs 3 ore.
  Each obsidian robot costs 3 ore and 8 clay.
  Each geode robot costs 3 ore and 12 obsidian.
""".split("\n\n")

    # print(part1(sample_input))
    # print(part2(sample_input))
    # solve(part1)
    solve(part2)
