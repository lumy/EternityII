import os
import timed_loop
import dill
import ind
import puzzle

# WINDOWS TROUBLE ><
os.environ['TCL_LIBRARY'] = "C:\\Python27\\tcl\\tcl8.5"
os.environ['TK_LIBRARY'] = "C:\\Python27\\tcl\\tk8.5"

import config

def _load_file(s):
  try:
    with open(s, "rb") as e:
      puzzle.Puzzle.dynamique_type()
      return dill.load(e)
  except Exception as e:
    print "Exception while loading file %s" % s
    print e
    return None

def load_population():

  f = _load_file(config.population_file_saved)
  if f != None:
    return f

  # Loading a basic Population with a runner
  inds = ind.get_population()
  corner = [i for i in inds if i[1].count(0) == 2]
  border = [i for i in inds if i[1].count(0) == 1]
  inside = [i for i in inds if i[1].count(0) == 0]
  return puzzle.Puzzle((corner, border, inside))


def save_population(puzzle):
  """
  Should we be using personal path ?
  :param puzzle:
  :return:
  """
  with open(config.population_file_saved, "wb") as f:
    dill.dump(puzzle, f)
  print "Saved @%s" % config.population_file_saved

def one_turn(puzzle, generation, write_stats):
  # Example of call
  removed_tils = puzzle.select(generation)
  # Example of call
  puzzle.crossover(removed_tils)
  # Example of call
  n_mutated = puzzle.mutate()
  # Evaluate the entire population
  puzzle.evaluate()
  if write_stats:
    # If you want log the different data
    puzzle.log_stats(generation, n_mutated)
  if puzzle.population[0].fitness_group.values[0] == config.score_group_max:
    return True
  return False

def _loop(puzzle, write_stats):
  """
    We Assume that the population is new an just setup and need to be eval first
  :param args:
  :param kwargs:
  :return:
  """
  for i in range(0, config.NGEN):
    if one_turn(puzzle, i, write_stats):
      return True
  if i % 500 == 0 and i != 0:
    # Write the populations to a file to free some memory
    puzzle.stats.free_memory()
  return False

def loop(puzzle, write_stats):
  s = _loop(puzzle, write_stats)
  if s:
    print "Solution Found !"
  else:
    print "No Solution Look at the logbook."
  if write_stats:
    puzzle.write_stats()
    save_population(puzzle)
  # END LOOP

def main(write_stats, timed=False):
  try:
    os.mkdir("./gen/")
  except Exception as e:
    print e
  puzzle = load_population()
  if timed:
    timed_loop.timed_loop(puzzle, one_turn)
  else:
    loop(puzzle, write_stats)

if __name__ == '__main__':
  timed = False
  main(True, timed=timed)
