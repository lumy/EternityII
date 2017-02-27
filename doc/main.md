# main

Main Module



main file can be called as ```python main.py --help```
Or ```python main.py -l [num_loop] -t [min_loop] --old-pop --timed```

```--loop|-l``` Number of loop maximum to do. if set to -1 it will not be   used to stop the loop(default: config.NGEN).

```--time|-t``` Maximum time to execute the loop in min, if not set will not   be used to stop the loop (default: None).

```--timed``` iteration and loop would be timed. (not really usefull).

```--old-pop|-o``` Load an old population. path is set in config file at   config.population_file_saved.


## API


### main

  main function will load a new population or an old one and run it with our     [Current Algorithm](doc/Algorithm.md)


 - [Bool](https://docs.python.org/2/library/stdtypes.html#boolean-values) write_stats: Should we be logging stats. Used during benchmark,   otherwise always set to True.
- [Bool](https://docs.python.org/2/library/stdtypes.html#boolean-values) old_pop: loading the old population saved at   config.population_file_saved
- float timer: see [loop](doc/main.md#loop)
- int nloop: see [loop](doc/main.md#loop)
- timed: that will activate some timer, to calculate how many time for one iteration and for the whole iteration.


### loop

  This function loop with stopping conditions as set in params. Write the     logbook at the end of the run.


- [puzzle](doc/puzzle.md): A [puzzle](doc/puzzle.md) object.
- [Bool](https://docs.python.org/2/library/stdtypes.html#boolean-values) write_stats: Should we be logging stats. Used during benchmark,   otherwise always set to True.
- int nloop: Number of loop to do, if -1 will not be used to stop the   loop.
- float timer: Minute to turn the loop if None will not be used to stop   loop.


- return bool: is the solution has been found or not


### one_turn

  Represent One iteration of the Algorithm.

  Ex.

  1. select
  2. crossover
  3. mutate
  4. evaluate
  5. log_stats

  More information at [Current Algorithm](doc/Algorithm.md)

- [puzzle](doc/puzzle.md): A [Puzzle](doc/puzzle.md) object.
- int generation: Iteration index.
- [Bool](https://docs.python.org/2/library/stdtypes.html#boolean-values) write_stats: Should we be logging stats. Used during benchmark,   otherwise always set to True.

- return bool: solution as been found or Not.


### get_args

  Function to Set and Parse args with argparse.



- return: object


### save_population

  Save a given puzzle into the path config.population_file_saved.


- [puzzle](doc/puzzle.md): A [Puzzle](doc/puzzle.md) object.

- return: None

- throw Exception: Can throw classic exception around open and dill.dump


### load_population

  Load an old population or a new one. If old_pop is False, the new     population will be loaded from config.population_file_base.


- [Bool](https://docs.python.org/2/library/stdtypes.html#boolean-values) old_pop: loading the old population saved at   config.population_file_saved

- return: A [Puzzle](doc/puzzle.md) object.


### _load_file

  Use to load a Puzzle with dill.


- [Str](https://docs.python.org/2/library/stdtypes.html#sequence-types-str-unicode-list-tuple-bytearray-buffer-xrange) path: path to the file to load

- return: object (excepted [Puzzle](doc/puzzle.md) but no check is made)
