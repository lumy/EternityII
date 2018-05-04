"""
  puzzle module contain Puzzle object.

"""
import getpass
import random
import copy
import os
import config
import eval
import stats
from ind import Ind
from deap import base
from deap import creator
from deap import tools
from datetime import datetime

# Coins Hautgauche, Hautdroit, basGauche, basDroit

# Mask des coins Hautgauche, Hautdroit, basGauche, basDroit
MASK_CORNERS = [[0, None, None, 0], [0, 0, None, None], [None, None, 0, 0], [None, 0, 0, None]]

# Tout les position de X pour les Bords
# Represent les mask des Bordures
MASK_TOP = [0, None, None, None]
MASK_BOT = [None, None, 0, None]
MASK_LEFT = [None, 0, None, None]
MASK_RIGHT = [None, None, None, 0]

class Puzzle(object):
  """
    Puzzle represent a board game, it contain a population of \
    [Individuals](doc/ind.md)

  Puzzle Description:

  - self.personal_path: path where the stats are gonna be wrote.
  - self.completion: Completion of puzzle.
  - self.connections_completions: Connections completions.
  - self.toolbox: deap.toolbox
  - self.population: current population
  - self.stats: [Stats instance](doc/stats.md)
  """

  @staticmethod
  def dynamique_type():
    """
      Static Method. Create dynamique Type used by deap.
      This method needs to be called before any loading file.

      Create static type:

      - FitnessInd
      - FitnessGroup
      - Individual

      Can be found at ```deap.creator.FitnessInd``` or \
      ```deap.creator.Individual```
    """
    creator.create("FitnessInd", base.Fitness, weights=(1,))
    creator.create("FitnessGroup", base.Fitness, weights=(1,))
    creator.create("Individual", Ind, fitness_ind=creator.FitnessInd, fitness_group=creator.FitnessGroup)


  def __init__(self, lines):
    """
    :param lines: the lines in order from the file e2pieces.txt
    """
    current_time = datetime.now().strftime("%d-%m-%Y_%Hh.%Mm.%Ss")
    user = getpass.getuser()
    self.personal_path = "gen/%s_%s/" % (user, current_time)
    self.index_line = 0
    self.completion = 0.0
    self.connections_completions = 0.0

    try:
      os.mkdir(self.personal_path)
    except Exception as e:
      pass
    print "Personal Path used for this Puzzle: %s" % self.personal_path

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
    self.evaluate()
    self.log_stats(-1, 0, 0)

  # Stats Function
  def log_stats(self, generation, rm_tils, n_mutated):
    """
      Log statistics, do that at each iteration, more info [@stats file](doc/stats.md)

    :param int generation: Iteration Index.
    :param int rm_tils: Number of selected/replaced tils.
    :param int n_mutated: Number of mutated element at this iteration.
    :return:
    """
    self.stats.log_stats(generation, copy.deepcopy(self.population), rm_tils, n_mutated, (self.connections_completions, self.completion))

    
  def write_stats(self):
    """
      Write the stats. More info [@stats file](doc/stats.md).
    """
    self.stats.write()
  # End Stats Function

  def mutate_position(self, index, list_positions):
    """
      Change the position between index and a random pos from list_position.

    :param int index: The index that going to be mutated.
    :param list list_positions: list of int, all position possible to change.
    """
    if len(list_positions) <= 1:
      return
    other = index
    while (index == other):
      other = random.randint(0, len(list_positions) - 1)
    self.population[index], self.population[list_positions[other]] = \
        self.population[list_positions[other]], self.population[index]

  def _mutate(self, positions):
    """
      Goes through all positions given in parameters and apply a mutation. If \
      random.uniform(0, 1) <= config.mutate_inpd Do a mutation. Mutation can be \
      One of these 3 type: [mutate_position](#mutate_position) \
      [mutate_rotation](ind.md#rotates), mutation_position_rotation \
      (both at same time in this order).

    :param list positions: a list of position to go through.
    :return int: Number of mutated element.
    """
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
    """
      Apply mutation on every [positions type](doc/config.md#positions). call \
      [self.fixing_outside](#fixing_outside).

    :return int: Number of mutated element.
    """
    mutation_counter = self._mutate(config.inside_pos)
    mutation_counter += self._mutate(config.border_pos)
    mutation_counter += self._mutate(config.corner_pos)
    self.fixing_outside()
    return mutation_counter

  def evaluate(self):
    """
      Call the [evaluate function from eval module](doc/eval.md). set value for \
      ```self.connections_completions``` ```self.completion``` and for every \
      individuals fitnesses (ind and groups)
    """
    # individuals, individual's clusters, and puzzle completion evaluations
    individuals_s, individuals_clusters_s, puzzle_completion, connections_completion, nb_individuals_per_ind_score = eval.eval_solution(self.population)

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
      return the [mask](doc/mask.md) for a given index

    :param int index: index to extract [mask](doc/mask.md) of.
    :return list: [mask](doc/mask.md)
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
    """
      Doc
    """
    t = [ind._mask_(mask, c_index=0), ind._mask_(mask, c_index=1), ind._mask_(mask, c_index=2),
         ind._mask_(mask, c_index=3)]
    ind.rotates(t.index(max(t)))
    if self.population[pos] != None:
      raise IndexError("Can't set on a not None object")
    self.population[pos] = ind

  def roulette(self, elems, k):
    """
      Please have a look at [deap roulette function](https://github.com/DEAP/deap/blob/master/deap/tools/selection.py)
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

    :param list list_type: list of [ind](doc/ind.md)
    :param list pos_type: list of int
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

    :param list removed_tils: list of [ind](doc/ind.md)
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
    """
      Use to make match each corner/border to the right [mask](doc/mask.md).

      *Warning* This is an unsafe function, from few test, if the corner CAN'T
      fit the mask, (ex: mask [0,0,None,None] tils [0,1,2,3]) it will make an \
      infinite loop.
    """
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

      *Warning*: This can generate an infinite loop ! if ind can fit mask \
      because of missing 0 or because of number not present. Use carefully.

    :param [ind](doc/ind.md) ind:
    :param list type: list of None and int to fit.
    :return:
    """
    while not ind.mask(type):
      ind.rotate()

  # Init Functions
  def _get_line_(self, arr):
    """
      Docu
    """
    i = self.index_line
    self.index_line += 1
    return arr[i]

  def give_random_pos(self, pos, line):
    """
      Docu
    """
    r = []
    for x in range(0, len(pos)):
      rp =  random.randrange(0, len(pos))
      rl = random.randrange(0, len(line))
      r.append((pos.pop(rp),line.pop(rl)))
    return r

  def randomize_lines(self, lc, lb, li):
    """
      Used during init, if it's a new population then we place them by \
      [type](doc/ind.md#type) and randomly.

    :return: yield line organize but randomize.
    """
    lc = self.give_random_pos(copy.copy(config.corner_pos), lc)
    lb = self.give_random_pos(copy.copy(config.border_pos), lb)
    li = self.give_random_pos(copy.copy(config.inside_pos), li)
    l = lc + lb + li
    f = lambda lst, index, c: lst[c][1] if lst[c][0] == index else f(lst, index, c + 1)
    for x in xrange(0, len(l)):
      yield f(l, x, 0)
  # End Init Functions

  def generate_graph_per_generations(self, saved=True, show=False):
    """
      See [@stats file](doc/stats.md#generate_graph_per_generations)

    :param saved:
    :param show:
    """
    self.stats.generate_graph_per_generations(saved=saved, show=show)

  def generate_stats_generations(self, ftype="avg", saved=True, show=False):
    """
      See [@stats file](doc/stats.md#generate_stats_generations)

    :param ftype:
    :param saved:
    :param show:
    """
    self.stats.generate_stats_generations(ftype=ftype, saved=saved, show=show)


  def save_picture(self, gen=0, score=0):
    """
      See [@eternity file](doc/eternity.md#save)

    Deprecated
    :param gen:
    :param score:
    :return:
    """
    raise NotImplemented
#    eternity.save(self.population,
#                  "%s/gen_%s_score_%s" % (self.personal_path, gen, score))

  def draw_generation(self, n):
    """
      See [@stats file](doc/stats.md#draw_generation)

    :param n:
    :return:
    """
    self.stats.draw_generation(n)

  def draw_all_generations(self):
    """See [@stats file](doc/stats.md#draw_all_eternity)"""
    self.stats.draw_all_eternity()

  def __len__(self):
    """Len
    """
    return len(self.population)

  def __repr__(self):
    """repr
    """
    return repr(self.personal_path)


__md__ = [
  'Puzzle'
]
__all__ = [
  'Puzzle'
  ]

if __name__ == '__main__':
  import ind
  inds = ind.get_population()
  corner = [i for i in inds if i[1].count(0) == 2]
  border = [i for i in inds if i[1].count(0) == 1]
  inside = [i for i in inds if i[1].count(0) == 0]
  puzzle = Puzzle((corner, border, inside))
 # puzzle.draw()
#  puzzle.save_picture()
