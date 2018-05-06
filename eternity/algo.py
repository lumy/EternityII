"""
  Algo
"""
import time
import datetime
import config
import tools

def one_turn(puzzle, generation, **kwargs):
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
  #if last_con > puzzle.connections_completions:
   # print "Score going down. Avoiding ? ", generation
    #puzzle.population = puzzle.stats.populations[-1]
    # if config.mutate_inpd == 0.0005:
    #   config.mutate_inpd = 0.05
  #  return
  # Always be logging
  puzzle.log_stats(generation, rm_tils, n_mutated)
  if puzzle.population[0].fitness_group.values[0] == config.score_group_max:
    return True
  return False


def loop(puzzle, write_stats=False, timer=None, ngen=None, **kwargs):
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

  while (ngen == -1 or iteration < ngen) and (end_time is None or time.time() < end_time):
    if one_turn(puzzle, iteration, **kwargs):
      if write_stats:
        puzzle.write_stats()
      return True
    if iteration % 500 == 0 and iteration != 0:
      # Write the populations to a file to free some memory
      puzzle.stats.free_memory()
    iteration += 1
  
  if write_stats:
    puzzle.write_stats()
    tools.save_population(puzzle)
  return False

__md__ = [ # Order of appearance in the documentation
  'loop',
  'one_turn',
  'save_population',
  'load_population',
  '_load_file'
]
__all__ = [
  'loop',
  'one_turn',
]
