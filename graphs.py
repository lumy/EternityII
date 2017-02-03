import matplotlib.pyplot as plt

def generate_graph_weight_population(fitnesses, path, generation, fitness_type="individual"):
  """
     Generate a graph and save it.
   :param ngen:
   :return:
   """
  nrow = [0, None, -1.0, 1.0]
  # [-100, -75, -50, -25, 0, 25, 50, 75, 100]
  # Temporary fix until we now exactly what we want to log
  y = 0
  for x in fitnesses:
    plt.scatter(y, x, marker='.', c='c')
    y += 1
  plt.axis(nrow)
  plt.ylabel("weight %s" % fitness_type)
  plt.xlabel("population generation(%s)" % generation)
  plt.gcf().set_size_inches(15, 5)
  plt.savefig("%s/g_%s_%s.png" % (path, fitness_type, generation), bbox_inches='tight', dpi=100)
  plt.clf()
  plt.close()

def generate_all_score(fitnesses):
  """
  graph   des   scores   post   boucle   algo

  :param fitnesses:
  :return:
  """
  pass