import os

from puzzle import create_subdir

os.environ['TCL_LIBRARY'] = "C:\\Python27\\tcl\\tcl8.5"
os.environ['TK_LIBRARY'] = "C:\\Python27\\tcl\\tk8.5"

import config
from runner import Runner



def _load_file(s):
  try:
    with open(s) as e:
      return e.readlines()
  except Exception:
    return None

#   def if_then_else(input, output1, output2):
#     return output1 if input else output2
#
#
# pset = PrimitiveSetTyped("main", [bool, float], float)
# pset.addPrimitive(operator.xor, [bool, bool], bool)
# pset.addPrimitive(operator.mul, [float, float], float)
# pset.addPrimitive(if_then_else, [bool, float, float], float)
# pset.addTerminal(3.0, float)
# pset.addTerminal(1, bool)
# [ X Y W Z]
# N W S E
# 0 is a border

def print_pop(pop, elem=None):
  def print_row(row, _elem=None):
    def print_ind(ind):
      if ind.fitness.valid:
        print "N[%s]W[%s]S[%s]E[%s]-Fitness[%s]" % (ind[0], ind[1], ind[2], ind[3], ind.fitness)
      else:
        print "N[%s]W[%s]S[%s]E[%s]-Fitness[%s]" % (ind[0], ind[1], ind[2], ind[3], None)

    for elem in row:
      if _elem > 0 or _elem == None:
        print_ind(elem)
      if _elem != None:
        _elem -= 1
    return _elem

  temp = elem
  for row in pop:
    temp = print_row(row, _elem=temp)

def load_population(pid):
  f = _load_file(config.population_file_saved)
  if f != None:
    return f
  f = _load_file(config.population_file_base)
  f = [[int(y) for y in x.split()] for x in f]
  corner = [l for l in f if l.count(0) == 2]
  border = [l for l in f if l.count(0) == 1]
  inside = [l for l in f if l.count(0) == 0]
  return Runner((corner, border, inside), pid)




def main():
  pid = os.getpid()
  create_subdir("gen/%s/" % pid)
  create_subdir("gen/%s/puzzles" % pid)
  runner = load_population(pid)
  runner(verbose=True)


if __name__ == '__main__':
  main()