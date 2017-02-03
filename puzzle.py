import getpass
import random
import copy
import string
import numpy
import os
from deap import base
from deap import creator
from deap import tools

import graphs
import config
import ind
import eternity
# Not use for now but for easier read i guess all eval code should go there.
import eval
import stats

# Coins Hautgauche, Hautdroit, basGauche, basDroit

CORNER_POS = [0, 15, 240, 255]
# Mask des coins Hautgauche, Hautdroit, basGauche, basDroit
MASK_CORNERS = [[0, None, None, 0], [0, 0, None, None], [None, None, 0, 0], [None, 0, 0, None]]
BORDER_TOP = range(1, 15)
BORDER_BOT = range(241, 255)
BODER_LEFT = [31, 47, 63, 79, 95, 111, 127, 143, 159, 175, 191, 207, 223, 239]
BORDER_RIGHT = [16, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224]
# Tout les position de X pour les Bords
BORDER_POS = BORDER_TOP + BORDER_BOT + BODER_LEFT + BORDER_RIGHT
# Represent les mask des Bordures
MASK_TOP = [0, None, None, None]
MASK_BOT = [None, None, 0, None]
MASK_LEFT = [None, 0, None, None]
MASK_RIGHT = [None, None, None, 0]
# Toutes les positions de X en dehors des coins et des bords
INSIDE_POS = [x for x in range(0, 255) if x not in CORNER_POS and x not in BORDER_POS]

class Puzzle(object):
  """
  Represant the game. Contain a population of each and get One fitnessValue.
  """
  # Constructor
  def __init__(self, lines):
    seed = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    user = getpass.getuser()
    self.personal_path = "gen/%s_%s/" % (user, seed)
    create_subdir(self.personal_path)
    self.index_line = 0
    print "Personal Path used for this Puzzle: %s" % self.personal_path

    self.completion = 0.0 # current puzzle completion in percentage

    self.toolbox = base.Toolbox()
    # Creation des deux valeurs
    creator.create("FitnessInd", base.Fitness, weights=(1,))
    creator.create("FitnessGroup", base.Fitness, weights=(1,))
    # Individu creation
    creator.create("Individual", ind.Ind, fitness_ind=creator.FitnessInd, fitness_group=creator.FitnessGroup)

    # Pseudo random. put corners at corners and border at border
    arr = list(self.randomize_lines(*lines))

    self.toolbox.register("new_individual", creator.Individual, self._get_line_, arr)
    self.toolbox.register("desk", tools.initRepeat, list, self.toolbox.new_individual)
    self.population = self.toolbox.desk(n=len(arr))
    # Applying rotation until it's the right side
    self.fixing_outside()
    # Init the stats we want to log
    self.stats = stats.Stats(self.personal_path)
    self.evaluate()
    self.log_stats(-1, 0)

  # Stats Function
  def log_stats(self, generation, n_mutated):
    """
    Do that at each iteration.
    :param generation:
    :param n_mutated:
    :return:
    """
    self.stats.log_stats(generation, copy.deepcopy(self.population), n_mutated, self.completion)

  def write_stats(self):
    """
    You can do that once you finished the main loop
    :return:
    """
    self.stats.write_logbook()
    self.stats.write_logbook(bin=True)
  # End Stats Function

  def mutate_rotation(self, ind):
    for x in range(random.randint(1, 3)):
      ind.rotate()

  def mutate_position(self, ind):
    current = self.population.index(ind)
    other = random.randint(0, 255)
    while (current == other):
      other = random.randint(0, 255)
    self.population[current], self.population[other] = self.population[other], self.population[current]

  def choose_mutation(self, ind):
    if (random.randint(0, 100) <= 50):
#      print "MUTATION POSITION"
      self.mutate_position(ind)
      return 1
    else:
#      print "MUTATION ROTATION"
      self.mutate_position(ind)
      return 2

  def mutate(self):
    mutation_counter = 0
    # CONST RAND RATE <!> TO UPDATE WHEN RAND RATE IMPLEMENTED
    rand_rate = config.mutate_inpd
    rand = 0.00
    for ind in self.population:
      rand = random.uniform(0.000, 100.000)
      if (rand <= rand_rate):
        mutation_counter += 1
        operation = self.choose_mutation(ind)
        if (random.uniform(0.000, 100.000) <= rand_rate):
          if (operation == 1):
            self.mutate_position(ind)
          else:
            self.mutate_rotation(ind)
    return mutation_counter

  def evaluate(self):
    """

    :return:
    """
    # individuals, individual's clusters, and puzzle completion evaluations
    individuals_s, individuals_clusters_s, puzzle_completion = eval.eval_solution(self.population)

    # print "individuals evaluation:"
    # for index in range(0, 16):
    #   print individuals_s[index * 16: (index * 16) + 16]
    # print

    # print "individuals clusters evaluation:"
    # for index in range(0, 16):
    #   print individuals_clusters_s[index * 16: (index * 16) + 16]
    # print

    # print "puzzle completion:", puzzle_completion, "%\n"

    self.completion = puzzle_completion
    for individual, individual_s, cluster_s in zip(self.population, individuals_s, individuals_clusters_s):
      individual.fitness_ind.values = individual_s,
      individual.fitness_group.values = cluster_s,

  def select(self):
    removed_tils = []
    selection_ind_value = min(self.population, key=lambda k:k.fitness_group.values).fitness_group.values
    # Get nb tils to remove
    nb_to_remove = (100.0 - config.elitism_percentage) * 256.0 / 100.0
    # Select algorithm
    while nb_to_remove > 0:
      for i, ind in enumerate(self.population):
        if nb_to_remove > 0 and i > 0 and ind is not None and ind.fitness_group.values == selection_ind_value:
          self.population[i] = None
          removed_tils.append(ind)
          nb_to_remove -= 1
      selection_ind_value = (selection_ind_value[0] + config.selection_ind_value_step,)
    return removed_tils

  def crossover(self, removed_tils):
    # Get corners, borders and centers tils in removed_tils
    list_corner = [ind for ind in removed_tils if ind.count(0) == 2]
    list_border = [ind for ind in removed_tils if ind.count(0) == 1]
    list_center = [ind for ind in removed_tils if ind.count(0) == 0]
    # Set corners and borders
    random.shuffle(list_center)
    random.shuffle(list_border)
    random.shuffle(list_corner)
    # Random rotation on center pils
    for ind in list_center:
      ind.rotates(random.randint(0, 4))
    for i, ind in enumerate(self.population):
      if ind is None:
        if i in CORNER_POS:
          self.population[i] = list_corner.pop()
        elif i in BORDER_POS:
          self.population[i] = list_border.pop()
        else:
          self.population[i] = list_center.pop(random.randrange(len(list_center)))
    # Applying rotation until it's the right side
    self.fixing_outside()

  #####################
  #  Tools function   #
  #####################
  def fixing_outside(self):
    for index, mask in zip(CORNER_POS, MASK_CORNERS):
      self.fit_to_border(self.population[index], mask)
    for index in BORDER_BOT:
      self.fit_to_border(self.population[index], MASK_BOT)
    for index in BORDER_TOP:
      self.fit_to_border(self.population[index], MASK_TOP)
    for index in BODER_LEFT:
      self.fit_to_border(self.population[index], MASK_LEFT)
    for index in BORDER_RIGHT:
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
    lc = self.give_random_pos(copy.copy(CORNER_POS), lc)
    lb = self.give_random_pos(copy.copy(BORDER_POS), lb)
    li = self.give_random_pos(copy.copy(INSIDE_POS), li)
    l = lc + lb + li
    f = lambda lst, index, c: lst[c][1] if lst[c][0] == index else f(lst, index, c + 1)
    for x in xrange(0, 256):
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
  puzzle.draw()
#  puzzle.save_picture()
