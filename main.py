import os
import ind
from puzzle import Puzzle

# WINDOWS TROUBLE ><
os.environ['TCL_LIBRARY'] = "C:\\Python27\\tcl\\tcl8.5"
os.environ['TK_LIBRARY'] = "C:\\Python27\\tcl\\tk8.5"

import config

def _load_file(s):
  try:
    with open(s) as e:
      return e.readlines()
  except Exception:
    return None

def load_population():

  f = _load_file(config.population_file_saved)
  if f != None: # Todo Save a basic population and reload it in the Puzzle
    raise NotImplemented

  # Loading a basic Population with a runner
  inds = ind.get_population()
  corner = [i for i in inds if i[1].count(0) == 2]
  border = [i for i in inds if i[1].count(0) == 1]
  inside = [i for i in inds if i[1].count(0) == 0]
  return Puzzle((corner, border, inside))


def save_population(puzzle):
  # TODO: Save with pickles
  pass


def loop(puzzle):
    """
      We Assume that the population is new an just setup and need to be eval first
    :param args:
    :param kwargs:
    :return:
    """
    for i in range(0, config.NGEN):
      # Evaluate the entire population
      puzzle.evaluate()
      # How you can save a picture into your personal folder
      puzzle.save_picture(gen=i)
      # Example of call
      removed_tils = puzzle.select()
      # Example of call
      puzzle.crossover(removed_tils)
      # Example of call
      puzzle.mutate(removed_tils)
      # If you want log the different data
      puzzle.log_stats(i)
      # you may want to generate some graph
      puzzle.generate_graph_values(config.NGEN)

    # END LOOP
    # You may want to save the log book
    puzzle.write_logbook()
    # you may want to generate some graph
    puzzle.generate_graph_values(config.NGEN)
    # TODO implement
    save_population(puzzle)

def main():
  try:
    os.mkdir("./gen/")
  except Exception as e:
    print e
  puzzle = load_population()
  loop(puzzle)


if __name__ == '__main__':
  main()