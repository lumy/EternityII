"""
  Main Module: in binary usage


  main file can be called as ```python main.py --help```
  Or ```python main.py -l [num_loop] -t [min_loop] --old-pop --timed```

  ```--loop|-l``` Number of loop maximum to do. if set to -1 it will not be \
  used to stop the loop(default: config.NGEN).

  ```--time|-t``` Maximum time to execute the loop in min, if not set will not \
  be used to stop the loop (default: None).

  ```--timed``` iteration and loop would be timed. (not really usefull). # Deprecated

  ```--old-pop|-o``` Load an old population. path is set in config file at \
  config.population_file_saved.
"""
import argparse
import os
import time
import datetime
import dill
import ind
import puzzle
import config
import algo

def main(write_stats, old_pop=False, timer=None, nloop=None, timed=False, input_grid=None):
  """
    main function will load a new population or an old one and run it.

 :param bool write_stats: Should we be logging stats. Used during benchmark, \
  otherwise always set to True.
  :param bool old_pop: loading the old population saved at \
  config.population_file_saved
  :param float timer: see [loop](doc/main.md#loop)
  :param int nloop: see [loop](doc/main.md#loop)
  :param timed: that will activate some timer, to calculate how many time for one iteration and for the whole iteration.
  :param str input_grid: path to the text file to load
  :return:
  """
  try:
    os.mkdir("./gen/")
  except Exception as e:
    pass
  puzzle = algo.load_population(old_pop)
  algo.loop(puzzle, write_stats, timer=timer, nloop=nloop)

def get_args():
  """
    Function to Set and Parse args with argparse.

  :return: object
  """
  help="""Run a population with arguments and config file.
  """
  parser = argparse.ArgumentParser(description=help)
  parser.add_argument('--loop', '-l', action='store', default=config.NGEN, type=int,
                      help='Number of loop maximum to do. if set to -1 infinite loop (use time to stop) (default: config.NGEN %s)' % config.NGEN)
  parser.add_argument('--time', '-t', action='store', default=None, type=float,
                      help='Maximum time to execute the loop in min')
  parser.add_argument('--old-pop', '-o', action='store_true', default=False,
                      help='Load an old population. path is set in config file current is @%s.' % config.population_file_saved)
  args = parser.parse_args()
  return args

if __name__ == '__main__':
  kwargs = get_args()
  main(True, old_pop=kwargs.old_pop, timer=kwargs.time, nloop=kwargs.loop)

__md__ = [ # Order of appearance in the documentation
  'main',
  'get_args',
]
__all__ = [
  'main',
]
