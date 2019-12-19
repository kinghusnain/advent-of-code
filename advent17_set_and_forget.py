# Lint as: python3
"""Advent of Code, Day 17 -- Set and forget."""


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


def ascii():
  with open('advent17_ascii.txt') as f:
    prog = f.read()
  cpu = IntcodeComputer()
  cpu.load_program(prog)
  cpu.run()
  return bytes(cpu.output).decode('ascii')


def solve_pt1():
  scaffold_map = ascii().strip().split('\n')
  alignment_params = []
  for y in range(1, len(scaffold_map) - 1):
    for x in range(1, len(scaffold_map[y]) - 1):
      if (scaffold_map[y][x] == '#'
          and scaffold_map[y - 1][x] == '#'
          and scaffold_map[y + 1][x] == '#'
          and scaffold_map[y][x - 1] == '#'
          and scaffold_map[y][x + 1] == '#'):
        alignment_params.append(x * y)
  print(sum(alignment_params))


def solve_pt2():
  with open('advent17_ascii.txt') as f:
    prog = f.read()
  prog = '2' + prog[1:]
  cpu = IntcodeComputer()
  cpu.load_program(prog)

  def get_input():
    cmd = input('  --------------------\n> ')
    encoded_cmd = [int(c) for c in cmd.encode('ascii')] + [10]
    for c in encoded_cmd:
      cpu.input = c

  def print_output():
    out = cpu.output[-1]
    if out < 256:
      s = bytes([out]).decode('ascii')
    else:
      s = str(out) + '\n'
    print(s, end='')

  cpu.input_needed_handler = get_input
  cpu.output_ready_handler = print_output
  cpu.run()


if __name__ == "__main__":
  doctest.testmod()
  solve_pt1()
  solve_pt2()
