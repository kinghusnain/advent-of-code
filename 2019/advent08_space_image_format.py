# Lint as: python3
"""Advent of Code, Day 8 -- Space Image Format.

>>> check_image('123456789012', 3, 2)
1
>>> check_image('111122000000', 3, 2)
8
>>> check_image('000000111122', 3, 2)
8
>>> render_image('0222112222120000', 2, 2)
'0110'
>>> render_image('22220222112222120000', 2, 2)
'0110'
"""


import doctest
import functools


def check_image(img, w, h):
  layers = layers_from_image(img, w, h)
  layers.sort(key=lambda L: len([p for p in L if p == '0']))
  return (len([p for p in layers[0] if p == '1'])
          * len([p for p in layers[0] if p == '2']))


def render_image(img, w, h):
  layers = layers_from_image(img, w, h)
  return functools.reduce(merge_layers, layers, '2' * w * h)


def layers_from_image(img, w, h):
  layers = []
  for li in range(len(img) // w // h):
    layers.append(img[li * w * h : (li + 1) * w * h])
    assert len(layers[-1]) == w * h
  return layers


def merge_layers(front, back):
  """Merge layers, honoring transparency.

  >>> merge_layers('212', '002')
  '012'
  >>> merge_layers(merge_layers('212', '002'), '111')
  '011'
  """
  return ''.join([(px if px != '2' else back[i]) for i, px in enumerate(front)])


def solve_pt1():
  img = ''
  with open('advent08_input.txt') as f:
    img = f.read().strip()
  assert len(img) % 25 * 6 == 0
  print(check_image(img, 25, 6))


def solve_pt2():
  img = ''
  with open('advent08_input.txt') as f:
    img = f.read().strip()
  r = render_image(img, 25, 6)
  assert len(r) == 25 * 6
  for i, px in enumerate(r):
    print('XX' if px == '1' else '  ', end='')
    if i % 25 == 25 - 1:
      print('')


if __name__ == '__main__':
  doctest.testmod()
  solve_pt1()
  solve_pt2()
