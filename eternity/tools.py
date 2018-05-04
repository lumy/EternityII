"""
  Tools
"""
import dill
import ind
import puzzle
import config

def _load_file(path):
  """
    Use to load a file with dill, used for loading puzzle. file should have \
    been wrote with dill.

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


__md__ = [ # Order of appearance in the documentation
  'save_population',
  'load_population',
  '_load_file'
]
__all__ = [
  'save_population',
  'load_population',
]
