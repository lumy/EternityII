"""
Doc
"""
import puzzle
from stats import open_logboox
import sys

def init(g):
  """
    Doc
  """
  puzzle.Puzzle.dynamique_type()
  stats = open_logboox(g)
  stats.generate_stats_generations(ftype="avg")
  stats.generate_stats_generations(ftype="min")
  stats.generate_stats_generations(ftype="max")
  stats.draw_all_eternity()
  stats.generate_graph_per_generations(saved=True, show=False)

__md__ = [
  "init"
]
__all__ = [
  "init"
]

if __name__ == '__main__':
  if len(sys.argv) <= 1:
    print "Usage: %s <./path_log>" % sys.argv[0]
    exit(-1)
  g = sys.argv[1]
  init(g)
