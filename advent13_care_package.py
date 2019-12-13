# Lint as: python3
"""Advent of Code, Day 13 -- Care Package."""


import doctest


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


class Arkanoid(object):

  class ScreenBuffer(object):
    tile_chars = [' ', 'H', '#', '=', 'o']
    def __init__(self, w, h):
      self.width = w
      self.height = h
      self.data = [0 for _ in range(w * h)]

    def __str__(self):
      chars = ''.join([self.tile_chars[c] for c in self.data])
      return '\n'.join([chars[r * self.width : r * self.width + self.width]
                        for r in range(self.height)])

    def set_tile(self, x, y, tile):
      if x >= self.width or y >= self.height:
        w = max(self.width, x + 1)
        h = max(self.height, y + 1)
        self.grow_buffer(w, h)
      self.data[y * self.width + x] = tile

    def grow_buffer(self, w, h):
      old_w = self.width
      old_h = self.height
      delta_w = w - old_w
      delta_h = h - old_h
      if delta_w < 0 or delta_h < 0:
        raise Exception
      new_buffer = []
      for r in range(old_h):
        new_buffer += self.data[r * old_w : r * old_w + old_w]
        new_buffer += [0 for _ in range(delta_w)]
      for r in range(delta_h):
        new_buffer += [0 for _ in range(w)]
      assert(len(new_buffer) == w * h)
      self.width = w
      self.height = h
      self.data = new_buffer

  def __init__(self):
    self.cpu = IntcodeComputer()
    with open('advent13_game_program.txt') as f:
      prog = f.read()
      self.cpu.load_program(prog)
    self.cpu.input_needed_handler = self.get_player_input
    self.cpu.output_ready_handler = self.handle_output
    self.score = 0
    self.free_play = False
    self.auto_play = False
    self.screen_buffer = self.ScreenBuffer(0,0)

  def handle_output(self):
    if len(self.cpu.output) >= 3 and len(self.cpu.output) % 3 == 0:
      x = self.cpu.output[-3]
      y = self.cpu.output[-2]
      tile = self.cpu.output[-1]
      if x == -1:
        self.score = tile
      else:
        self.screen_buffer.set_tile(x, y, tile)

  def print_screen(self):
    print('SCORE: {}'.format(self.score))
    print(self.screen_buffer, end='\n\n')

  def get_player_input(self):
    self.print_screen()
    if self.auto_play:
      self.cpu.input = self.best_move()
    else:
      user_input = -1
      while user_input not in ['[', '', ']', 'q']:
        user_input = input('> ')
      if user_input == '[':
        self.cpu.input = -1
      elif user_input == '':
        self.cpu.input = 0
      elif user_input == ']':
        self.cpu.input = 1
      else:
        raise Exception

    print('\n')

  def best_move(self):
    ball_xpos = self.screen_buffer.data.index(4) % self.screen_buffer.width
    paddle_xpos = self.screen_buffer.data.index(3) % self.screen_buffer.width
    print('Ball is at {}, paddle is at {}.'.format(ball_xpos, paddle_xpos))
    if ball_xpos < paddle_xpos:
      return -1
    elif ball_xpos > paddle_xpos:
      return 1
    else:
      return 0

  def go(self):
    self.cpu.mem[0] = 2 if self.free_play else 1
    self.cpu.run()

def solve_pt1():
  arkanoid = Arkanoid()
  arkanoid.go()
  print(len([c for c in str(arkanoid.screen_buffer)
             if c == Arkanoid.ScreenBuffer.tile_chars[2]]))


def solve_pt2():
  arkanoid = Arkanoid()
  arkanoid.free_play = True
  arkanoid.auto_play = True
  arkanoid.go()
  arkanoid.print_screen()


if __name__ == "__main__":
  doctest.testmod()
  solve_pt1()
  solve_pt2()
