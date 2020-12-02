# Lint as: python3
r"""Advent of Code, Day 12 -- N-body problem.

>>> system = GravitationalSystem()
>>> system.members.append(GravitationalSystem.Body((-1, 0, 2)))
>>> system.members.append(GravitationalSystem.Body((2, -10, -7)))
>>> system.members.append(GravitationalSystem.Body((4, -8, 8)))
>>> system.members.append(GravitationalSystem.Body((3, 5, -1)))

>>> print(system)
(-1, 0, 2) (0, 0, 0)
(2, -10, -7) (0, 0, 0)
(4, -8, 8) (0, 0, 0)
(3, 5, -1) (0, 0, 0)

>>> system.step()
>>> print(system)
(2, -1, 1) (3, -1, -1)
(3, -7, -4) (1, 3, 3)
(1, -7, 5) (-3, 1, -3)
(2, 2, 0) (-1, -3, 1)

>>> system.step()
>>> print(system)
(5, -3, -1) (3, -2, -2)
(1, -2, 2) (-2, 5, 6)
(1, -4, -1) (0, 3, -6)
(1, -4, 2) (-1, -6, 2)

>>> system.step()
>>> print(system)
(5, -6, -1) (0, -3, 0)
(0, 0, 6) (-1, 2, 4)
(2, 1, -5) (1, 5, -4)
(1, -8, 2) (0, -4, 0)

>>> system.step()
>>> print(system)
(2, -8, 0) (-3, -2, 1)
(2, 1, 7) (2, 1, 1)
(2, 3, -6) (0, 2, -1)
(2, -9, 1) (1, -1, -1)

>>> system.step()
>>> print(system)
(-1, -9, 2) (-3, -1, 2)
(4, 1, 5) (2, 0, -2)
(2, 2, -4) (0, -1, 2)
(3, -7, -1) (1, 2, -2)

>>> system.step()
>>> print(system)
(-1, -7, 3) (0, 2, 1)
(3, 0, 0) (-1, -1, -5)
(3, -2, 1) (1, -4, 5)
(3, -4, -2) (0, 3, -1)

>>> system.step()
>>> print(system)
(2, -2, 1) (3, 5, -2)
(1, -4, -4) (-2, -4, -4)
(3, -7, 5) (0, -5, 4)
(2, 0, 0) (-1, 4, 2)

>>> system.step()
>>> print(system)
(5, 2, -2) (3, 4, -3)
(2, -7, -5) (1, -3, -1)
(0, -9, 6) (-3, -2, 1)
(1, 1, 3) (-1, 1, 3)

>>> system.step()
>>> print(system)
(5, 3, -4) (0, 1, -2)
(2, -9, -3) (0, -2, 2)
(0, -8, 4) (0, 1, -2)
(1, 1, 5) (0, 0, 2)

>>> system.step()
>>> print(system)
(2, 1, -3) (-3, -2, 1)
(1, -8, 0) (-1, 1, 3)
(3, -6, 1) (3, 2, -3)
(2, 0, 4) (1, -1, -1)

>>> for m in system.members:
...   print(m.pe(), m.ke(), m.e())
6 6 36
9 5 45
10 8 80
6 3 18
>>> system.e()
179

>>> system = GravitationalSystem()
>>> system.members.append(GravitationalSystem.Body((-1, 0, 2)))
>>> system.members.append(GravitationalSystem.Body((2, -10, -7)))
>>> system.members.append(GravitationalSystem.Body((4, -8, 8)))
>>> system.members.append(GravitationalSystem.Body((3, 5, -1)))
>>> s = 0
>>> start = str(system)
>>> current = None
>>> while start != current:
...   system.step()
...   current = str(system)
...   s += 1
>>> s
2772
"""


import doctest


class GravitationalSystem():

  class Body():
    def __init__(self, position, velocity=(0, 0, 0)):
      self.position = position
      self.velocity = velocity

    def __repr__(self):
      return '({}, {}, {}) ({}, {}, {})'.format(
          *self.position, *self.velocity)

    def pe(self):
      x, y, z = self.position
      return abs(x) + abs(y) + abs(z)

    def ke(self):
      x, y, z = self.velocity
      return abs(x) + abs(y) + abs(z)

    def e(self):
      return self.pe() * self.ke()

  def __init__(self):
    self.members = []

  def __str__(self):
    return '\n'.join([str(m) for m in self.members])

  def apply_gravity(self):
    for i, a in enumerate(self.members):
      ax, ay, az = a.position
      avx, avy, avz = a.velocity
      avx += (len([1 for m in self.members if m.position[0] > ax])
              - len([1 for m in self.members if m.position[0] < ax]))
      avy += (len([1 for m in self.members if m.position[1] > ay])
              - len([1 for m in self.members if m.position[1] < ay]))
      avz += (len([1 for m in self.members if m.position[2] > az])
              - len([1 for m in self.members if m.position[2] < az]))
      self.members[i].velocity = (avx, avy, avz)

  def apply_velocity(self):
    for i, b in enumerate(self.members):
      x, y, z = b.position
      vx, vy, vz = b.velocity
      self.members[i].position = (x + vx, y + vy, z + vz)

  def step(self):
    self.apply_gravity()
    self.apply_velocity()

  def e(self):
    return sum([m.e() for m in self.members])


def solve_pt1():
  system = GravitationalSystem()
  system.members.append(GravitationalSystem.Body((-3, 10, -1)))
  system.members.append(GravitationalSystem.Body((-12, -10, -5)))
  system.members.append(GravitationalSystem.Body((-9, 0, 10)))
  system.members.append(GravitationalSystem.Body((7, -5, -3)))
  for _ in range(1000):
    system.step()
  print(system.e())


def solve_pt2():
  pass


if __name__ == '__main__':
  doctest.testmod()
  solve_pt1()
  solve_pt2()
