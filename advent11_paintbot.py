# Lint as: python3
"""Advent of Code, Day 11 -- Space Police.

"""


import doctest


class IntcodeComputer:

  def __init__(self):
    self.ip = 0
    self.halted = False
    self.mem = []
    self.relative_base = 0
    self.input = []
    self.output = []
    self.interrupt_handler = lambda: None

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
    self.put_mem(dest, self.input.pop())
    self.ip += 2
    return self.mem

  def out_instr(self):
    val = self.get_param(0)
    self.output.append(val)
    self.ip += 2
    self.interrupt_handler()
    return self.mem

  def clear_input_buffer(self):
    self.input = []

  def clear_output_buffer(self):
    self.output = []

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


class Paintbot5000():

  def __init__(self, os):
    self.location = 0, 0
    self.facing = 0
    self.panels_painted = []
    self.cpu = IntcodeComputer()
    self.cpu.load_program(os)
    self.cpu.interrupt_handler = self.output_handler
    self.handler_buffer = []

  def output_handler(self):
    self.handler_buffer.append(self.cpu.output[-1])
    if len(self.handler_buffer) == 1:
      color = self.handler_buffer[0]
      self.paint_location(color)
    elif len(self.handler_buffer) == 2:
      _, direction = self.handler_buffer
      self.handler_buffer = []
      self.turn(direction)
      self.advance(1)
      detected_color = self.get_color()
      self.cpu.input.insert(0, detected_color)

  def paint_location(self, color):
    self.panels_painted.append((self.location, color))

  def turn(self, direction):
    if direction == 1:
      self.turn_cw()
    elif direction == 0:
      self.turn_ccw()
    else:
      raise Exception

  def turn_cw(self):
    self.facing = 0 if self.facing == 3 else self.facing + 1

  def turn_ccw(self):
    self.facing = 3 if self.facing == 0 else self.facing - 1

  def advance(self, distance):
    x, y = self.location
    if self.facing == 0:
      self.location = x, y + distance
    elif self.facing == 1:
      self.location = x + distance, y
    elif self.facing == 2:
      self.location = x, y - distance
    elif self.facing == 3:
      self.location = x - distance, y
    else:
      raise Exception

  def get_color(self, location=None):
    if location is None:
      location = self.location
    color = 0
    for loc, c in self.panels_painted:
      if location == loc:
        color = c
    return color

  def go(self, start_color):
    self.cpu.input.insert(0, start_color)
    self.cpu.run()


def solve_pt1():
  prog = "3,8,1005,8,328,1106,0,11,0,0,0,104,1,104,0,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,0,10,4,10,1001,8,0,29,1,104,7,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,0,10,4,10,1001,8,0,55,1,2,7,10,1006,0,23,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,1001,8,0,84,1006,0,40,1,1103,14,10,1,1006,16,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,1,8,10,4,10,1002,8,1,116,1006,0,53,1,1104,16,10,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,1,10,4,10,102,1,8,146,2,1104,9,10,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,1,10,4,10,1001,8,0,172,1006,0,65,1,1005,8,10,1,1002,16,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,0,8,10,4,10,102,1,8,204,2,1104,9,10,1006,0,30,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,102,1,8,233,2,1109,6,10,1006,0,17,1,2,6,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,1,8,10,4,10,102,1,8,266,1,106,7,10,2,109,2,10,2,9,8,10,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,1,10,4,10,1001,8,0,301,1,109,9,10,1006,0,14,101,1,9,9,1007,9,1083,10,1005,10,15,99,109,650,104,0,104,1,21102,1,837548789788,1,21101,0,345,0,1106,0,449,21101,0,846801511180,1,21101,0,356,0,1106,0,449,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21101,235244981271,0,1,21101,403,0,0,1105,1,449,21102,1,206182744295,1,21101,0,414,0,1105,1,449,3,10,104,0,104,0,3,10,104,0,104,0,21102,837896937832,1,1,21101,0,437,0,1106,0,449,21101,867965862668,0,1,21102,448,1,0,1106,0,449,99,109,2,22102,1,-1,1,21101,40,0,2,21102,1,480,3,21101,0,470,0,1106,0,513,109,-2,2106,0,0,0,1,0,0,1,109,2,3,10,204,-1,1001,475,476,491,4,0,1001,475,1,475,108,4,475,10,1006,10,507,1101,0,0,475,109,-2,2106,0,0,0,109,4,1201,-1,0,512,1207,-3,0,10,1006,10,530,21102,1,0,-3,22102,1,-3,1,21201,-2,0,2,21102,1,1,3,21102,549,1,0,1106,0,554,109,-4,2105,1,0,109,5,1207,-3,1,10,1006,10,577,2207,-4,-2,10,1006,10,577,21202,-4,1,-4,1106,0,645,21202,-4,1,1,21201,-3,-1,2,21202,-2,2,3,21101,596,0,0,1106,0,554,21201,1,0,-4,21102,1,1,-1,2207,-4,-2,10,1006,10,615,21101,0,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,637,22102,1,-1,1,21101,637,0,0,105,1,512,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2106,0,0"
  bot = Paintbot5000(prog)
  bot.go(0)
  panels = set([loc for loc, c in bot.panels_painted])
  print(len(panels))


def solve_pt2():
  prog = "3,8,1005,8,328,1106,0,11,0,0,0,104,1,104,0,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,0,10,4,10,1001,8,0,29,1,104,7,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,0,10,4,10,1001,8,0,55,1,2,7,10,1006,0,23,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,1001,8,0,84,1006,0,40,1,1103,14,10,1,1006,16,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,1,8,10,4,10,1002,8,1,116,1006,0,53,1,1104,16,10,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,1,10,4,10,102,1,8,146,2,1104,9,10,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,1,10,4,10,1001,8,0,172,1006,0,65,1,1005,8,10,1,1002,16,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,0,8,10,4,10,102,1,8,204,2,1104,9,10,1006,0,30,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,102,1,8,233,2,1109,6,10,1006,0,17,1,2,6,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,1,8,10,4,10,102,1,8,266,1,106,7,10,2,109,2,10,2,9,8,10,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,1,10,4,10,1001,8,0,301,1,109,9,10,1006,0,14,101,1,9,9,1007,9,1083,10,1005,10,15,99,109,650,104,0,104,1,21102,1,837548789788,1,21101,0,345,0,1106,0,449,21101,0,846801511180,1,21101,0,356,0,1106,0,449,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21101,235244981271,0,1,21101,403,0,0,1105,1,449,21102,1,206182744295,1,21101,0,414,0,1105,1,449,3,10,104,0,104,0,3,10,104,0,104,0,21102,837896937832,1,1,21101,0,437,0,1106,0,449,21101,867965862668,0,1,21102,448,1,0,1106,0,449,99,109,2,22102,1,-1,1,21101,40,0,2,21102,1,480,3,21101,0,470,0,1106,0,513,109,-2,2106,0,0,0,1,0,0,1,109,2,3,10,204,-1,1001,475,476,491,4,0,1001,475,1,475,108,4,475,10,1006,10,507,1101,0,0,475,109,-2,2106,0,0,0,109,4,1201,-1,0,512,1207,-3,0,10,1006,10,530,21102,1,0,-3,22102,1,-3,1,21201,-2,0,2,21102,1,1,3,21102,549,1,0,1106,0,554,109,-4,2105,1,0,109,5,1207,-3,1,10,1006,10,577,2207,-4,-2,10,1006,10,577,21202,-4,1,-4,1106,0,645,21202,-4,1,1,21201,-3,-1,2,21202,-2,2,3,21101,596,0,0,1106,0,554,21201,1,0,-4,21102,1,1,-1,2207,-4,-2,10,1006,10,615,21101,0,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,637,22102,1,-1,1,21101,637,0,0,105,1,512,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2106,0,0"
  bot = Paintbot5000(prog)
  bot.go(1)
  panels = list(set([loc for loc, c in bot.panels_painted]))
  panels.sort(key=lambda x: x[0])
  min_x = panels[0][0]
  max_x = panels[-1][0]
  panels.sort(key=lambda x: x[1])
  min_y = panels[0][1]
  max_y = panels[-1][1]
  for y in range(max_y, min_y - 1, -1):
    for x in range(min_x, max_x + 1):
      c = bot.get_color(location=(x, y))
      if c:
        print('##', end='')
      else:
        print('  ', end='')
    print()


if __name__ == "__main__":
  doctest.testmod()
  solve_pt1()
  solve_pt2()
