import random
import copy
import matplotlib.pyplot as plt
import numpy
import array
from deap import base
from deap import creator
from deap import tools

from eval import eval_solution

class HoldLine(object):

  def __init__(self, f, arr):
    self.content, self.position = f(arr)
  def __getitem__(self, item):
    return copy.copy(self.content[item])
  def __setitem__(self, key, value):
    self.content[key] = value


class Puzzle(object):
  """
  Represant the game. Contain a population of each and get One fitnessValue.
  """

  def generate_graph_values(self, ngen=0):  # , size_avgs):
    nrow = [0, None, -1.0, 1.0]
    #[-100, -75, -50, -25, 0, 25, 50, 75, 100]

    fitnesses = self.get_other_values()
    y = 0
    for x in fitnesses:
      plt.scatter(y, x, marker='.', c='c')
      y += 1
    plt.axis(nrow)
    plt.ylabel("weight")
    plt.xlabel("population")
    plt.gcf().set_size_inches(15, 5)
    plt.savefig("gen/puzzles/p_%s_g_%s.png" % (self.uid, ngen), bbox_inches='tight', dpi=100)
    plt.clf()
    plt.close()

  def randomize_lines(self):
    for x in xrange(0, 256):
      l = random.randrange(0, len(self.lines))
      yield self.lines.pop(l)

  def gen_ind(self, arr):
    c = arr[self.create_index]
    self.create_index += 1
    return c, self.create_index

  def __init__(self, f):
    uid, lines = f()
    self.lines = copy.copy(lines)
    self.uid = uid

    self.toolbox = base.Toolbox()
    # Used by creator.Individual
    self.create_index = 0

    creator.create("WeightMax", base.Fitness, weights=(-1.0,))
    creator.create("Individual", HoldLine, weight=creator.WeightMax)

    #Should be Optimized to put corner at the corner etc...
    arr = [[int(l) for l in line.split()] for line in self.randomize_lines()]
    self.toolbox.register("individual", creator.Individual, self.gen_ind, arr) # , arr)
    self.toolbox.register("desk", tools.initRepeat, list, self.toolbox.individual)
    self.population = self.toolbox.desk(n=len(arr)) # numpy.array(arr, dtype=list, order="F")

    # toolbox.register("mate", tools.cxTwoPoint)
    # Using this muttation for now. May change for ourself.
    # self.toolbox.register("mutate", lambda x, **kwargs: x.mutate(**kwargs), indpb=0.4)
    # toolbox.register("select", tools.selTournament, tournsize=3)
    # self.toolbox.register("evaluate", lambda pop: pop.evaluate())

    #
    self.stats = tools.Statistics(key=lambda ind: ind.weight.value)
    self.stats.register("avg", numpy.mean)
    self.stats.register("std", numpy.std)
    self.stats.register("min", numpy.min)
    self.stats.register("max", numpy.max)
    self.logbook = tools.Logbook()
    self.logbook.header = "generation", "fitness", "min", "avg", "max"

  def __len__(self):
    return len(self.content)

  # def __getitem__(self, item):
  #   return copy.copy(self.population[item])
  # def __setitem__(self, key, value):
  #   self.population[key] = value

  def __repr__(self):
    return repr(self.values)

  def get_other_values(self):
    return self.values

  def evaluate(self, eval=0):
    self.values, n = eval_solution(self.population)
    for ind, v in zip(self.population, self.values):
      ind.weight.value = v
    record = self.stats.compile(self.population)
    self.logbook.record(eval=eval, population=self.population, **record)
    return n,

  def _get_mins_weight_pop(self, n, bad_pop):
    """
      Select n element in bad pop
    :param bad_pop:
    :return:
    """
    ret = []
    for i in range(0, n):
      index = random.randrange(0, len(bad_pop))
      ret.append(bad_pop.pop(index))
    return ret

  def get_mins_weight(self, n):
    """
      Take Random Min Weight
    :param n:
    :return:
    """
    #pop = copy.copy(self.population)
    e = min(self.population, key=lambda x: x.weight.value)
    bad_pop = [x for x in self.population if x.weight.value == e.weight.value]
    if len(bad_pop) > n:
      bad_pop = self._get_mins_weight_pop(n, bad_pop)
    elif len(bad_pop) < n:
      print "Not Enough Bad weigth going for the next bad weight"
      exit(0)
    #self.population = [ind for ind in self.population if ind not in bad_pop]
    for ind in bad_pop:
      ind.weight.value = None
    return bad_pop

  def set_new_position(self, elems, pos):
    for elem in elems:
      c = random.randrange(0, len(pos))
      elem.position = pos[c]
      pos.pop(c)

  def select(self, nselect=30):
    """
      This fonction should select X Individual that have the worst weight/Fitness
      They should be selected to be reset at different position
    :return:
    """
    missing_element = self.get_mins_weight(40)
    pos = [x.position for x in missing_element]
    for x in missing_element: x.position = -1
    self.set_new_position(missing_element, pos)


  def mutate(self, indpb=0.0):
    """
    Based on deap.tools.mutShuffleIndexes
      Adjusting it for our own process.


    deap.tools.mutShuffleIndexes Documentation:
    Shuffle the attributes of the input individual and return the mutant.
    The *individual* is expected to be a :term:`sequence`. The *indpb* argument is the
    probability of each attribute to be moved. Usually this mutation is applied on
    vector of indices.

    :param individual: Individual to be mutated.
    :param indpb: Independent probability for each attribute to be exchanged to
                 another position.
    :returns: A tuple of one individual.

    This function uses the :func:`~random.random` and :func:`~random.randint`
    functions from the python base :mod:`random` module.

    :return:
    """
    size = len(self.population)
    for i in xrange(size):
      if random.random() < indpb:
        swap_indx = random.randint(0, size - 2)
        if swap_indx >= i:
          swap_indx += 1
        self.population[i], self.population[swap_indx] = \
          self.population[swap_indx], self.population[i]
