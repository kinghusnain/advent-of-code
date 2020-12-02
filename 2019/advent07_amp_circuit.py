# Lint as: python3
"""Advent of Code, Day 7 -- Amplification Circuit.

>>> test_phase_sequence([4,3,2,1,0], '3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0')
43210
>>> test_phase_sequence([0,1,2,3,4], '3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0')
54321
>>> test_phase_sequence([1,0,4,3,2], '3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0')
65210

>>> test_phase_sequence_with_feedback([9,8,7,6,5], '3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5')
139629729
>>> test_phase_sequence_with_feedback([9,7,8,5,6], '3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10')
18216
"""


import doctest


class IntcodeComputer:

  def __init__(self):
    self.ip = 0
    self.halted = False
    self.mem = []
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
    instr = "{:0>5}".format(self.mem[self.ip])
    opcode = int(instr[3:5])
    self.param_modes = [int(m) for m in reversed(instr[0:3])]
    self.instr_impl[opcode]()
    return self.mem

  def get_param(self, i):
    if self.param_modes[i] == 0:
      return self.get_param_position(i)
    else:
      return self.get_param_immediate(i)

  def get_param_position(self, i):
    return self.mem[self.mem[self.ip + i + 1]]

  def get_param_immediate(self, i):
    return self.mem[self.ip + i + 1]

  def add_instr(self):
    operand1 = self.get_param(0)
    operand2 = self.get_param(1)
    dest = self.get_param_immediate(2)
    self.mem[dest] = operand1 + operand2
    self.ip += 4
    return self.mem

  def mult_instr(self):
    operand1 = self.get_param(0)
    operand2 = self.get_param(1)
    dest = self.get_param_immediate(2)
    self.mem[dest] = operand1 * operand2
    self.ip += 4
    return self.mem

  def in_instr(self):
    dest = self.get_param_immediate(0)
    self.mem[dest] = self.input.pop()
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
    dest = self.get_param_immediate(2)
    if operand1 < operand2:
      self.mem[dest] = 1
    else:
      self.mem[dest] = 0
    self.ip += 4
    return self.mem

  def equals_instr(self):
    operand1 = self.get_param(0)
    operand2 = self.get_param(1)
    dest = self.get_param_immediate(2)
    if operand1 == operand2:
      self.mem[dest] = 1
    else:
      self.mem[dest] = 0
    self.ip += 4
    return self.mem

  def halt_instr(self):
    self.halted = True
    self.ip += 1
    return self.mem


def get_amplitude(phase, amp_input, cpu):
  cpu.input.insert(0, phase)
  cpu.input.insert(0, amp_input)
  cpu.run()
  return cpu.output[0]


def test_phase_sequence(seq, controller_program):
  out = 0
  for setting in seq:
    cpu = IntcodeComputer()
    cpu.load_program(controller_program)
    out = get_amplitude(setting, out, cpu)
  return out


def test_phase_sequence_with_feedback(seq, controller_program):
  cpu = [0, 0, 0, 0, 0]
  current_cpu = 0

  def glue():
    nonlocal current_cpu
    out = cpu[current_cpu].output[-1]
    current_cpu = current_cpu + 1 if current_cpu + 1 < len(cpu) else 0
    cpu[current_cpu].input.insert(0, out)
    cpu[current_cpu].run()

  for i in range(5):
    cpu[i] = IntcodeComputer()
    cpu[i].load_program(controller_program)
    cpu[i].interrupt_handler = glue
    cpu[i].input.insert(0, seq[i])

  cpu[0].input.insert(0, 0)
  cpu[0].run()

  return cpu[-1].output[-1]


def solve_pt1():
  controller_program = "3,8,1001,8,10,8,105,1,0,0,21,34,43,64,85,98,179,260,341,422,99999,3,9,1001,9,3,9,102,3,9,9,4,9,99,3,9,102,5,9,9,4,9,99,3,9,1001,9,2,9,1002,9,4,9,1001,9,3,9,1002,9,4,9,4,9,99,3,9,1001,9,3,9,102,3,9,9,101,4,9,9,102,3,9,9,4,9,99,3,9,101,2,9,9,1002,9,3,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,99"
  best_seq = []
  best_result = 0
  for a in range(5):
    for b in range(5):
      for c in range(5):
        for d in range(5):
          for e in range(5):
            seq = [a, b, c, d, e]
            if len(set(seq)) == len(seq):
              result = test_phase_sequence(seq, controller_program)
              if result > best_result:
                best_seq = seq
                best_result = result
  print(best_result)


def solve_pt2():
  controller_program = "3,8,1001,8,10,8,105,1,0,0,21,34,43,64,85,98,179,260,341,422,99999,3,9,1001,9,3,9,102,3,9,9,4,9,99,3,9,102,5,9,9,4,9,99,3,9,1001,9,2,9,1002,9,4,9,1001,9,3,9,1002,9,4,9,4,9,99,3,9,1001,9,3,9,102,3,9,9,101,4,9,9,102,3,9,9,4,9,99,3,9,101,2,9,9,1002,9,3,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,99"
  best_seq = []
  best_result = 0
  for a in range(5, 10):
    for b in range(5, 10):
      for c in range(5, 10):
        for d in range(5, 10):
          for e in range(5, 10):
            seq = [a, b, c, d, e]
            if len(set(seq)) == len(seq):
              result = test_phase_sequence_with_feedback(seq, controller_program)
              if result > best_result:
                best_seq = seq
                best_result = result
  print(best_result)


if __name__ == "__main__":
  doctest.testmod()
  solve_pt1()
  solve_pt2()
