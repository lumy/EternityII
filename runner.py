from deap import base, tools
from deap import creator
from deap.tools import HallOfFame
import matplotlib.pyplot as plt

import config
import config as CONFIG
import eternity
from puzzle import Puzzle
import copy

class Runner():

  def __init__(self, lines, pid,):
    self.toolbox = base.Toolbox()
    self.lc, self.lb, self.li = lines
    self.puzzle_id = 0
    self.pid = pid

    creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
    creator.create("Puzzle", Puzzle, fitness=creator.FitnessMax)
    self.toolbox.register("puzzle", creator.Puzzle, self.get_args_lines_index)
    self.toolbox.register("population", tools.initRepeat, list, self.toolbox.puzzle)

    # toolbox.register("mate", tools.cxTwoPoint)
    # toolbox.register("select", tools.selTournament, tournsize=3)
    self.toolbox.register("evaluate", lambda pop, eval: pop.evaluate(eval=eval))

    #
    self.stats = tools.Statistics(key=lambda ind: ind.fitness.values)
#    self.stats.register("min", min)
#    self.stats.register("max", max)
    self.logbook = tools.Logbook()
    self.logbook.header = "eval", "population", "fitnesses"

    maxsize = 10
    self.famous = HallOfFame(maxsize)

  def generate_graph(self, gen, fitnesses):
    # [-100, -75, -50, -25, 0, 25, 50, 75, 100]
    nrow = [0, None, -100.0, 100.0]
    #[-100, -75, -50, -25, 0, 25, 50, 75, 100]
    y = 0
    print gen, fitnesses
    for x in fitnesses:
      for _x in x:
        plt.scatter(y, _x, marker='.', c='c')
      y += 1
    plt.axis(nrow)
    plt.ylabel("weight")
    plt.xlabel("gen")
    plt.gcf().set_size_inches(15, 5)
    plt.savefig("gen/%s/puzles_fitness.png" % self.pid, bbox_inches='tight', dpi=100)
    plt.show()
    plt.clf()
    plt.close()


  def get_args_lines_index(self):
    t = self.puzzle_id
    self.puzzle_id += 1
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
    return fitnesses

  def crossover(self):
    """
       The crossover method could be taking Zone of big score (like 9 having a great score together and
          putting them at the same position in another puzzle. the ind of the puzzle that has been taking
          spaces should take the free new one randomly.
    """
    pass

  def __call__(self, *args, **kwargs):
    pop = self.get_population(kwargs.get("verbose", False))

    for i in range(0, kwargs.get("evals", CONFIG.NGEN)):

      # We May be Preselecting some puzzle to save and "Reproduce"

      for puzzle in pop:
        puzzle.save_picture(gen=i)
        puzzle.select()
        puzzle.mutate(config.mutate_inpd)
      self.crossover()
      fitnesses = self.eval(pop, eval=i, verbose=True)

      record = self.stats.compile(pop)
      self.logbook.record(eval=i, fitnesses=fitnesses, population=pop, **record)
      self.famous.update(pop)


    # Here log the interesting stats.

    gen = self.logbook.select("eval")
    #self.logbook.header = "population"
    fits = self.logbook.select("fitnesses")
    self.generate_graph(gen, fits)
    map(lambda x: x.writeLogbook(), pop)
    with open("gen/%s/logbook.txt" % self.pid, "w") as f:
      f.write(str(self.logbook))



