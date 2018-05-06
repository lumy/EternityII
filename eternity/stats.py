"""
  Statistics:
"""
import numpy, os, config, pickle
from deap import tools
import progressbar

def get_group_val(ind):
  return ind.fitness_group.values
def get_ind_val(ind):
  return ind.fitness_ind.values

class Stats(object):

  def __init__(self, personal_path):
    """
    We have to talk about it here and see what's we're looging and if we do us a math on it.
    :return:
    """
    self.personal_path = personal_path
    stats1 = tools.Statistics(key=get_ind_val)
    stats2 = tools.Statistics(key=get_group_val)
    self.stats = tools.MultiStatistics(individual_fitness=stats1, group_fitness=stats2)
    self.stats.register("avg", numpy.mean)
    self.stats.register("min", min)
    self.stats.register("max", max)
    self.init_book()

  def init_book(self):
    self.logbook = tools.Logbook()
    self.populations = []
    # Use when Wrote to file or printed to screen
    self.logbook.header = "generations", "nb_full_connected", "connections_completions", "score", "selected", "mutation_percent", "mutated", "individual_fitness", "group_fitness"
    self.logbook.chapters['individual_fitness'].header = "min", "avg", "max"
    self.logbook.chapters['group_fitness'].header = "min", "avg", "max"

  def log_stats(self, generation, population, selected, n_mutated, scores):
    """
      Stats to be logged:
        Generation : Represant the iteration you're on
        mutated : Represent the mutated population
        mutation_percent : Percentage of mutation
        fitness_ind : Fitness of all individue
        group_fitness : Fitness of all groups
        population : Population at this time.
        score : One score for the Puzzle
        record: fitness_ind and fitness_group compiled by stats. (min max avg)
    :param generation: The current iteration you're on
    :param population: The current population you're using
    :param n_mutated: The number of mutated element.
    :return:
    """
    record = self.stats.compile(population)
    self.populations.append(population)
    self.logbook.record(generations=generation, mutated=n_mutated, mutation_percent=config.mutate_inpd,
                        nb_full_connected=len([x for x in population if x.fitness_ind.values[0] == 4]),
                        connections_completions=scores[0], score=scores[1], selected=selected, **record)
    # I case we need to keep famous big scores.
    # self.famous.update(self.pop)

  def get_last_stats(self):
    return (self.logbook[-1], self.populations[-1])

  def write_logbook(self, bin=False):
    """
      The binary mode save All the data, so if you want create Graph you need to have a pckl Log book as much as
      you need a txt one to read fast information.
    :param bin:
    :return:
    """
    if not bin:
      with open("%s/logbook.txt" % self.personal_path, "w") as f:
        f.write("%s\n" % str(self.logbook))
    else:
      pickle.dump(self.logbook, open("%s/logbook.pkl" % self.personal_path, "w"))

  def write(self):
    self.write_logbook()
    self.write_logbook(bin=True)
    self.free_memory()

  def free_memory(self, write_stats=False, write_db=True):
    """
      Deprecated: to not break anything these should save into file or db by looking at config
    """
    # can't do that anymore, should be logged into db.
    #pickle.dump(self.populations, open("%s/populations.pkl" % self.personal_path, "a"))
  
    self.populations = []

  def generate_graph_per_generations(self, saved=True, show=False):
    gen, all_pop = self.logbook.select("generations"), self.populations
    try:
      os.mkdir("%s/graphs/" % self.personal_path)
    except Exception as e:
      print e
    pbar = progressbar.ProgressBar(widgets=[progressbar.Percentage(), progressbar.Bar()],
                                   maxval=len(self.populations)).start()
    for g, pop in zip(gen, all_pop):
      inds,groups = zip(*[(x.fitness_ind.values[0], x.fitness_group.values[0]) for x in pop])
      self._generate_graph_per_generation(g, inds, groups, saved=saved, show=show)
      pbar.update(g + 2)

  def _generate_graph_per_generation(self, gen, inds, groups, saved=True, show=False):
    raise NotImplemented
    # graphs.generate_graph_weight_population(gen, inds, groups, saved, show, "%s/graphs/" % self.personal_path)

  def generate_stats_generations(self, ftype="avg", saved=True, show=False):
    gen = self.logbook.select("generations")
    all_inds = self.logbook.chapters["individual_fitness"].select(ftype)
    all_groups = self.logbook.chapters["group_fitness"].select(ftype)
    graphs.generate_graph_all_data(gen, all_inds, all_groups, saved, show, self.personal_path, ftype)


  def draw_eternity(self, gen, inds, score):
    raise NotImplemented
#   eternity.save(inds, "%s/images/gen_%s_score_%s" % (self.personal_path, gen, score))

  def draw_all_eternity(self):
    gen, scores = self.logbook.select("generations", "score")
    try:
      os.mkdir("%s/images/" % self.personal_path)
    except Exception as e:
      print e
    pbar = progressbar.ProgressBar(widgets=[progressbar.Percentage(), progressbar.Bar()], maxval=len(self.populations)).start()
    for g, s, inds in zip(gen, scores, self.populations):
      self.draw_eternity(g, inds, s)
      pbar.update(g + 1)

def open_logboox(path):
  s = Stats("%s/logbook.pkl" % path)
  with open("%s/logbook.pkl" % path, "r") as f:
      s.logbook = pickle.load(f)
  s.populations = open_population(path)
  s.personal_path = path
  return s

def open_population(path):
  ret = []
  with open("%s/populations.pkl" % path, "r") as f:
    try:
      while True:
        ret.extend(pickle.load(f))
    except EOFError:
      pass
  return ret

__md__ = [
  "Stats",
  "open_logboox",
  "open_population"
]

__all__ = [
  "Stats",
  "open_logboox",
  "open_population"
]

if __name__ == '__main__':
  import puzzle, sys
  puzzle.Puzzle.dynamique_type()
  stats = open_logboox(sys.argv[1])
  cs, ss = stats.logbook.select("connections_completions", "score")
  for c, s in zip(cs, ss):
    print "C %s s %s c - s %s" % (c, s, c - s)

