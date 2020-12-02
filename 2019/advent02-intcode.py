# Lint as: python3
"""Advent of Code, Day 2 -- Intcode computer.

Tests:

>>> cpu = IntcodeComputer()
>>> cpu.load_program("1,9,10,3,2,3,11,0,99,30,40,50")
[1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
>>> cpu.step()
[1, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
>>> cpu.step()
[3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
>>> cpu.load_program("1,9,10,3,2,3,11,0,99,30,40,50")
[1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
>>> cpu.run()
[3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]

Solution to pt. 1:

>>> cpu = IntcodeComputer()
>>> cpu.load_program("1,0,0,0,99")
[1, 0, 0, 0, 99]
>>> cpu.run()
[2, 0, 0, 0, 99]
>>> cpu.load_program("2,3,0,3,99")
[2, 3, 0, 3, 99]
>>> cpu.run()
[2, 3, 0, 6, 99]
>>> cpu.load_program("2,4,4,5,99,0")
[2, 4, 4, 5, 99, 0]
>>> cpu.run()
[2, 4, 4, 5, 99, 9801]
>>> cpu.load_program("1,1,1,4,99,5,6,0,99")
[1, 1, 1, 4, 99, 5, 6, 0, 99]
>>> cpu.run()
[30, 1, 1, 4, 2, 5, 6, 0, 99]
"""


import doctest


class IntcodeComputer:

  def __init__(self):
    self.ip = 0
    self.halt = False
    self.mem = []

    self.instr_impl = {}
    self.instr_impl[1] = self.add_instr
    self.instr_impl[2] = self.mult_instr
    self.instr_impl[99] = self.halt_instr

  def load_program(self, prog):
    self.mem = [int(e) for e in prog.split(",")]
    return self.mem

  def run(self):
    self.ip = 0
    self.halt = False
    while self.ip < len(self.mem) and not self.halt:
      self.step()
    return self.mem

  def step(self):
    op = self.mem[self.ip]
    self.instr_impl[op]()
    return self.mem

  def add_instr(self):
    operand1 = self.mem[self.ip + 1]
    operand2 = self.mem[self.ip + 2]
    dest = self.mem[self.ip + 3]
    self.mem[dest] = self.mem[operand1] + self.mem[operand2]
    self.ip += 4
    return self.mem

  def mult_instr(self):
    operand1 = self.mem[self.ip + 1]
    operand2 = self.mem[self.ip + 2]
    dest = self.mem[self.ip + 3]
    self.mem[dest] = self.mem[operand1] * self.mem[operand2]
    self.ip += 4
    return self.mem

  def halt_instr(self):
    self.halt = True
    self.ip += 1
    return self.mem


def find_inputs(program, target_output):
  cpu = IntcodeComputer()
  for noun in range(0, 100):
    for verb in range(0, 100):
      cpu.load_program(program)
      cpu.mem[1] = noun
      cpu.mem[2] = verb
      dump = cpu.run()
      out = dump[0]
      if out == target_output:
        return noun, verb


def main():
  p = """1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,10,19,1,19,6,23,2,23,13,27,1,27,5,
      31,2,31,10,35,1,9,35,39,1,39,9,43,2,9,43,47,1,5,47,51,2,13,51,55,1,55,9,
      59,2,6,59,63,1,63,5,67,1,10,67,71,1,71,10,75,2,75,13,79,2,79,13,
      83,1,5,83,87,1,87,6,91,2,91,13,95,1,5,95,99,1,99,2,103,1,103,6,0,99,2,
      14,0,0"""
  noun, verb = find_inputs(p, 19690720)
  print(100 * noun + verb)


if __name__ == "__main__":
  doctest.testmod()
  main()
