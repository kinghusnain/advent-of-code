# Lint as: python3
"""Advent of Code, Day 2 -- Intcode computer.

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
    self.pc = 0
    self.halt = False
    self.mem = []
    self.op_impl = {}
    self.op_impl[1] = self.exec_op01
    self.op_impl[2] = self.exec_op02
    self.op_impl[99] = self.exec_op99

  def load_program(self, prog):
    self.mem = [int(e) for e in prog.split(",")]
    return self.mem

  def run(self):
    self.pc = 0
    self.halt = False
    while self.pc < len(self.mem) and not self.halt:
      self.step()
    return self.mem

  def step(self):
    op = self.mem[self.pc]
    self.op_impl[op]()
    self.pc += 4
    return self.mem

  def exec_op01(self):
    operand1 = self.mem[self.pc + 1]
    operand2 = self.mem[self.pc + 2]
    dest = self.mem[self.pc + 3]
    self.mem[dest] = self.mem[operand1] + self.mem[operand2]
    return self.mem

  def exec_op02(self):
    operand1 = self.mem[self.pc + 1]
    operand2 = self.mem[self.pc + 2]
    dest = self.mem[self.pc + 3]
    self.mem[dest] = self.mem[operand1] * self.mem[operand2]
    return self.mem

  def exec_op99(self):
    self.halt = True
    return self.mem


def main():
  pass

if __name__ == "__main__":
  doctest.testmod()
  main()
