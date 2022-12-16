"""Advent of Code 2022, Day 16."""

import doctest
import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass


def part1(problem_input: Iterable[str]) -> int:
    """Solution to part 1.

    >>> part1(sample_input)
    1651
    """
    tunnel_map: dict[str, list[str]] = {}
    flow_rates: dict[str, int] = {}
    for line in problem_input:
        m = re.match(
            r"Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.+)", line
        )
        if m:
            valve, rate, exits = m.groups()
            tunnel_map[valve] = [e.strip() for e in exits.split(",")]
            flow_rates[valve] = int(rate)

    @dataclass(eq=True, frozen=True)
    class ValveState:
        current_valve: str
        open_valves: frozenset[str]
        total_pressure_released: int
        total_flow_rate: int

    end_states = set([ValveState("AA", frozenset(), 0, 0)])
    for t in range(30):
        future_states: set[ValveState] = set()
        for s in end_states:
            # Open an unopened valve if it adds any flow.
            if s.current_valve not in s.open_valves and flow_rates[s.current_valve] > 0:
                future_states.add(
                    ValveState(
                        s.current_valve,
                        s.open_valves.union(set([s.current_valve])),
                        s.total_pressure_released + s.total_flow_rate,
                        s.total_flow_rate + flow_rates[s.current_valve],
                    )
                )
            # If all useful valves are open, do nothing.
            unopened = [
                v
                for v in tunnel_map.keys()
                if flow_rates[v] > 0 and v not in s.open_valves
            ]
            if len(unopened) == 0:
                future_states.add(
                    ValveState(
                        s.current_valve,
                        s.open_valves,
                        s.total_pressure_released + s.total_flow_rate,
                        s.total_flow_rate,
                    )
                )
            # Move through a tunnel.
            else:
                for exit in tunnel_map[s.current_valve]:
                    future_states.add(
                        ValveState(
                            exit,
                            s.open_valves,
                            s.total_pressure_released + s.total_flow_rate,
                            s.total_flow_rate,
                        )
                    )
        # Hack: in later rounds, purge hopeless timelines
        if t > 20:
            leader = max(s.total_pressure_released for s in future_states)
            future_states = set(
                [s for s in future_states if s.total_pressure_released > leader // 2]
            )
        end_states = future_states

    return max(s.total_pressure_released for s in end_states)


def part2(problem_input: Iterable[str]) -> int:
    """Solution to part 2.

    >>> part2(sample_input)
    1707
    """
    tunnel_map: dict[str, list[str]] = {}
    flow_rates: dict[str, int] = {}
    for line in problem_input:
        m = re.match(
            r"Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.+)", line
        )
        if m:
            valve, rate, exits = m.groups()
            tunnel_map[valve] = [e.strip() for e in exits.split(",")]
            flow_rates[valve] = int(rate)

    @dataclass(eq=True, frozen=True)
    class ValveState:
        my_location: str
        elephant_location: str
        open_valves: frozenset[str]
        total_pressure_released: int
        total_flow_rate: int

    end_states = set([ValveState("AA", "AA", frozenset(), 0, 0)])
    for t in range(26):
        # Release pressure
        end_states = set(
            ValveState(
                s.my_location,
                s.elephant_location,
                s.open_valves,
                s.total_pressure_released + s.total_flow_rate,
                s.total_flow_rate,
            )
            for s in end_states
        )

        states_after_my_move: set[ValveState] = set()
        # My moves
        for s in end_states:
            # Open an unopened valve if it adds any flow.
            if s.my_location not in s.open_valves and flow_rates[s.my_location] > 0:
                states_after_my_move.add(
                    ValveState(
                        s.my_location,
                        s.elephant_location,
                        s.open_valves.union(set([s.my_location])),
                        s.total_pressure_released,
                        s.total_flow_rate + flow_rates[s.my_location],
                    )
                )
            # If all useful valves are open, do nothing.
            unopened = [
                v
                for v in tunnel_map.keys()
                if flow_rates[v] > 0 and v not in s.open_valves
            ]
            if len(unopened) == 0:
                states_after_my_move.add(s)
            # Move through a tunnel.
            else:
                for exit in tunnel_map[s.my_location]:
                    states_after_my_move.add(
                        ValveState(
                            exit,
                            s.elephant_location,
                            s.open_valves,
                            s.total_pressure_released,
                            s.total_flow_rate,
                        )
                    )

        # Elephant's moves
        states_after_elephant_move: set[ValveState] = set()
        for s in states_after_my_move:
            # Elephant opens an unopened valve if it adds any flow.
            if (
                s.elephant_location not in s.open_valves
                and flow_rates[s.elephant_location] > 0
            ):
                states_after_elephant_move.add(
                    ValveState(
                        s.my_location,
                        s.elephant_location,
                        s.open_valves.union(set([s.elephant_location])),
                        s.total_pressure_released,
                        s.total_flow_rate + flow_rates[s.elephant_location],
                    )
                )
            # If all useful valves are open, do nothing.
            unopened = [
                v
                for v in tunnel_map.keys()
                if flow_rates[v] > 0 and v not in s.open_valves
            ]
            if len(unopened) == 0:
                states_after_elephant_move.add(s)
            # Elephant moves through a tunnel.
            else:
                for exit in tunnel_map[s.elephant_location]:
                    states_after_elephant_move.add(
                        ValveState(
                            s.my_location,
                            exit,
                            s.open_valves,
                            s.total_pressure_released,
                            s.total_flow_rate,
                        )
                    )

        # Hack: in later rounds, purge hopeless timelines
        if t > 10:
            leader = max(s.total_pressure_released for s in states_after_elephant_move)
            states_after_elephant_move = set(
                s
                for s in states_after_elephant_move
                if s.total_pressure_released > leader * 0.9
            )
        end_states = states_after_elephant_move

    return max(s.total_pressure_released for s in end_states)


def solve(func: Callable[[Iterable[str]], int]) -> None:
    with open("problem_input/day16.txt") as f:
        print(func(f))


if __name__ == "__main__":
    sample_input = """
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
""".strip().splitlines()

    doctest.testmod(verbose=True)
    solve(part1)
    solve(part2)
