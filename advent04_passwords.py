# Lint as: python3
"""Advent of Code, Day 4 -- Secure container passwords."""


import doctest


def has_double(pw):
  """True if pw has a double.

  >>> has_double('111111')
  True
  >>> has_double('123456')
  False
  """
  for i in range(len(pw) - 1):
    if pw[i] == pw[i + 1]:
      return True
  return False


def has_double_strict(pw):
  """True if pw has a double that isn't part of a triple or more.

  >>> has_double_strict('112233')
  True
  >>> has_double_strict('123444')
  False
  >>> has_double_strict('111122')
  True
  """
  consecutive_runs = [pw[0]]
  for i in range(1, len(pw)):
    if pw[i] == consecutive_runs[-1][-1]:
      consecutive_runs[-1] += pw[i]
    else:
      consecutive_runs.append(pw[i])
  for run in consecutive_runs:
    if len(run) == 2:
      return True
  return False


def is_ascending(pw):
  """True if pw is ascending.

  >>> is_ascending('111111')
  True
  >>> is_ascending('123456')
  True
  >>> is_ascending('123454')
  False
  """
  for i in range(len(pw) - 1):
    if pw[i] > pw[i + 1]:
      return False
  return True


def possible_passwords(lower, upper):
  return (pw for pw in map(str, range(lower, upper))
          if is_ascending(pw) and has_double(pw))


def possible_passwords_strict(lower, upper):
  return (pw for pw in map(str, range(lower, upper))
          if is_ascending(pw) and has_double_strict(pw))


def solve_pt1():
  pws = possible_passwords(372304, 847060)
  count = 0
  for _ in pws:
    count += 1
  print(count)


def solve_pt2():
  pws = possible_passwords_strict(372304, 847060)
  count = 0
  for _ in pws:
    count += 1
  print(count)


if __name__ == '__main__':
  doctest.testmod()
  solve_pt1()
  solve_pt2()
