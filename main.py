import os
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
  return Runner(f, pid)

def run_population(toolbox, pop):

  # Evaluate the entire population
  #fitnesses = map(toolbox.evaluate, pop)

  value_pop = eval_solution(pop)
  print value_pop

  print_pop(pop, 1)
  # for g in range(config.NGEN):
  #
  #   # Clone the selected individuals
  #   offspring = map(toolbox.clone, pop)
  #
  #   # # Apply crossover and mutation on the offspring
  #   # for child1, child2 in zip(offspring[::2], offspring[1::2]):
  #   #   if random.random() < CXPB:
  #   #     toolbox.mate(child1, child2)
  #   #     del child1.fitness.values
  #   #     del child2.fitness.values
  #   #
  #   # for mutant in offspring:
  #   #   if random.random() < MUTPB:
  #   #     toolbox.mutate(mutant)
  #   #     del mutant.fitness.values
  #
  #   # Evaluate the individuals with an invalid fitness
  #   invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
  #   fitnesses = map(toolbox.evaluate, invalid_ind)
  #   for ind, fit in zip(invalid_ind, fitnesses):
  #     ind.fitness.values = fit
  #
  #   # The population is entirely replaced by the offspring
  #   pop[:] = offspring
  #
  # return pop


def create_subdir(pid):
  try:
    os.mkdir("gen/%s/" % pid)
    os.mkdir("gen/%s/puzzles" % pid)
  except Exception as e:
    print e


def main():
  pid = os.getpid()
  create_subdir(pid)
  runner = load_population(pid)
  runner(verbose=True)


if __name__ == '__main__':
  main()