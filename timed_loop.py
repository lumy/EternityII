import timeit

import time

import datetime

import config

def _timed_loop(puzzle, write_stats, one_turn, nloop=None, timer=None):
  """
    We Assume that the population is new an just setup and need to be eval first
  :param args:
  :param kwargs:
  :return:
  """
  end_time = None
  iteration = 0
  if timer:
    end_time = time.time() + datetime.timedelta(minutes=timer).total_seconds()

  while iteration < nloop and (end_time is None or time.time() < end_time):
    start_time = timeit.default_timer()
    s = one_turn(puzzle, iteration, write_stats)
    elapsed = timeit.default_timer() - start_time
    print "one generation in", elapsed, s
    if s:
      return True
    iteration += 1
  return False


def timed_loop(puzzle, write_stats, funcs, nloop=None, timer=None):
  """
    We Assume that the population is new an just setup and need to be eval first
  :param args:
  :param kwargs:
  :return:
  """
  one_turn, save_population = funcs
  start_time = timeit.default_timer()
  solution = _timed_loop(puzzle, write_stats, one_turn, nloop=nloop, timer=timer)
  elapsed = timeit.default_timer() - start_time
  print "Time to  elapsed ", elapsed, " Solution found ? ", solution
  puzzle.write_stats()
  puzzle.generate_stats_generations(ftype="avg")
  save_population(puzzle)

