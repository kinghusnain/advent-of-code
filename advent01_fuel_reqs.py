# Lint as: python3
"""Advent of Code, Day 1 -- Calculates fuel requirements per rocket module.

>>> fuel_required(12)
2
>>> fuel_required(14)
2
>>> fuel_required(1969)
654
>>> fuel_required(100756)
33583
>>> fuel_required_improved(14)
2
>>> fuel_required_improved(1969)
966
>>> fuel_required_improved(100756)
50346
"""

import doctest
import math


def fuel_required(mass):
  return math.floor(mass / 3) - 2


def fuel_required_improved(mass):
  subtotal = math.floor(mass / 3) - 2
  if subtotal < 0:
    return 0
  else:
    return subtotal + fuel_required_improved(subtotal)


def main():
  total = 0
  total_improved = 0
  with open("advent01_input.txt") as f:
    for line in f:
      mass = int(line)
      total += fuel_required(mass)
      total_improved += fuel_required_improved(mass)
  print(total)
  print(total_improved)


if __name__ == "__main__":
  doctest.testmod()
  main()
