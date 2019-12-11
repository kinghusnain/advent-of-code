# Lint as: python3
r"""Advent of Code, Day 10 -- Monitoring station.

>>> m = AsteroidMap('#.#\n...\n..#')
>>> for y in range(3):
...   for x in range(3):
...     print(m.asteroid_at(x, y))
True
False
True
False
False
False
False
False
True
>>> m = AsteroidMap('''
... .#..#
... .....
... #####
... ....#
... ...##
... ''')
>>> m.has_los((3,4), (1,0))
False
>>> m.has_los((3,4), (4,0))
True
>>> m.has_los((3,4), (1,2))
True
>>> len(m.asteroids_visible_from(3,4))
8
>>> m.has_los((0,2), (2,2))
False
>>> m.best_location()
(3, 4)
>>> m.sweep_from(3,4)
[(3, 2), (4, 0), (4, 2), (4, 3), (4, 4), (0, 2), (1, 2), (2, 2)]
"""


import doctest
import math


class AsteroidMap():

  def __init__(self, mapstring):
    self.data = []
    for line in mapstring.strip().split('\n'):
      self.data.append([c == '#' for c in line])

  def asteroid_at(self, x, y):
    return self.data[y][x]

  def has_los(self, a, b):
    if not self.asteroid_at(*a) or not self.asteroid_at(*b):
      raise Exception
    a_x, a_y = a
    b_x, b_y = b
    x_step = 1 if a_x < b_x else -1
    y_step = 1 if a_y < b_y else -1
    ab_slope = slope(a, b)
    usual_suspects = [(x, y)
                      for x in range(a_x, b_x + x_step, x_step)
                      for y in range(a_y, b_y + y_step, y_step)
                      if self.asteroid_at(x, y) and (x, y) != a and (x, y) != b]
    for x, y in usual_suspects:
      pb_slope = slope((x, y), b)
      if ab_slope == pb_slope:
        return False
    return True

  def asteroids_visible_from(self, x, y):
    return [(p_x, p_y)
            for p_x in range(len(self.data[0]))
            for p_y in range(len(self.data))
            if ((x, y) != (p_x, p_y)
                and self.asteroid_at(p_x, p_y)
                and self.has_los((x, y), (p_x, p_y)))]

  def best_location(self):
    location = None, None
    num_visible = 0
    asteroids = [(x, y)
                 for x in range(len(self.data[0]))
                 for y in range(len(self.data))
                 if self.asteroid_at(x, y)]
    for x, y in asteroids:
      n = len(self.asteroids_visible_from(x, y))
      if n > num_visible:
        location = x, y
        num_visible = n
    return location

  def sweep_from(self, origin_x, origin_y):
    def slope_float(p):
      delta_y, delta_x = slope((origin_x, origin_y), p)
      return delta_y / delta_x
    asteroids = self.asteroids_visible_from(origin_x, origin_y)
    north = [(x, y) for x, y in asteroids if x == origin_x and y < origin_y]
    assert len(north) <= 1
    east = list(sorted([(x, y) for x, y in asteroids if x > origin_x],
                       key=slope_float))
    south = [(x, y) for x, y in asteroids if x == origin_x and y > origin_y]
    assert len(south) <= 1
    west = list(sorted([(x, y) for x, y in asteroids if x < origin_x],
                       key=slope_float))
    return north + east + south + west

  def vaporize(self, x, y):
    self.data[y][x] = False


def slope(a, b):
  delta_x = a[0] - b[0]
  delta_y = a[1] - b[1]
  gcd = math.gcd(delta_x, delta_y)
  return delta_y // gcd, delta_x // gcd


def solve_pt1():
  m = AsteroidMap("""
##.##..#.####...#.#.####
##.###..##.#######..##..
..######.###.#.##.######
.#######.####.##.#.###.#
..#...##.#.....#####..##
#..###.#...#..###.#..#..
###..#.##.####.#..##..##
.##.##....###.#..#....#.
########..#####..#######
##..#..##.#..##.#.#.#..#
##.#.##.######.#####....
###.##...#.##...#.######
###...##.####..##..#####
##.#...#.#.....######.##
.#...####..####.##...##.
#.#########..###..#.####
#.##..###.#.######.#####
##..##.##...####.#...##.
###...###.##.####.#.##..
####.#.....###..#.####.#
##.####..##.#.##..##.#.#
#####..#...####..##..#.#
.##.##.##...###.##...###
..###.########.#.###..#.
""")
  best_location = m.best_location()
  num_visible = len(m.asteroids_visible_from(*best_location))
  print(best_location, num_visible)


def solve_pt2():
  m = AsteroidMap("""
##.##..#.####...#.#.####
##.###..##.#######..##..
..######.###.#.##.######
.#######.####.##.#.###.#
..#...##.#.....#####..##
#..###.#...#..###.#..#..
###..#.##.####.#..##..##
.##.##....###.#..#....#.
########..#####..#######
##..#..##.#..##.#.#.#..#
##.#.##.######.#####....
###.##...#.##...#.######
###...##.####..##..#####
##.#...#.#.....######.##
.#...####..####.##...##.
#.#########..###..#.####
#.##..###.#.######.#####
##..##.##...####.#...##.
###...###.##.####.#.##..
####.#.....###..#.####.#
##.####..##.#.##..##.#.#
#####..#...####..##..#.#
.##.##.##...###.##...###
..###.########.#.###..#.
""")
  best_location = m.best_location()
  kill_list = []
  while len(kill_list) < 200:
    sweep = m.sweep_from(*best_location)
    kill_list += sweep
    for p in sweep:
      m.vaporize(*p)
  x, y = kill_list[199]
  print(100*x + y)



if __name__ == '__main__':
  doctest.testmod()
  solve_pt1()
  solve_pt2()
