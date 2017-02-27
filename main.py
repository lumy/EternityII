import argparse
import os
import time
import datetime
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

def load_population(old_pop=False):
  if old_pop:
    f = _load_file(config.population_file_saved)
    if f != None:
      return f

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
  last_con = puzzle.stats.logbook.select("connections_completions")[-1]
  last_score = puzzle.stats.logbook.select("score")[-1]
  removed_tils = puzzle.select(generation, last_con, last_score)
  # Example of call
  rm_tils = len(removed_tils)
  puzzle.crossover(removed_tils)
  # Example of call
  n_mutated = puzzle.mutate()
  # Evaluate the entire population
  puzzle.evaluate()
  #if last_con > puzzle.connections_completions:
   # print "Score going down. Avoiding ? ", generation
    #puzzle.population = puzzle.stats.populations[-1]
    # if config.mutate_inpd == 0.0005:
    #   config.mutate_inpd = 0.05
  #  return
  if write_stats:
    # If you want log the different data
    puzzle.log_stats(generation, rm_tils, n_mutated)
  if puzzle.population[0].fitness_group.values[0] == config.score_group_max:
    return True
  return False


def loop(puzzle, write_stats, nloop=None, timer=None):
  """
  :param puzzle:
  :param write_stats:
  :param nloop: argparse set nloop to config.ngen if not set.
  :param time:
  :return:
  """
  end_time = None
  iteration = 0
  if timer:
    end_time = time.time() + datetime.timedelta(minutes=timer).total_seconds()
  while (nloop == -1 or iteration < nloop) and (end_time is None or time.time() < end_time):

    if one_turn(puzzle, iteration, write_stats):
      if write_stats:
        # Saving logbook
        puzzle.write_stats()
      return True
    if iteration % 500 == 0 and iteration != 0:
      # Write the populations to a file to free some memory
      puzzle.stats.free_memory()
    iteration += 1
  if write_stats:
    puzzle.write_stats()
    save_population(puzzle)

def main(write_stats, old_pop=False, timer=None, nloop=None, timed=False, input_grid=None):
  """
    main function will load a new population or an old one and run it.

  :param write_stats:
  :param old_pop:
  :param timer:
  :param nloop:
  :param timed: that will activate some timer, to calculate how many time for one iteration and for the whole iteration.
  :return:
  """
  if input_grid != None:
    config.population_file_base = input_grid
    config.init()
    import eval
    reload(eval)

  try:
    os.mkdir("./gen/")
  except Exception as e:
    pass
  puzzle = load_population(old_pop)
  if timed:
    timed_loop.timed_loop(puzzle, write_stats, (one_turn, save_population), timer=timer, nloop=nloop)
  else:
    loop(puzzle, write_stats, timer=timer, nloop=nloop)

def get_args():
  help="""Run a population with arguments and config file.
  """
  parser = argparse.ArgumentParser(description=help)
  parser.add_argument('--loop', '-l', action='store', default=config.NGEN,
                      help='Number of loop maximum to do. if set to -1 infinite loop (use time to stop) (default: config.NGEN %s)' % config.NGEN)
  parser.add_argument('--time', '-t', action='store', default=None,
                      help='Maximum time to execute the loop in min')
  parser.add_argument('--timed', action='store_true', default=False,
                      help='iteration and loop would be timed. benchmark.')
  parser.add_argument('--old-pop', '-o', action='store_true', default=False,
                      help='Load an old population. path is set in config file current is @%s.' % config.population_file_saved)
  args = parser.parse_args()
  return args

if __name__ == '__main__':
  kwargs = get_args()
  main(True, old_pop=kwargs.old_pop, timed=kwargs.timed,
       timer=None if kwargs.time is None else float(kwargs.time),
       nloop=int(kwargs.loop))
