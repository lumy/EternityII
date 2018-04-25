# eval

Doc




# Functions


### eval_individual_score(population, index)

Doc




### eval_solution(population)

Evaluate the whole population on the solution.

more details at: https://github.com/lumy/EternityII/issues/5

individual score: range [0, 4]
individual's cluster score: range [0, 1024]
puzzle completion: range [0.0, 100.0]


  :individuals_score: list of individuals score
  :individuals_cluster_score: list of clusters score by individual
  :puzzle_completion: puzzle completion in percentage
- population: one dimension array representing the puzzle grid

- return (individuals_score, individuals_cluster_score, puzzle_completion):



### eval_individual(population, index, individuals_score, individuals_cluster_score, cluster_score = 0, level = 0, cluster = [])

Evaluate the individual's and individual's clusters scores starting from an individual


- population: one dimension array representing the puzzle grid
- index: individual's one dimensional coordinate on the grid
- individuals_score: [list](https://docs.python.org/2/tutorial/datastructures.html#more-on-lists) of individuals score
- individuals_cluster_score: [list](https://docs.python.org/2/tutorial/datastructures.html#more-on-lists) of clusters score by individual
- cluster_score: cluster's score
- level = 0: grid crawling level, default value is `0`
- cluster: [list](https://docs.python.org/2/tutorial/datastructures.html#more-on-lists) of individuals in the crawled cluster, default value is empty

- return cluster_score: individual's cluster's score



### get_individual_neighbor(population, index, x, y, direction)

Retrieve the individual's neighbor from coordinates and direction


- population: one dimension array representing the puzzle grid
- index: individual's one dimensional coordinate on the grid
- x: individual's x 2d coordinate on the grid
- y: individual's y 2d coordinate on the grid
- direction: lookup direction from individual's po[int](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-[float](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-float-long-complex)-long-complex) of view: NORTH || EAST || SOUTH || WEST

- return neighbor: found neighbor or `None`



### init_virgin_scores_list()

Doc


