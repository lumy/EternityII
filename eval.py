from __future__ import print_function
import copy

import config

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

virgin_score_list = []

def init_virgin_scores_list():
  for index in range(0, config.total):
      virgin_score_list.append(None);

init_virgin_scores_list()

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
    neighbor_index = index - config.size_line # (x, y - 1)
  elif direction == EAST and x != (config.size_line - 1): # x != max
    neighbor_index = index + 1 # (x + 1, y)
  elif direction == SOUTH and y != config.size_line - 1: # y != max
    neighbor_index = index + config.size_line # (x, y + 1)
  elif direction == WEST and x != 0: # x != min
    neighbor_index = index - 1 # (x - 1, y)

  if neighbor_index != None:
    neighbor = population[neighbor_index]

  return [neighbor, neighbor_index]

def eval_individual(population, index, individuals_score, individuals_cluster_score, cluster_score = 0, level = 0, cluster = []):
  """
    Evaluate the individual's and individual's clusters scores starting from an individual

  :param population: one dimension array representing the puzzle grid
  :param index: individual's one dimensional coordinate on the grid
  :param individuals_score: list of individuals score
  :param individuals_cluster_score: list of clusters score by individual
  :param cluster_score: cluster's score
  :param level = 0: grid crawling level, default value is `0`
  :param cluster: list of individuals in the crawled cluster, default value is empty
  :return cluster_score: individual's cluster's score
  """
  individual = population[index]
  x = index % config.size_line
  y = index / config.size_line
  individual_score = 0

  # print("Evaluating individual\t\t\t\t( index:", index, ")\t( x:", x, "| y:", y, ")")

  if level == 0:
    # print("Initializing new cluster from individual\t( index:", index, ")")
    cluster = []
  if individuals_cluster_score[index] != None:
    # print("Cluster already evaluated for individual\t( index:", index, ")\n")
    return individuals_cluster_score[index]

  eval_neighbors_matches = [
    # [neighbor, individual_side, neighbor_side]
    [get_individual_neighbor(population, index, x, y, NORTH), NORTH, SOUTH],
    [get_individual_neighbor(population, index, x, y, EAST), EAST, WEST],
    [get_individual_neighbor(population, index, x, y, SOUTH), SOUTH, NORTH],
    [get_individual_neighbor(population, index, x, y, WEST), WEST, EAST]
  ]

  cluster.append(index)
  individuals_cluster_score[index] = -1
  for eval_neighbor_match in eval_neighbors_matches:
    neighbor = eval_neighbor_match[0][0]
    neighbor_index = eval_neighbor_match[0][1]
    individual_side = eval_neighbor_match[1]
    neighbor_side = eval_neighbor_match[2]
    # evaluate individual and neighbor corresponding sides
    if neighbor == None or individual[individual_side] == neighbor[neighbor_side]:
      individual_score += 1
    # crawl (or not) and evaluate individuals cluster
    if neighbor != None and individuals_cluster_score[neighbor_index] != -1 and individual[individual_side] == neighbor[neighbor_side]:
      # print("[ + ] Crawling cluster from individual\t\t( index:", index, ")\tto neighbor ( index:", neighbor_index, ")")
      cluster_score = eval_individual(population, neighbor_index, individuals_score, individuals_cluster_score, cluster_score, level + 1, cluster)
      # print("[ - ] Crawling out cluster from neighbor\t( index:", neighbor_index, ")\tto individual ( index:", index, ")")

  individuals_score[index] = individual_score
  cluster_score += individual_score
  if level == 0:
    # print("Finalizing cluster from individual\t\t( index:", index, ")\twith ( cluster score:", cluster_score, ")")
    # print("Cluster content\t\t\t\t\t(", cluster, ")\n")
    for individual_index in cluster:
      individuals_cluster_score[individual_index] = cluster_score

  return cluster_score

def eval_solution(population):
  """
    Evaluate the whole population on the solution.

    more details at: https://github.com/lumy/EternityII/issues/5

    individual score: range [0, 4]
    individual's cluster score: range [0, 1024]
    puzzle completion: range [0.0, 100.0]

    :individuals_score: list of individuals score
    :individuals_cluster_score: list of clusters score by individual
    :puzzle_completion: puzzle completion in percentage
  :param population: one dimension array representing the puzzle grid
  :return (individuals_score, individuals_cluster_score, puzzle_completion):
  """
  individuals_score = copy.deepcopy(virgin_score_list)
  individuals_cluster_score = copy.deepcopy(virgin_score_list)

  for index in range(0, len(population)):
    eval_individual(population, index, individuals_score, individuals_cluster_score)
  puzzle_completion = sum(individuals_score) * 100.0 / 1024.0

  return (individuals_score, individuals_cluster_score, puzzle_completion)
