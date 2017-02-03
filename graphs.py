import matplotlib.pyplot as plt

def generate_graph_weight_population(generation, fits_ind, fits_group, saved, show, path):
  """
     Generate a graph and save it.
   :param ngen:
   :return:
   """
  fig, ax1 = plt.subplots()
  line1 = ax1.plot(range(0, 256), fits_ind, "b.", label="Individual Fitness")
  ax1.set_xlabel("Population @ %s" % generation)
  ax1.set_ylabel("Individual Fitness", color="b")
  for tl in ax1.get_yticklabels():
    tl.set_color("b")

  ax2 = ax1.twinx()
  line2 = ax2.plot(range(0, 256), fits_group, "r.", label="Groups Fitness")
  ax2.set_ylabel("Group Fitness", color="r")
  for tl in ax2.get_yticklabels():
    tl.set_color("r")
  lns = line1 + line2
  labs = [l.get_label() for l in lns]
  ax1.legend(lns, labs, loc="center right")
  plt.gcf().set_size_inches(18, 5)
  if show:
    plt.show()
  if saved:
    plt.savefig("%s/ind_group_gen%s.png" % (path, generation), bbox_inches='tight', dpi=100)

    # nrow = [0, None, -1.0, 1.0]
  # # [-100, -75, -50, -25, 0, 25, 50, 75, 100]
  # # Temporary fix until we now exactly what we want to log
  # y = 0
  # for x in fitnesses:
  #   plt.scatter(y, x, marker='.', c='c')
  #   y += 1
  # plt.axis(nrow)
  # plt.ylabel("weight %s" % fitness_type)
  # plt.xlabel("population generation(%s)" % generation)

def generate_all_score(fitnesses):
  pass