import numpy
from deap import base, tools
from deap import creator
from deap.tools import HallOfFame
import matplotlib.pyplot as plt
import config as CONFIG
from puzzle import Puzzle
import copy
import statistics

class Runner():

  def __init__(self, lines, pid,):
    self.toolbox = base.Toolbox()
    self.lc, self.lb, self.li = lines
    self.create_index = 0
    self.pid = pid

    creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
    creator.create("Puzzle", Puzzle, fitness=creator.FitnessMax)
    self.toolbox.register("puzzle", creator.Puzzle, self.get_args_lines_index)
    self.toolbox.register("population", tools.initRepeat, list, self.toolbox.puzzle)

    # toolbox.register("mate", tools.cxTwoPoint)
    # Using this muttation for now. May change for ourself.
    self.toolbox.register("mutate", lambda x, **kwargs: x.mutate(**kwargs), indpb=0.4)
    # toolbox.register("select", tools.selTournament, tournsize=3)
    self.toolbox.register("evaluate", lambda pop, eval: pop.evaluate(eval=eval))

    #
    self.stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    #stats_size = tools.Statistics(key=lambda ind: ind.get_other_values())
#    self.mstats = tools.MultiStatistics(fitness=stats_fit, content=stats_size)
    self.stats.register("avg", numpy.mean)
    self.stats.register("std", numpy.std)
    self.stats.register("min", min)
    self.stats.register("max", max)
    self.logbook = tools.Logbook()

    self.logbook.header = "eval", "select", "mutate", "fitness", "min", "avg", "max"

    maxsize = 10
    self.famous = HallOfFame(maxsize)

  def generate_graph(self, gen, fit_maxs, fit_avgs):
    # [-100, -75, -50, -25, 0, 25, 50, 75, 100]

    fig, ax1 = plt.subplots()
    line1 = ax1.plot(gen, fit_maxs, "b.", label="Maximum Fitness")
    ax1.set_xlabel("Evaluation")
    ax1.set_ylabel("Fitness", color="b")
    for tl in ax1.get_yticklabels():
      tl.set_color("b")

    ax2 = ax1.twinx()
    line2 = ax2.plot(gen, fit_avgs, "r.", label="Average Fitness")
    ax2.set_ylabel("Size", color="r")
    for tl in ax2.get_yticklabels():
      tl.set_color("r")

    lns = line1 + line2
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
               ncol=2, mode="expand", borderaxespad=0.)
    plt.savefig("gen/%s/puzles_fitness.png" % self.pid, bbox_inches='tight', dpi=100)
    plt.show()


  def get_args_lines_index(self):
    t = self.create_index
    self.create_index += 1
    return (t, (copy.copy(self.lc), copy.copy(self.lb), copy.copy(self.li)), self.pid)


  def get_population(self, verbose):
    pop = self.toolbox.population(n=CONFIG.NPOPULATION)
    # Evaluate the entire population
    self.eval(pop, verbose=True)
    return pop

  def eval(self, puzzles, eval=0, verbose=False):
    fitnesses = map(lambda x: self.toolbox.evaluate(x, eval=eval), puzzles, )
    for puzzle, fit in zip(puzzles, fitnesses):
      puzzle.fitness.values = fit
      if verbose:
        puzzle.generate_graph_values(ngen=eval)

  def __call__(self, *args, **kwargs):
    pop = self.get_population(kwargs.get("verbose", False))
    record = self.stats.compile(pop)
    self.logbook.record(eval=0, population=pop, **record)
    self.famous.update(pop)
    for i in range(1, kwargs.get("evals", CONFIG.NGEN)):

      for puzzle in pop:
        puzzle.select()
      self.eval(pop, eval=i, verbose=True)

      record = self.stats.compile(pop)
      self.logbook.record(eval=i, select=True, population=pop, **record)

      for ind in pop:
        #"""
        #  Think About the mutate method
        #"""
        self.toolbox.mutate(ind)

      #"""
      #    The crossover method should be taking Zone of big score (like 9 having a great score together and
      #       putting them at the same position in another puzzle. the ind of the puzzle that has been taking
      #       spaces should take the free new one randomly.
      #"""

      self.eval(pop, eval=i, verbose=True)

      record = self.stats.compile(pop)
      self.logbook.record(eval=i, mutate=True, population=pop, **record)
      self.famous.update(pop)

    print(self.logbook)
    gen = self.logbook.select("eval")
    self.logbook.header = "avg", "max"
    fit_max = self.logbook.select("max")
    fit_avg = self.logbook.select("avg")
    self.generate_graph(gen, fit_max, fit_avg)
    map(lambda x: x.writeLogbook(), pop)
    with open("gen/%s/logbook.txt" % self.pid, "w") as f:
      f.write(str(self.logbook))
    #logbook.chapters["content"].select("all")




