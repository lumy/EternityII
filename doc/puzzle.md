# puzzle

puzzle module contain Puzzle object.



# Class
# 

    Puzzle represent a board game, it contain a population of     [Individuals](doc/ind.md)
    
    Puzzle Description:
    
    - self.personal_path: path where the stats are gonna be wrote.
    - self.completion: Completion of puzzle.
    - self.connections_completions: Connections completions.
    - self.toolbox: deap.toolbox
    - self.population: current population
    - self.stats: [Stats instance](doc/stats.md)

### \_get_line_(self, arr)

    



### \_mutate(self, positions)

    Goes through all positions given in parameters and apply a mutation. If       random.uniform(0, 1) <= config.mutate_inpd Do a mutation. Mutation can be       One of these 3 type: [mutate_position](#mutate_position)       [mutate_rotation](ind.md#rotates), mutation_position_rotation       (both at same time in this order).
    

- [list](https://docs.python.org/2/tutorial/datastructures.html#more-on-lists) positions: a [list](https://docs.python.org/2/tutorial/datastructures.html#more-on-lists) of position to go through.

- return [int](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-[float](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-float-long-complex)-long-complex): Number of mutated element.


### crossover(self, removed_tils)

    - We shall first sort the removed_tils by type of tils (list_corner/border/center)
    - then we should look for every available connected position for a given type.
    - We should shuffle our lists
    - for each type of tils
    - get X positions valuable for now and put it at a random one.
    - Look for new free conncted position to add to the typelist
    

- [list](https://docs.python.org/2/tutorial/datastructures.html#more-on-lists) removed_tils: [list](https://docs.python.org/2/tutorial/datastructures.html#more-on-lists) of [ind](doc/ind.md)


### draw_all_generations(self)

    See [@stats file](doc/stats.md#draw_all_eternity)



### draw_generation(self, n)

    See [@stats file](doc/stats.md#draw_generation)
    

- n:

- return:


### dynamique_type()

    Static Method. Create dynamique Type used by deap.
    This method needs to be called before any loading file.
    
    Create static type:
    
    - FitnessInd
    - FitnessGroup
    - Individual
    
    Can be found at ```deap.creator.FitnessInd``` or       ```deap.creator.Individual```



### evaluate(self)

    Call the [evaluate function from eval module](doc/eval.md). set value for       ```self.connections_completions``` ```self.completion``` and for every       individuals fitnesses (ind and groups)



### fit_to_border(self, ind, type)

    Rotate the pieces until it feet with the border.
    
    *Warning*: This can generate an infinite loop ! if ind can fit mask       because of missing 0 or because of number not present. Use carefully.
    

- [ind](doc/ind.md) ind:
- [list](https://docs.python.org/2/tutorial/datastructures.html#more-on-lists) type: [list](https://docs.python.org/2/tutorial/datastructures.html#more-on-lists) of None and [int](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-[float](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-float-long-complex)-long-complex) to fit.

- return:


### fixing_outside(self)

    Use to make match each corner/border to the right [mask](doc/mask.md).
    
    *Warning* This is an unsafe function, from few test, if the corner CAN'T
    fit the mask, (ex: mask [0,0,None,None] tils [0,1,2,3]) it will make an       infinite loop.



### generate_graph_per_generations(self, saved=True, show=False)

    See [@stats file](doc/stats.md#generate_graph_per_generations)
    

- saved:
- show:


### generate_stats_generations(self, ftype="avg", saved=True, show=False)

    See [@stats file](doc/stats.md#generate_stats_generations)
    

- ftype:
- saved:
- show:


### get_mask(self, index)

    return the [mask](doc/mask.md) for a given index
    

- [int](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-[float](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-float-long-complex)-long-complex) index: index to extract [mask](doc/mask.md) of.

- return [list](https://docs.python.org/2/tutorial/datastructures.html#more-on-lists): [mask](doc/mask.md)


### give_random_pos(self, pos, line)

    



### log_stats(self, generation, rm_tils, n_mutated)

    Log statistics, do that at each iteration, more info [@stats file](doc/stats.md)
    

- [int](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-[float](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-float-long-complex)-long-complex) generation: Iteration Index.
- [int](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-[float](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-float-long-complex)-long-complex) rm_tils: Number of selected/replaced tils.
- [int](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-[float](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-float-long-complex)-long-complex) n_mutated: Number of mutated element at this iteration.

- return:


### mutate(self)

    Apply mutation on every [positions type](doc/config.md#positions). call       [self.fixing_outside](#fixing_outside).
    


- return [int](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-[float](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-float-long-complex)-long-complex): Number of mutated element.


### mutate_position(self, index, list_positions)

    Change the position between index and a random pos from list_position.
    

- [int](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-[float](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-float-long-complex)-long-complex) index: The index that going to be mutated.
- [list](https://docs.python.org/2/tutorial/datastructures.html#more-on-lists) [list](https://docs.python.org/2/tutorial/datastructures.html#more-on-lists)_positions: [list](https://docs.python.org/2/tutorial/datastructures.html#more-on-lists) of [int](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-[float](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-float-long-complex)-long-complex), all position possible to change.


### place_type(self, list_type, pos_type)

    - get X positions valuable for now and put it at a random one.
    - Look for new free conncted position to add to the typelist
    - Place the next til
    

- [list](https://docs.python.org/2/tutorial/datastructures.html#more-on-lists) [list](https://docs.python.org/2/tutorial/datastructures.html#more-on-lists)_type: [list](https://docs.python.org/2/tutorial/datastructures.html#more-on-lists) of [ind](doc/ind.md)
- [list](https://docs.python.org/2/tutorial/datastructures.html#more-on-lists) pos_type: [list](https://docs.python.org/2/tutorial/datastructures.html#more-on-lists) of [int](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-[float](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-float-long-complex)-long-complex)


### randomize_lines(self, lc, lb, li)

    Used during init, if it's a new population then we place them by       [type](doc/ind.md#type) and randomly.
    


- return: yield line organize but randomize.


### roulette(self, elems, k)

    Please have a look at [deap roulette function](https://github.com/DEAP/deap/blob/master/deap/tools/selection.py)
    It's cleary inspired of the function selRoulette.
    Thanks to deap.

- elems:
- k:

- return:


### save_picture(self, gen=0, score=0)

    See [@eternity file](doc/eternity.md#save)
    

- gen:
- score:

- return:


### select(self, generation, con_complt, score)

    Remove all connection < 4 and group_value < average_group_value

- generation:
- average_ind_value:
- average_group_value:

- return:


### set_individual_best_mask(self, ind, pos, mask)

    



### write_stats(self)

    Write the stats. More info [@stats file](doc/stats.md).



