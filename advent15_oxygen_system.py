# Lint as: python3
"""Advent of Code, Day 15 -- Oxygen System."""


import doctest
import random


class IntcodeComputer:

  def __init__(self):
    self.ip = 0
    self.halted = False
    self.mem = []
    self.relative_base = 0
    self._input_buffer = []
    self.output = []
    self.input_needed_handler = lambda: None
    self.output_ready_handler = lambda: None

    self.param_modes = [0, 0, 0]
    self.instr_impl = {}
    self.instr_impl[1] = self.add_instr
    self.instr_impl[2] = self.mult_instr
    self.instr_impl[3] = self.in_instr
    self.instr_impl[4] = self.out_instr
    self.instr_impl[5] = self.jump_true_instr
    self.instr_impl[6] = self.jump_false_instr
    self.instr_impl[7] = self.lessthan_instr
    self.instr_impl[8] = self.equals_instr
    self.instr_impl[9] = self.setrel_instr
    self.instr_impl[99] = self.halt_instr

  @property
  def input(self):
    if len(self._input_buffer) > 0:
      return self._input_buffer.pop()
    else:
      self.input_needed_handler()
      return self.input

  @input.setter
  def input(self, value):
    self._input_buffer.insert(0, value)

  def load_program(self, prog):
    self.mem = [int(e) for e in prog.split(",")]
    self.ip = 0
    self.halted = False
    return self.mem

  def run(self):
    while self.ip < len(self.mem) and not self.halted:
      self.step()
    return self.mem

  def step(self):
    instr = "{:0>5}".format(self.get_mem(self.ip))
    opcode = int(instr[3:5])
    self.param_modes = [int(m) for m in reversed(instr[0:3])]
    self.instr_impl[opcode]()
    return self.mem

  def get_param(self, i):
    if self.param_modes[i] == 0:
      return self.get_param_position(i)
    elif self.param_modes[i] == 1:
      return self.get_param_immediate(i)
    elif self.param_modes[i] == 2:
      return self.get_param_relative(i)
    else:
      raise Exception

  def get_param_position(self, i):
    return self.get_mem(self.get_mem(self.ip + i + 1))

  def get_param_relative(self, i):
    return self.get_mem(self.relative_base + self.get_mem(self.ip + i + 1))

  def get_param_immediate(self, i):
    return self.get_mem(self.ip + i + 1)

  def get_dest_param(self, i):
    if self.param_modes[i] == 0:
      return self.get_mem(self.ip + i + 1)
    elif self.param_modes[i] == 2:
      return self.relative_base + self.get_mem(self.ip + i + 1)
    else:
      raise Exception

  def get_mem(self, dest):
    if len(self.mem) <= dest:
      self.mem += [0 for _ in range(dest + 1 - len(self.mem))]
    return self.mem[dest]

  def put_mem(self, dest, value):
    if len(self.mem) <= dest:
      self.mem += [0 for _ in range(dest + 1 - len(self.mem))]
    self.mem[dest] = value

  def add_instr(self):
    operand1 = self.get_param(0)
    operand2 = self.get_param(1)
    dest = self.get_dest_param(2)
    self.put_mem(dest, operand1 + operand2)
    self.ip += 4
    return self.mem

  def mult_instr(self):
    operand1 = self.get_param(0)
    operand2 = self.get_param(1)
    dest = self.get_dest_param(2)
    self.put_mem(dest, operand1 * operand2)
    self.ip += 4
    return self.mem

  def in_instr(self):
    dest = self.get_dest_param(0)
    self.put_mem(dest, self.input)
    self.ip += 2
    return self.mem

  def out_instr(self):
    val = self.get_param(0)
    self.output.append(val)
    self.ip += 2
    self.output_ready_handler()
    return self.mem

  def jump_true_instr(self):
    val = self.get_param(0)
    target = self.get_param(1)
    if val != 0:
      self.ip = target
    else:
      self.ip += 3
    return self.mem

  def jump_false_instr(self):
    val = self.get_param(0)
    target = self.get_param(1)
    if val == 0:
      self.ip = target
    else:
      self.ip += 3
    return self.mem

  def lessthan_instr(self):
    operand1 = self.get_param(0)
    operand2 = self.get_param(1)
    dest = self.get_dest_param(2)
    if operand1 < operand2:
      self.put_mem(dest, 1)
    else:
      self.put_mem(dest, 0)
    self.ip += 4
    return self.mem

  def equals_instr(self):
    operand1 = self.get_param(0)
    operand2 = self.get_param(1)
    dest = self.get_dest_param(2)
    if operand1 == operand2:
      self.put_mem(dest, 1)
    else:
      self.put_mem(dest, 0)
    self.ip += 4
    return self.mem

  def setrel_instr(self):
    inc = self.get_param(0)
    self.relative_base += inc
    self.ip += 2
    return self.mem

  def halt_instr(self):
    self.halted = True
    self.ip += 1
    return self.mem


class RepairDroid:

  COMMANDS = {}
  COMMANDS['w'] = 1
  COMMANDS['s'] = 2
  COMMANDS['a'] = 3
  COMMANDS['d'] = 4
  COMMANDS['auto'] = None

  REVERSE = {}
  REVERSE[1] = 2
  REVERSE[2] = 1
  REVERSE[3] = 4
  REVERSE[4] = 3

  def __init__(self):
    self.cpu = IntcodeComputer()
    with open('advent15_repair_droid_firmware.txt') as f:
      self.cpu.load_program(f.read())
    self.cpu.input_needed_handler = self.get_next_move
    self.cpu.output_ready_handler = self.handle_output
    self.auto_explore = False
    self.auto_steps = 10000
    self.breadcrumbs = []
    self.location = 0,0
    self.map = {(0,0):  '.'}
    self.x_min = 0
    self.x_max = 0
    self.y_min = 0
    self.y_max = 0

  def get_next_move(self):
    self.breadcrumbs.append(self.location)
    # if self.cpu.output and self.cpu.output[-1] == 2:
    #   self.auto_explore = False
    #   path = remove_redundant_segments(self.breadcrumbs)
    #   print('Found in {} steps.'.format(len(path)))
    if self.auto_steps < 1:
      self.auto_explore = False
    if self.auto_explore:
      self.get_next_move_auto()
    else:
      self.get_next_move_manual()

  def get_next_move_auto(self):
    self.auto_steps -= 1
    x, y = self.location
    adjacent_tiles = [(x, y - 1),  # N
                      (x, y + 1),  # S
                      (x - 1, y),  # E
                      (x + 1, y)]  # W
    for d in range(4):
      if adjacent_tiles[d] not in self.map:
        self.cmd = d + 1
        self.cpu.input = self.cmd
        return
    self.cmd = random.randint(1,4)
    self.cpu.input = self.cmd

  def get_next_move_manual(self):
    self.print_map()
    c = ''
    while c not in self.COMMANDS:
      c = input('> ')
    if c == 'auto':
      self.auto_steps = 10000
      self.auto_explore = True
      self.get_next_move_auto()
    else:
      self.cmd = self.COMMANDS[c]
      self.cpu.input = self.cmd

  def print_map(self):
    print()
    for y in range(self.y_min, self.y_max + 1):
      for x in range(self.x_min, self.x_max + 1):
        c = ' '
        if (x,y) in self.map:
          c = 'D' if (x,y) == self.location else self.map[(x,y)]
          # c = 'o' if (x,y) == (0,0) else c
        print(c, end='')
      print()

  def handle_output(self):
    out = self.cpu.output[-1]
    if out == 0:
      self.record_wall()
    elif out == 1:
      self.record_space()
    elif out == 2:
      self.record_destination()
    else:
      raise Exception

  def record_wall(self):
    x, y = self.location
    if self.cmd == 1:    # N
      y -= 1
      self.y_min = min(y, self.y_min)
    elif self.cmd == 2:  # S
      y += 1
      self.y_max = max(y, self.y_max)
    elif self.cmd == 3:  # W
      x -= 1
      self.x_min = min(x, self.x_min)
    elif self.cmd == 4:  # E
      x += 1
      self.x_max = max(x, self.x_max)
    else:
      raise Exception
    self.map[(x, y)] = '#'

  def record_space(self):
    x, y = self.location
    if self.cmd == 1:    # N
      y -= 1
      self.y_min = min(y, self.y_min)
    elif self.cmd == 2:  # S
      y += 1
      self.y_max = max(y, self.y_max)
    elif self.cmd == 3:  # W
      x -= 1
      self.x_min = min(x, self.x_min)
    elif self.cmd == 4:  # E
      x += 1
      self.x_max = max(x, self.x_max)
    else:
      raise Exception
    self.map[(x, y)] = '.'
    self.location = x, y

  def record_destination(self):
    x, y = self.location
    if self.cmd == 1:    # N
      y -= 1
      self.y_min = min(y, self.y_min)
    elif self.cmd == 2:  # S
      y += 1
      self.y_max = max(y, self.y_max)
    elif self.cmd == 3:  # W
      x -= 1
      self.x_min = min(x, self.x_min)
    elif self.cmd == 4:  # E
      x += 1
      self.x_max = max(x, self.x_max)
    else:
      raise Exception
    self.map[(x, y)] = 'X'
    self.location = x, y


def remove_redundant_segments(path):
  i = 0
  print('Shrinking path of length {}...'.format(len(path)))
  while i < len(path):
    step = path[i]
    if step in path[:i]:
      j = path[:i].index(step)
      path = path[:j] + path[i:]
      i = path.index(step)
      print('Shrunk to size {}...'.format(len(path)))
    i += 1
  return path[1:]


def solve_pt1():
  bot = RepairDroid()
  bot.auto_explore = True
  bot.cpu.run()


def solve_pt2():
  complete_map = list("""
X### ### ############# # ########### ###X
#...#...#.............#.#...........#...#
#.#.#.#.###.#########.#.#.###.#####.###.#
#.#...#...#...#.....#.#.#.#...#.........#
#.#######.###.#.#####.#.#.#.###########.#
#.#...........#.......#.#.#.......#...#.#
#.###.#########.#######.#.#######.#.#.#.#
#...#.#.......#.#...............#.#.#...#
 ##.###.#####.#.#.###########.###.#.####X
#...#...#...#.#.#...#...#.....#...#.#...#
#.###.###.#.#.#.#####.#.#.#####.###.###.#
#...#...#.#.#.#...#...#.#...#...#.......#
#.#.###.###.#.###.#.###.#####.##########X
#.#...#.#...#.#...#.#.#.......#...#.....#
 ####.#.#.###.#.###.#.###.#####.#.#.###.#
#.....#.#...#.#.....#...#.#...#.#.....#.#
#.#####.#.#.#.#######.#.#.#.#.#.#######.#
#.#.....#.#.#...#.....#...#.#...#.......#
#.#.#######.###.###########.#####.######X
#.#.#.....#...#.#...........#...#.#.....#
#.#.#.#.#.#.#.#.#.#####.#####.###.#.###.#
#.#.#.#.#...#.#.#.#...#...#.....#.#.#...#
#.#.###.#####.#.#.#.#####.#####.#.#.#.##X
#.#...#.....#.#...#.#...#.#.....#.#.#...#
#.###.#.###.#####.#.#.###.#.#.###.#####.#
#.....#.#...#...#.#.#.......#.#...#.....#
#.#####.#.###.#.###.###########.###.####X
#...#...#...#.#.....#...........#.......#
 ##.###.###.#.#######.###########.#####.#
#.#...#.#...#.........#...#.....#.#.....#
#.###.###.#.###########.###.#.###.#.###.#
#.#...#...#.#...#.....#.#...#.....#.#...#
#.#.###.###.#.#.#.###.#.#.#########.#.##X
#...#...#.#...#.#.#...#.#.#......O#.#...#
#.###.###.#####.#.#.###.#.###.#.###.###.#
#.#...#.......#...#.#.........#.#...#.#.#
#.###.#.###.#######.#########.###.###.#.#
#.#...#.#.#.......#...#.....#.#...#.....#
#.#.###.#.#######.###.#.###.###.###.####X
#...#...........#.......#.......#.......#
 ### ########### ####### ####### #######X
  """.strip())
  tick = 0
  h = 41
  w = 41 + 1
  while complete_map.count('.') > 0:
    tmp = complete_map.copy()
    for i in range(len(complete_map)):
      if complete_map[i] == 'O':
        if complete_map[i - w] == '.':
          tmp[i - w] = 'O'
        if complete_map[i - 1] == '.':
          tmp[i - 1] = 'O'
        if complete_map[i + 1] == '.':
          tmp[i + 1] = 'O'
        if complete_map[i + w] == '.':
          tmp[i + w] = 'O'
    complete_map = tmp
    print(''.join(complete_map))
    tick += 1
    input('...')
  print('Done after {} ticks.'.format(tick))


if __name__ == "__main__":
  doctest.testmod()
  #solve_pt1()
  solve_pt2()
