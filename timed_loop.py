import timeit
import config

def _timed_loop(puzzle, one_turn):
  """
    We Assume that the population is new an just setup and need to be eval first
  :param args:
  :param kwargs:
  :return:
  """
  for i in range(0, config.NGEN):
    start_time = timeit.default_timer()
    s = one_turn(puzzle, i)
    elapsed = timeit.default_timer() - start_time
    print "one generation in", elapsed, s
    if s:
      return True
  return False

def timed_loop(puzzle, one_turn):
  """
    We Assume that the population is new an just setup and need to be eval first
  :param args:
  :param kwargs:
  :return:
  """
  start_time = timeit.default_timer()
  solution = _timed_loop(puzzle, one_turn)
  elapsed = timeit.default_timer() - start_time
  print "Time to  elapsed ", elapsed, " Solution found ? ", solution
  puzzle.write_stats()
  puzzle.generate_stats_generations(ftype="avg")
  #puzzle.save_population()

