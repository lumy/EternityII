import numpy
import config
import pickle
from deap import tools

import graphs


class Stats(object):

  def __init__(self, personal_path):
    """
    We have to talk about it here and see what's we're looging and if we do us a math on it.
    :return:
    """
    self.personal_path = personal_path
    stats1 = tools.Statistics(key=lambda ind: ind.fitness_ind.values)
    stats2 = tools.Statistics(key=lambda ind: ind.fitness_group.values)
    self.stats = tools.MultiStatistics(individual_fitness=stats1, group_fitness=stats2)
    self.stats.register("avg", numpy.mean)
    self.stats.register("min", min)
    self.stats.register("max", max)
    self.logbook = tools.Logbook()
    # Use when Wrote to file or printed to screen
    self.logbook.header = "generations", "mutated", "individual_fitness", "group_fitness"
    self.logbook.chapters['individual_fitness'].header = "min", "avg", "max"
    self.logbook.chapters['group_fitness'].header = "min", "avg", "max"

  def log_stats(self, generation, population, n_mutated):
    """
      Stats to be logged:
        Generation : Represant the iteration you're on
        mutated : Represent the mutated population
        mutation_percent : Percentage of mutation
        fitness_ind : Fitness of all individue
        group_fitness : Fitness of all groups
        population : Population at this time.
        record: fitness_ind and fitness_group compiled by stats. (min max avg)
    :param generation: The current iteration you're on
    :param population: The current population you're using
    :param n_mutated: The number of mutated element.
    :return:
    """
    record = self.stats.compile(population)
    self.logbook.record(generations=generation, mutated=n_mutated, mutation_percent=config.mutate_inpd,
                        population=population, **record)
    # I case we need to keep famous big scores.
    # self.famous.update(self.pop)

  def write_logbook(self, bin=False):
    """
      The binary mode save All the data, so if you want create Graph you need to have a pckl Log book as much as
      you need a txt one to read fast information.
    :param bin:
    :return:
    """
    if not bin:
      with open("%s/logbook.txt" % self.personal_path, "w") as f:
        f.write(str(self.logbook))
    else:
      pickle.dump(self.logbook, open("%s/logbook.pkl" % self.personal_path, "w"))

  def generate_graph_per_generations(self, saved=True, show=False):
    gen, all_inds, all_groups = self.logbook.select("generations", "individual_fitness", "group_fitness")
    for g, inds, groups in zip(gen, all_inds, all_groups):
       self._generate_graph_per_generation(g, inds, groups, saved=saved, show=show)

  def generate_stats_generations(self, ftype="avg", saved=True, show=False):
    gen = self.logbook.select("generations")
    all_inds = self.logbook.chapters["individual_fitness"].select(ftype)
    all_groups = self.logbook.chapters["group_fitness"].select(ftype)
    graphs.generate_graph_all_data(gen, all_inds, all_groups, saved, show, self.personal_path, ftype)

  def _generate_graph_per_generation(self, gen, inds, groups, saved=True, show=False):
    graphs.generate_graph_weight_population(gen, inds, groups, saved, show, self.personal_path)


def open_logboox(path):
  s = Stats("%s/logbook.pkl" % path)
  s.logbook = pickle.load(open("%s/logbook.pkl" % path, "r"))
  return s
