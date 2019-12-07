# Lint as: python3
"""Advent of Code, Day 6 -- Orbit map.

>>> orbit_map = OrbitMap2()
>>> orbit_map.add_direct_orbit('COM', 'B')
>>> orbit_map.add_direct_orbit('B', 'C')
>>> orbit_map.add_direct_orbit('C', 'D')
>>> orbit_map.add_direct_orbit('D', 'E')
>>> orbit_map.add_direct_orbit('E', 'F')
>>> orbit_map.add_direct_orbit('B', 'G')
>>> orbit_map.add_direct_orbit('G', 'H')
>>> orbit_map.add_direct_orbit('D', 'I')
>>> orbit_map.add_direct_orbit('E', 'J')
>>> orbit_map.add_direct_orbit('J', 'K')
>>> orbit_map.add_direct_orbit('K', 'L')
>>> orbit_map.total_orbits()
42

>>> orbit_map.add_direct_orbit('K', 'YOU')
>>> orbit_map.add_direct_orbit('I', 'SAN')
>>> orbit_map.path_to_com('YOU')
['K', 'J', 'E', 'D', 'C', 'B', 'COM']
>>> orbit_map.path_to_com('SAN')
['I', 'D', 'C', 'B', 'COM']
>>> orbit_map.path('YOU', 'SAN')
['J', 'E', 'D', 'I']

>>> orbit_map = OrbitMap2()
>>> orbit_map.add_direct_orbit('COM', 'A')
>>> orbit_map.add_direct_orbit('COM', 'B')
>>> orbit_map.add_direct_orbit('B', 'C')
>>> orbit_map.path('A', 'C')  # A > COM > B > C
['B']

>>> orbit_map = OrbitMap2()
>>> orbit_map.add_direct_orbit('B', 'A')
>>> orbit_map.add_direct_orbit('COM', 'B')
>>> orbit_map.add_direct_orbit('COM', 'C')
>>> orbit_map.path('A', 'C')  # A > B > COM > C
['COM']

>>> orbit_map = OrbitMap2()
>>> orbit_map.add_direct_orbit('A', '-A')
>>> orbit_map.add_direct_orbit('B', 'A')
>>> orbit_map.add_direct_orbit('COM', 'B')
>>> orbit_map.add_direct_orbit('COM', 'C')
>>> orbit_map.path('-A', 'C')  # -A > A > B > COM > C
['B', 'COM']

>>> orbit_map = OrbitMap2()
>>> orbit_map.add_direct_orbit('COM', 'A')
>>> orbit_map.add_direct_orbit('A', 'B')
>>> orbit_map.add_direct_orbit('A', 'B2')
>>> orbit_map.add_direct_orbit('B', 'C')
>>> orbit_map.add_direct_orbit('C', 'D')
>>> orbit_map.path('B2', 'D')  # B2 > A > B > C > D
['B', 'C']

>>> orbit_map = OrbitMap2()
>>> orbit_map.load('advent06_orbit_data.txt')
>>> len(orbit_map.map)
1234
"""


import doctest
import functools


class OrbitMap:
  """False start. Abandoned for OrbitMap2."""

  def __init__(self):
    self.map = {'COM': []}

  def add_direct_orbit(self, center, obj):
    if center in self.map:
      self.map[center].append(obj)
    else:
      self.map[center] = [obj]
    if obj not in self.map:
      self.map[obj] = []

  def num_orbits(self, obj='COM'):
    direct_orbits = len(self.map[obj])
    if direct_orbits == 0:
      return 0
    else:
      indirect_orbits = [self.num_orbits(obj=o) for o in self.map[obj]]
      return (direct_orbits
              + functools.reduce(lambda x, y: x + y, indirect_orbits))

  def total_orbits(self):
    all_orbits = [self.num_orbits(obj=o) for o in self.map.keys()]
    return functools.reduce(lambda x, y: x + y, all_orbits)

  def load(self, filename):
    for entry in open(filename):
      if len(entry.strip()) > 0:
        center, obj = entry.split(')', maxsplit=1)
        self.add_direct_orbit(center.strip(), obj.strip())


class OrbitMap2:

  def __init__(self):
    self.map = {'COM': None}

  def add_direct_orbit(self, center, obj):
    if obj in self.map:
      raise Exception
    self.map[obj] = center

  def num_orbits(self, obj):
    if obj == 'COM':
      return 0
    else:
      return 1 + self.num_orbits(self.map[obj])

  def total_orbits(self):
    all_orbits = [self.num_orbits(o) for o in self.map.keys()]
    return sum(all_orbits)

  def path_to_com(self, obj):
    if obj == 'COM':
      return []
    else:
      return [self.map[obj]] + self.path_to_com(self.map[obj])

  def path(self, obj, target):
    if obj == 'COM' or target == 'COM':
      raise Exception
    path_from_obj = self.path_to_com(obj)
    path_from_target = self.path_to_com(target)
    assert path_from_obj[-1] == path_from_target[-1]
    while (len(path_from_obj) > 1 and len(path_from_target) > 1
           and path_from_obj[-2] == path_from_target[-2]):
      path_from_obj = path_from_obj[:-1]
      path_from_target = path_from_target[:-1]
    path = path_from_obj[:-1] + list(reversed(path_from_target))
    assert path[0] == self.map[obj]
    return path[1:]

  def load(self, filename):
    for entry in open(filename):
      if len(entry.strip()) > 0:
        center, obj = entry.split(')', maxsplit=1)
        self.add_direct_orbit(center.strip(), obj.strip())


def solve_pt1():
  orbit_map = OrbitMap2()
  orbit_map.load('advent06_orbit_data.txt')
  orbits = orbit_map.total_orbits()
  print(orbits)


def solve_pt2():
  orbit_map = OrbitMap2()
  orbit_map.load('advent06_orbit_data.txt')
  xfers = len(orbit_map.path('YOU', 'SAN'))
  print(xfers)


if __name__ == "__main__":
  doctest.testmod()
  solve_pt1()
  solve_pt2()
