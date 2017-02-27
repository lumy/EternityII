"""
  Main Module


  main file can be called as ```python main.py --help```
  Or ```python main.py -l [num_loop] -t [min_loop] --old-pop --timed```

  ```--loop|-l``` Number of loop maximum to do. if set to -1 it will not be \
  used to stop the loop(default: config.NGEN).

  ```--time|-t``` Maximum time to execute the loop in min, if not set will not \
  be used to stop the loop (default: None).

  ```--timed``` iteration and loop would be timed. (not really usefull).

  ```--old-pop|-o``` Load an old population. path is set in config file at \
  config.population_file_saved.
"""
import argparse
import os
import time
import datetime
import timed_loop
import dill
import ind
import puzzle
import config

# WINDOWS TROUBLE ><
os.environ['TCL_LIBRARY'] = "C:\\Python27\\tcl\\tcl8.5"
os.environ['TK_LIBRARY'] = "C:\\Python27\\tcl\\tk8.5"


def _load_file(path):
  """
    Use to load a Puzzle with dill.

  :param str path: path to the file to load
  :return: object (excepted [Puzzle](doc/puzzle.md) but no check is made)
  """
  try:
    with open(path, "rb") as e:
      puzzle.Puzzle.dynamique_type()
      return dill.load(e)
  except Exception as e:
    print "Exception while loading file %s" % path
    print e
    return None


def load_population(old_pop=False):
  """
    Load an old population or a new one. If old_pop is False, the new \
    population will be loaded from config.population_file_base.

  :param bool old_pop: loading the old population saved at \
  config.population_file_saved
  :return: A [Puzzle](doc/puzzle.md) object.
  """
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
    Save a given puzzle into the path config.population_file_saved.

  :param [puzzle](doc/puzzle.md): A [Puzzle](doc/puzzle.md) object.
  :return: None
  :throw Exception: Can throw classic exception around open and dill.dump
  """
  with open(config.population_file_saved, "wb") as f:
    dill.dump(puzzle, f)
  print "Saved @%s" % config.population_file_saved

def one_turn(puzzle, generation, write_stats):
  """
    Represent One iteration of the Algorithm.
    Ex.

    1. select
    2. crossover
    3. mutate
    4. evaluate
    5. log_stats

    More information at [Current Algorithm](doc/Algorithm.md)

  :param [puzzle](doc/puzzle.md): A [Puzzle](doc/puzzle.md) object.
  :param int generation: Iteration index.
  :param bool write_stats: Should we be logging stats. Used during benchmark, \
  otherwise always set to True.
  :return bool: solution as been found or Not.
  """
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
  if write_stats:
    # If you want log the different data
    puzzle.log_stats(generation, rm_tils, n_mutated)
  if puzzle.population[0].fitness_group.values[0] == config.score_group_max:
    return True
  return False


def loop(puzzle, write_stats, nloop=None, timer=None):
  """
    This function loop with stopping conditions as set in params. Write the \
    logbook at the end of the run.

  :param [puzzle](doc/puzzle.md): A [puzzle](doc/puzzle.md) object.
  :param bool write_stats: Should we be logging stats. Used during benchmark, \
  otherwise always set to True.
  :param int nloop: Number of loop to do, if -1 will not be used to stop the \
  loop.
  :param float timer: Minute to turn the loop if None will not be used to stop \
  loop.

  :return bool: is the solution has been found or not
  """
  end_time = None
  iteration = 0
  if timer:
    end_time = time.time() + datetime.timedelta(minutes=timer).total_seconds()

  while (nloop == -1 or iteration < nloop) and (end_time is None or time.time() < end_time):

    if one_turn(puzzle, iteration, write_stats):
      if write_stats:
        puzzle.write_stats()
      return True
    if iteration % 500 == 0 and iteration != 0:
      # Write the populations to a file to free some memory
      puzzle.stats.free_memory()
    iteration += 1

  if write_stats:
    puzzle.write_stats()
    save_population(puzzle)
  return False

def main(write_stats, old_pop=False, timer=None, nloop=None, timed=False):
  """
    main function will load a new population or an old one and run it with our \
    [Current Algorithm](doc/Algorithm.md)

   :param bool write_stats: Should we be logging stats. Used during benchmark, \
  otherwise always set to True.
  :param bool old_pop: loading the old population saved at \
  config.population_file_saved
  :param float timer: see [loop](doc/main.md#loop)
  :param int nloop: see [loop](doc/main.md#loop)
  :param timed: that will activate some timer, to calculate how many time for one iteration and for the whole iteration.
  """
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
  """
    Function to Set and Parse args with argparse.

  :return: object
  """
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

__md__ = [ # Order of appearance in the documentation
  'main',
  'loop',
  'one_turn',
  'get_args',
  'save_population',
  'load_population',
  '_load_file'
]
__all__ = [
  'main',
  'loop',
  'one_turn',
]