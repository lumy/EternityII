# stats

Statistics:




# Class
## Stats(self, personal_path)

We have to talk about it here and see what's we're looging and if we do us a math on it.


- return:

### \_generate_graph_per_generation(self, gen, inds, groups, saved=True, show=False)






### draw_all_eternity(self)






### draw_eternity(self, gen, inds, score)






### free_memory(self)






### generate_graph_per_generations(self, saved=True, show=False)






### generate_stats_generations(self, ftype="avg", saved=True, show=False)






### init_book(self)






### log_stats(self, generation, population, selected, n_mutated, scores)

Stats to be logged:
Generation : Represant the iteration you're on
mutated : Represent the mutated population
mutation_percent : Percentage of mutation
fitness_ind : Fitness of all individue
group_fitness : Fitness of all groups
population : Population at this time.
score : One score for the Puzzle
record: fitness_ind and fitness_group compiled by stats. (min max avg)

- generation: The current iteration you're on
- population: The current population you're using
- n_mutated: The number of mutated element.

- return:



### write(self)






### write_logbook(self, bin=False)

The binary mode save All the data, so if you want create Graph you need to have a pckl Log book as much as
you need a txt one to read fast information.

- bin:

- return:



