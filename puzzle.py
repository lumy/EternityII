import getpass
import random
import copy
import string
import numpy
import os
from deap import base
from deap import creator
from deap import tools
from datetime import datetime

import graphs
import config
import ind
import eternity
# Not use for now but for easier read i guess all eval code should go there.
import eval
import stats

# config.corner_pos = [0, 15, 240, 255]
# config.border_left_pos = [31, 47, 63, 79, 95, 111, 127, 143, 159, 175, 191, 207, 223, 239]
# config.border_right_pos = [16, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224]
# config.border_top_pos = range(1, 15)
# config.border_bot_pos = range(241, 255)
# config.inside_pos = [x for x in range(0, 255) if x not in config.corner_pos and x not in config.border_pos_pos]
# config.border_pos_pos = config.border_top_pos + config.border_bot_pos + config.border_left_pos + config.border_right_pos

# Coins Hautgauche, Hautdroit, basGauche, basDroit

# Mask des coins Hautgauche, Hautdroit, basGauche, basDroit
MASK_CORNERS = [[0, None, None, 0], [0, 0, None, None], [None, None, 0, 0], [None, 0, 0, None]]

# Tout les position de X pour les Bords
# Represent les mask des Bordures
MASK_TOP = [0, None, None, None]
MASK_BOT = [None, None, 0, None]
MASK_LEFT = [None, 0, None, None]
MASK_RIGHT = [None, None, None, 0]
# Toutes les positions de X en dehors des coins et des bords

class Puzzle(object):
  """
  Represant the game. Contain a population of each and get One fitnessValue.
  """
  @staticmethod
  def dynamique_type():
    # Creation des deux valeurs
    creator.create("FitnessInd", base.Fitness, weights=(1,))
    creator.create("FitnessGroup", base.Fitness, weights=(1,))
    # Individu creation
    creator.create("Individual", ind.Ind, fitness_ind=creator.FitnessInd, fitness_group=creator.FitnessGroup)


  # Constructor
  def __init__(self, lines):
    current_time = datetime.now().strftime("%d-%m-%Y_%Hh.%Mm.%Ss")
    user = getpass.getuser()
    self.personal_path = "gen/%s_%s/" % (user, current_time)
    create_subdir(self.personal_path)
    self.index_line = 0
    print "Personal Path used for this Puzzle: %s" % self.personal_path

    self.completion = 0.0 # current puzzle completion in percentage
    # Pseudo random. put corners at corners and border at border
    arr = list(self.randomize_lines(*lines))
    Puzzle.dynamique_type()
    self.toolbox = base.Toolbox()
    self.toolbox.register("new_individual", creator.Individual, self._get_line_, arr)
    self.toolbox.register("desk", tools.initRepeat, list, self.toolbox.new_individual)
    self.population = self.toolbox.desk(n=len(arr))
    # Applying rotation until it's the right side
    self.fixing_outside()
    # Init the stats we want to log
    self.stats = stats.Stats(self.personal_path)
    self.connections_completions = 0.0
    self.completion = 0.0
    self.evaluate()
    self.log_stats(-1, 0, 0)

  # Stats Function
  def log_stats(self, generation, rm_tils, n_mutated):
    """
    Do that at each iteration.
    :param generation:
    :param n_mutated:
    :return:
    """
    self.stats.log_stats(generation, copy.deepcopy(self.population), rm_tils, n_mutated, (self.connections_completions, self.completion))

    
  def write_stats(self):
    """
    You can do that once you finished the main loop
    :return:
    """
    self.stats.write()
  # End Stats Function

  def mutate_position(self, index, list_positions):
    """
      If only one position in the list position will return (could do but it would be an useless procs calls.
    :param index:
    :param list_positions:
    :return:
    """
    if len(list_positions) <= 1:
      return
    other = index
    while (index == other):
      other = random.randint(0, len(list_positions) - 1)
    self.population[index], self.population[list_positions[other]] = self.population[list_positions[other]], self.population[index]

  def _mutate(self, positions):
    mutated = 0
    for x in positions:
      if random.uniform(0, 1) <= config.mutate_inpd:
        mutated += 1
        operation = random.randint(1, 3)
        # operation == 1 mutate rotation # operation == 2 mutate position # operation == 3 mutate both
        if operation >= 2:
          self.mutate_position(x, positions)
          operation -= 2
        if operation >= 1:
          self.population[x].rotates(random.randint(1, 3))
    return mutated


  def mutate(self):
    mutation_counter = self._mutate(config.inside_pos)
    mutation_counter += self._mutate(config.border_pos)
    mutation_counter += self._mutate(config.corner_pos)
    self.fixing_outside()
    return mutation_counter

  def evaluate(self):
    """

    :return:
    """
    # individuals, individual's clusters, and puzzle completion evaluations
    individuals_s, individuals_clusters_s, puzzle_completion, connections_completion, nb_individuals_per_ind_score = eval.eval_solution(self.population)

    # print "individuals evaluation:"
    # for index in range(0, 16):
    #   print individuals_s[index * 16: (index * 16) + 16]
    # print

    # print "individuals clusters evaluation:"
    # for index in range(0, 16):
    #   print individuals_clusters_s[index * 16: (index * 16) + 16]
    # print

    # print "puzzle completion:", puzzle_completion, "%\n"
    self.connections_completions = connections_completion
    self.completion = puzzle_completion
    for individual, individual_s, cluster_s in zip(self.population, individuals_s, individuals_clusters_s):
      individual.fitness_ind.values = individual_s,
      individual.fitness_group.values = cluster_s,

  def select(self, generation, con_complt, score):
    """
      Remove all connection < 4 and group_value < average_group_value
    :param generation:
    :param average_ind_value:
    :param average_group_value:
    :return:
    """
    keep_tils = []
    def _get_neighs(current):
      x,y = current % config.size_line, current / config.size_line
      return ((eval.get_individual_neighbor(self.population, current, x, y, eval.NORTH), eval.NORTH, eval.SOUTH),
              (eval.get_individual_neighbor(self.population, current, x, y, eval.EAST), eval.EAST, eval.WEST),
              (eval.get_individual_neighbor(self.population, current, x, y, eval.SOUTH), eval.SOUTH, eval.NORTH),
              (eval.get_individual_neighbor(self.population, current, x, y, eval.WEST), eval.WEST, eval.EAST))
 
    def _select_ligth_(root, current):
      keep_tils.append(current)
      neighbors = _get_neighs(current)
      for neighs, ind_side, neigh_side in neighbors:
        neigh, n_index = neighs
        if neigh is not None and n_index not in keep_tils and \
          self.population[current][ind_side] == neigh[neigh_side]:
          _select_ligth_(root, n_index)

    def _select_heavy_(root, current, heavy):
      keep_tils.append(current)
      neighbors = _get_neighs(current)
      for neighs, ind_side, neigh_side in neighbors:
        neigh, n_index = neighs
        if neigh is not None and n_index not in keep_tils and \
          neigh.fitness_ind.values[0] >= heavy:
          _select_heavy_(root, n_index, heavy)

    diff = con_complt - score
    if  diff < config.select_light:
      _select_ligth_(0, 0)
    elif config.select_light <= diff <= config.select_medium:
      _select_heavy_(0, 0, 3)
    else:
      _select_heavy_(0, 0, 4)
    removed_tils = []
    for index in [i for i in range(0, config.total) if i not in keep_tils]:
      removed_tils.append(self.population[index])
      self.population[index] = None
    return removed_tils

  def get_mask(self, index):
    """
      return the Mask for a given index
    :param index: int index of population
    :return:
    """
    def _get_mask(dir, ldir):
      n, n_i = eval.get_individual_neighbor(self.population, index,
                                            index % config.size_line, index / config.size_line, dir)
      if n_i is None:
        return 0
      if n is None:
        return None
      return n[ldir]
    # [n, e, s, w]
    return [_get_mask(eval.NORTH, 2),_get_mask(eval.EAST, 3), _get_mask(eval.SOUTH, 0), _get_mask(eval.WEST, 1)]

  def set_individual_best_mask(self, ind, pos, mask):
    t = [ind._mask_(mask, c_index=0), ind._mask_(mask, c_index=1), ind._mask_(mask, c_index=2),
         ind._mask_(mask, c_index=3)]
    ind.rotates(t.index(max(t)))
    if self.population[pos] != None:
      raise IndexError("Can't set on a not None object")
    self.population[pos] = ind

  def roulette(self, elems, k):
    """
      Please have a look at https://github.com/DEAP/deap/blob/master/deap/tools/selection.py
      It's cleary inspired of the function selRoulette.
      Thanks to deap.
    :param elems:
    :param k:
    :return:
    """

    s_inds = sorted(elems, reverse=True)
    sum_fits = sum(elems)

    chosen = []
    for i in xrange(k):
      u = random.random() * sum_fits
      sum_ = 0
      for i, ind in enumerate(s_inds):
        sum_ += ind
        if sum_ > u:
          chosen.append(i)
          break
    return chosen

  def place_type(self, list_type, pos_type):
    """
        - get X positions valuable for now and put it at a random one.
        - Look for new free conncted position to add to the typelist
        - Place the next til
    :param list_type:
    :param pos_type:
    :return:
    """
    if len(list_type) == 0:
      return
    free_pos_type = [x for x in pos_type if  self.population[x] == None]
    mask_list = [self.get_mask(x) for x in free_pos_type]
    for pos in list_type:
      # Setting + 1 in the loop, because roulette function doesn't take value 0.
      val_free_pos = [1 + pos.best_value_of_mask(mask) for mask in mask_list]
      new_pos = self.roulette(val_free_pos, 1)[0]
      self.set_individual_best_mask(pos, free_pos_type.pop(new_pos), mask_list.pop(new_pos))

  def crossover(self, removed_tils):
    """
      - We shall first sort the removed_tils by type of tils (list_corner/border/center)
      - then we should look for every available connected position for a given type.
      - We should shuffle our lists
      - for each type of tils
        - get X positions valuable for now and put it at a random one.
        - Look for new free conncted position to add to the typelist
    :param removed_tils:
    :return:
    """
    # Get corners, borders and centers tils in removed_tils
    list_corner = [ind for ind in removed_tils if ind.count(0) == 2]
    list_border = [ind for ind in removed_tils if ind.count(0) == 1]
    list_center = [ind for ind in removed_tils if ind.count(0) == 0]
    # Set corners and borders
    random.shuffle(list_center)
    random.shuffle(list_border)
    random.shuffle(list_corner)
    # Placing every ind
    self.place_type(list_corner, config.corner_pos)
    self.place_type(list_border, config.border_pos)
    self.place_type(list_center, config.inside_pos)

    # In case of but we shouldn't need that.
    self.fixing_outside()

  #####################
  #  Tools function   #
  #####################
  def fixing_outside(self):
    for index, mask in zip(config.corner_pos, MASK_CORNERS):
      self.fit_to_border(self.population[index], mask)
    for index in config.border_bot_pos:
      self.fit_to_border(self.population[index], MASK_BOT)
    for index in config.border_top_pos:
      self.fit_to_border(self.population[index], MASK_TOP)
    for index in config.border_left_pos:
      self.fit_to_border(self.population[index], MASK_LEFT)
    for index in config.border_right_pos:
      self.fit_to_border(self.population[index], MASK_RIGHT)

  def fit_to_border(self, ind, type):
    """
      Rotate the pieces until it feet with the border.
    :param ind:
    :param type: list of None and 0 for direction to fit.
    :return:
    """
    while not ind.mask(type):
      ind.rotate()

  def give_random_pos(self, pos, line):
    r = []
    for x in range(0, len(pos)):
      rp =  random.randrange(0, len(pos))
      rl = random.randrange(0, len(line))
      r.append((pos.pop(rp),line.pop(rl)))
    return r

  def randomize_lines(self, lc, lb, li):
    """
      Trying to have an half randomize algorithm
    :return:
    """
    lc = self.give_random_pos(copy.copy(config.corner_pos), lc)
    lb = self.give_random_pos(copy.copy(config.border_pos), lb)
    li = self.give_random_pos(copy.copy(config.inside_pos), li)
    l = lc + lb + li
    f = lambda lst, index, c: lst[c][1] if lst[c][0] == index else f(lst, index, c + 1)
    for x in xrange(0, len(l)):
      yield f(l, x, 0)


  def __len__(self):
    return len(self.population)

  def __repr__(self):
    return repr(self.personal_path)

  def generate_graph_per_generations(self, saved=True, show=False):
    self.stats.generate_graph_per_generations(saved=saved, show=show)

  def generate_stats_generations(self, ftype="avg", saved=True, show=False):
    self.stats.generate_stats_generations(ftype=ftype, saved=saved, show=show)


  def _get_line_(self, arr):
    i = self.index_line
    self.index_line += 1
    return arr[i]

  def save_picture(self, gen=0, score=0):
    eternity.save(self.population, "%s/gen_%s_score_%s" % (self.personal_path, gen, score))

  def draw_generation(self, n):
    self.stats.draw_generation(n)

  def draw_all_generations(self):
    self.stats.draw_all_eternity()

def create_subdir(s):
  try:
    os.mkdir(s)
  except Exception as e:
    print e


if __name__ == '__main__':
  import ind
  inds = ind.get_population()
  corner = [i for i in inds if i[1].count(0) == 2]
  border = [i for i in inds if i[1].count(0) == 1]
  inside = [i for i in inds if i[1].count(0) == 0]
  puzzle = Puzzle((corner, border, inside))
 # puzzle.draw()
#  puzzle.save_picture()
