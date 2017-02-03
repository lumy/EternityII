from __future__ import print_function

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

def special_case(ind, val, direction):
  if ind[direction] == 0:
    return val + 0.25
  else:
    return val - 0.25

# noinspection PyUnboundLocalVariable
def normal_case(ind, ind2, val, direction):
  """

  :param ind:
  :param ind2:
  :param val:
  :param direction: Has to be NORTH, SOUTH, WEST or EAST define up of this file
  :return:
  """
  if direction == NORTH or direction == SOUTH:
    opposed = NORTH if direction == SOUTH else SOUTH
  elif direction == WEST or direction == EAST:
    opposed = WEST if direction == EAST else EAST
  return val + 0.25 if ind[direction] == ind2[opposed] else val - 0.25

def eval_position(populations, x):
  ind = populations[x]
  _y, _x = x / 16, x % 16
  val = 0.0
  if _y == 0:
    val = special_case(ind, val, NORTH) # Up
    val = normal_case(ind, populations[(_y + 1) * 16 + _x], val, SOUTH) # Down
  elif _y == 15:
    val = special_case(ind, val, SOUTH) # Down
    val = normal_case(ind, populations[(_y - 1)  * 16 + _x], val, NORTH) # Up
  else:
    val = normal_case(ind, populations[(_y - 1)  * 16 + _x], val, NORTH)  # Up
    val = normal_case(ind, populations[(_y + 1) * 16 + _x], val, SOUTH) # Down
  if _x == 0:
    val = special_case(ind, val, WEST) # Left
    val = normal_case(ind, populations[_y * 16 + _x + 1], val, EAST) # Right
  elif _x == 15:
    val = special_case(ind, val, EAST) # Right
    val = normal_case(ind, populations[_y * 16 + _x - 1], val, WEST) # Left
  else:
    val = normal_case(ind, populations[_y * 16 + _x + 1], val, EAST)  # Right
    val = normal_case(ind, populations[_y * 16 + _x - 1], val, WEST) # Left
  return val

def get_individual_neighbor(population, index, x, y, direction):
  """
    Retrieve the individual's neighbor from coordinates and direction
  :param population: one dimension array representing the puzzle grid
  :param index: individual's one dimensional coordinate on the grid
  :param x: individual's x 2d coordinate on the grid
  :param y: individual's y 2d coordinate on the grid
  :param direction: lookup direction from individual's point of view: NORTH || EAST || SOUTH || WEST
  :return neighbor: found neighbor or `None`
  """
  neighbor = None
  neighbor_index = None

  if direction == NORTH and y != 0: # y != min
    neighbor_index = index - 16 # (x, y - 1)
  elif direction == EAST and x != 15: # x != max
    neighbor_index = index + 1 # (x + 1, y)
  elif direction == SOUTH and y != 15: # y != max
    neighbor_index = index + 16 # (x, y + 1)
  elif direction == WEST and x != 0: # x != min
    neighbor_index = index - 1 # (x - 1, y)

  if neighbor_index != None:
    neighbor = population[neighbor_index]

  return [neighbor, neighbor_index]

def eval_individual(population, index):
  """
    Evaluate the individual score of an individual
  :param population: one dimension array representing the puzzle grid
  :param index: individual's one dimensional coordinate on the grid
  :return score: individual's score
  """
  individual = population[index]
  x = index % 16; y = index / 16
  score = 0

  eval_neighbors_matches = [
    # [neighbor, individual_side, neighbor_side]
    [get_individual_neighbor(population, index, x, y, NORTH), NORTH, SOUTH],
    [get_individual_neighbor(population, index, x, y, EAST), EAST, WEST],
    [get_individual_neighbor(population, index, x, y, SOUTH), SOUTH, NORTH],
    [get_individual_neighbor(population, index, x, y, WEST), WEST, EAST]
  ]

  for eval_neighbor_match in eval_neighbors_matches:
    neighbor = eval_neighbor_match[0][0]
    individual_side = eval_neighbor_match[1]
    neighbor_side = eval_neighbor_match[2]
    if neighbor == None or individual[individual_side] == neighbor[neighbor_side]:
      score += 1;

  print("individual evaluation at: | index =", index, "\t| x =", x, "\t| y =", y, "\t| score =", score)

  return score

virgin_individuals_cluster_score = []

def init_virgin_individuals_cluster_score():
  for index in range(0, 256):
      virgin_individuals_cluster_score.append(None);

init_virgin_individuals_cluster_score();

def eval_individual_cluster(population, index, individuals_score, individuals_cluster_score, score = 0, level = 0, cluster = []):
  """
    Evaluate the cluster's score of an individual
  :param population: one dimension array representing the puzzle grid
  :param index: individual's one dimensional coordinate on the grid
  :return score: individual's score
  """
  individual = population[index]
  x = index % 16; y = index / 16

  if individuals_cluster_score[index] != None:
    return individuals_cluster_score[index]

  eval_neighbors_matches = [
    # [neighbor, individual_side, neighbor_side]
    [get_individual_neighbor(population, index, x, y, NORTH), NORTH, SOUTH],
    [get_individual_neighbor(population, index, x, y, EAST), EAST, WEST],
    [get_individual_neighbor(population, index, x, y, SOUTH), SOUTH, NORTH],
    [get_individual_neighbor(population, index, x, y, WEST), WEST, EAST]
  ]

  print("cluster eval at | index =", index, "\t| x =", x, "\t| y =", y, "\t| prev score =", score, "| i score =", individuals_score[index])
  cluster.append(index)
  score += individuals_score[index]
  individuals_cluster_score[index] = -1
  for eval_neighbor_match in eval_neighbors_matches:
    neighbor = eval_neighbor_match[0][0]
    neighbor_index = eval_neighbor_match[0][1]
    individual_side = eval_neighbor_match[1]
    neighbor_side = eval_neighbor_match[2]
    if neighbor != None and individuals_cluster_score[neighbor_index] != -1 and individual[individual_side] == neighbor[neighbor_side]:
      print("\tGoing recursively from individual at index =", index, "into neighbor on", neighbor_index)
      score = eval_individual_cluster(population, neighbor_index, individuals_score, individuals_cluster_score, score, level + 1, cluster);
      print("\tGoing recursively out from neighbor at index =", neighbor_index, "into individual on", index)

  if level == 0:
    for individual_index in cluster:
      individuals_cluster_score[individual_index] = score

  print("cluster eval at | index =", index, "\t| x =", x, "\t| y =", y, "\t| cur score =", score)

  return score

def eval_solution(population):
  """
    Evaluate the whole population on the solution.
  :param population:
  :return:
  """

  # 0 a 15
  # print population
  # print type(population)
  # values = [eval_position(population, x) for x in range(0, 256)]
  individuals_score = [eval_individual(population, index) for index in range(0, 256)]
  individuals_cluster_score = virgin_individuals_cluster_score
  [eval_individual_cluster(population, index, individuals_score, individuals_cluster_score) for index in range(0, 256)]
  # Fitness = (number of good position * 100.0) / 256 (total element)
  note = sum(individuals_score) * 100 / 256 # Total
  print("evaluation complete")
  print("")
  return (individuals_score, note)
