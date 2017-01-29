import os
import ind

os.environ['TCL_LIBRARY'] = "C:\\Python27\\tcl\\tcl8.5"
os.environ['TK_LIBRARY'] = "C:\\Python27\\tcl\\tk8.5"

import config
from runner import Runner


def create_subdir(s):
  try:
    os.mkdir(s)
  except Exception as e:
    print e

def _load_file(s):
  try:
    with open(s) as e:
      return e.readlines()
  except Exception:
    return None

def load_population(pid):

  f = _load_file(config.population_file_saved)
  if f != None: # Todo Save a basic population and reload it in the Runner
    raise NotImplemented

  # Loading a basic Population with a runner
  inds = ind.get_population()
  corner = [i for i in inds if i[1].count(0) == 2]
  border = [i for i in inds if i[1].count(0) == 1]
  inside = [i for i in inds if i[1].count(0) == 0]
  return Runner((corner, border, inside), pid)


def main():
  pid = os.getpid()
  create_subdir("gen/%s/" % pid)
  create_subdir("gen/%s/puzzles" % pid)
  runner = load_population(pid)
  runner(verbose=True)


if __name__ == '__main__':
  main()