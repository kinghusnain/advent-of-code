# Lint as: python3
"""Advent of Code, Day 5 -- Intcode computer v2.

Tests:

>>> cpu = IntcodeComputer()
>>> mem = cpu.load_program("3,0,4,0,99")
>>> cpu.input = 'test'
>>> cpu.step()
['test', 0, 4, 0, 99]
>>> mem = cpu.run()
>>> cpu.output
'test'
>>> mem = cpu.load_program("1002,4,3,4,33")
>>> cpu.run()
[1002, 4, 3, 4, 99]
>>> mem = cpu.load_program("1101,100,-1,4,0")
>>> cpu.run()
[1101, 100, -1, 4, 99]

>>> mem = cpu.load_program("3,9,8,9,10,9,4,9,99,-1,8")
>>> cpu.input = 8
>>> mem = cpu.run()
>>> cpu.output
1
>>> mem = cpu.load_program("3,9,8,9,10,9,4,9,99,-1,8")
>>> cpu.input = 6
>>> mem = cpu.run()
>>> cpu.output
0
>>> mem = cpu.load_program("3,3,1108,-1,8,3,4,3,99")
>>> cpu.input = 8
>>> mem = cpu.run()
>>> cpu.output
1
>>> mem = cpu.load_program("3,3,1108,-1,8,3,4,3,99")
>>> cpu.input = 6
>>> mem = cpu.run()
>>> cpu.output
0

>>> mem = cpu.load_program("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9")
>>> cpu.input = 8
>>> mem = cpu.run()
>>> cpu.output
1
>>> mem = cpu.load_program("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9")
>>> cpu.input = 0
>>> mem = cpu.run()
>>> cpu.output
0

>>> mem = cpu.load_program("3,3,1105,-1,9,1101,0,0,12,4,12,99,1")
>>> cpu.input = 8
>>> mem = cpu.run()
>>> cpu.output
1
>>> mem = cpu.load_program("3,3,1105,-1,9,1101,0,0,12,4,12,99,1")
>>> cpu.input = 0
>>> mem = cpu.run()
>>> cpu.output
0

>>> mem = cpu.load_program('''3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,\
31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,\
1,20,4,20,1105,1,46,98,99''')
>>> cpu.input = 7
>>> mem = cpu.run()
>>> cpu.output
999
>>> mem = cpu.load_program('''3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,\
31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,\
1,20,4,20,1105,1,46,98,99''')
>>> cpu.input = 8
>>> mem = cpu.run()
>>> cpu.output
1000
>>> mem = cpu.load_program('''3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,\
31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,\
1,20,4,20,1105,1,46,98,99''')
>>> cpu.input = 9
>>> mem = cpu.run()
>>> cpu.output
1001
"""


import doctest


class IntcodeComputer:

  def __init__(self):
    self.ip = 0
    self.halt = False
    self.mem = []
    self.input = None
    self.output = None

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
    self.instr_impl[99] = self.halt_instr

  def load_program(self, prog):
    self.mem = [int(e) for e in prog.split(",")]
    self.ip = 0
    self.halt = False
    return self.mem

  def run(self):
    while self.ip < len(self.mem) and not self.halt:
      self.step()
    return self.mem

  def step(self):
    instr = "{:0>5}".format(self.mem[self.ip])
    opcode = int(instr[3:5])
    self.param_modes = [int(m) for m in reversed(instr[0:3])]
    self.instr_impl[opcode]()
    return self.mem

  def get_param(self, i):
    if self.param_modes[i] == 0:
      return self.mem[self.mem[self.ip + i + 1]]
    else:
      return self.mem[self.ip + i + 1]

  def add_instr(self):
    operand1 = self.get_param(0)
    operand2 = self.get_param(1)
    dest = self.mem[self.ip + 1 + 2]
    self.mem[dest] = operand1 + operand2
    self.ip += 4
    return self.mem

  def mult_instr(self):
    operand1 = self.get_param(0)
    operand2 = self.get_param(1)
    dest = self.mem[self.ip + 1 + 2]
    self.mem[dest] = operand1 * operand2
    self.ip += 4
    return self.mem

  def in_instr(self):
    dest = self.mem[self.ip + 1]
    self.mem[dest] = self.input
    self.ip += 2
    return self.mem

  def out_instr(self):
    val = self.get_param(0)
    self.output = val
    self.ip += 2
    return self.mem

  def jump_true_instr(self):
    val = self.get_param(0)
    dest = self.get_param(1)
    if val != 0:
      self.ip = dest
    else:
      self.ip += 3
    return self.mem

  def jump_false_instr(self):
    val = self.get_param(0)
    dest = self.get_param(1)
    if val == 0:
      self.ip = dest
    else:
      self.ip += 3
    return self.mem

  def lessthan_instr(self):
    operand1 = self.get_param(0)
    operand2 = self.get_param(1)
    dest = self.mem[self.ip + 1 + 2]
    if operand1 < operand2:
      self.mem[dest] = 1
    else:
      self.mem[dest] = 0
    self.ip += 4
    return self.mem

  def equals_instr(self):
    operand1 = self.get_param(0)
    operand2 = self.get_param(1)
    dest = self.mem[self.ip + 1 + 2]
    if operand1 == operand2:
      self.mem[dest] = 1
    else:
      self.mem[dest] = 0
    self.ip += 4
    return self.mem

  def halt_instr(self):
    self.halt = True
    self.ip += 1
    return self.mem


def run_diagnostic(sys_id):
  prog = "3,225,1,225,6,6,1100,1,238,225,104,0,1102,35,92,225,1101,25,55,225,1102,47,36,225,1102,17,35,225,1,165,18,224,1001,224,-106,224,4,224,102,8,223,223,1001,224,3,224,1,223,224,223,1101,68,23,224,101,-91,224,224,4,224,102,8,223,223,101,1,224,224,1,223,224,223,2,217,13,224,1001,224,-1890,224,4,224,102,8,223,223,1001,224,6,224,1,224,223,223,1102,69,77,224,1001,224,-5313,224,4,224,1002,223,8,223,101,2,224,224,1,224,223,223,102,50,22,224,101,-1800,224,224,4,224,1002,223,8,223,1001,224,5,224,1,224,223,223,1102,89,32,225,1001,26,60,224,1001,224,-95,224,4,224,102,8,223,223,101,2,224,224,1,223,224,223,1102,51,79,225,1102,65,30,225,1002,170,86,224,101,-2580,224,224,4,224,102,8,223,223,1001,224,6,224,1,223,224,223,101,39,139,224,1001,224,-128,224,4,224,102,8,223,223,101,3,224,224,1,223,224,223,1102,54,93,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1008,677,677,224,1002,223,2,223,1005,224,329,101,1,223,223,7,677,677,224,102,2,223,223,1006,224,344,101,1,223,223,108,677,677,224,1002,223,2,223,1006,224,359,1001,223,1,223,7,677,226,224,1002,223,2,223,1005,224,374,1001,223,1,223,1107,677,226,224,1002,223,2,223,1005,224,389,1001,223,1,223,107,226,677,224,102,2,223,223,1005,224,404,1001,223,1,223,1108,226,677,224,1002,223,2,223,1006,224,419,101,1,223,223,107,226,226,224,102,2,223,223,1005,224,434,1001,223,1,223,108,677,226,224,1002,223,2,223,1006,224,449,101,1,223,223,108,226,226,224,102,2,223,223,1006,224,464,1001,223,1,223,1007,226,226,224,1002,223,2,223,1005,224,479,101,1,223,223,8,677,226,224,1002,223,2,223,1006,224,494,101,1,223,223,1007,226,677,224,102,2,223,223,1006,224,509,101,1,223,223,7,226,677,224,1002,223,2,223,1005,224,524,101,1,223,223,107,677,677,224,102,2,223,223,1005,224,539,101,1,223,223,1008,677,226,224,1002,223,2,223,1005,224,554,1001,223,1,223,1008,226,226,224,1002,223,2,223,1006,224,569,1001,223,1,223,1108,226,226,224,102,2,223,223,1005,224,584,101,1,223,223,1107,226,677,224,1002,223,2,223,1005,224,599,1001,223,1,223,8,226,677,224,1002,223,2,223,1006,224,614,1001,223,1,223,1108,677,226,224,102,2,223,223,1005,224,629,1001,223,1,223,8,226,226,224,1002,223,2,223,1005,224,644,1001,223,1,223,1107,677,677,224,1002,223,2,223,1005,224,659,1001,223,1,223,1007,677,677,224,1002,223,2,223,1005,224,674,101,1,223,223,4,223,99,226"
  cpu = IntcodeComputer()
  cpu.load_program(prog)
  cpu.input = sys_id
  cpu.run()
  return cpu.output


def solve_pt1():
  print(run_diagnostic(1))


def solve_pt2():
  print(run_diagnostic(5))


if __name__ == "__main__":
  doctest.testmod()
  solve_pt1()
  solve_pt2()
