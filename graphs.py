import matplotlib.pyplot as plt


def _generate_graph_weight_population(xlabel, value1, value2, saved, show, fullpath):
  """
     Generate a graph and save it.
   :param ngen:
   :return:
   """

  fig, ax1 = plt.subplots()
  line1 = ax1.plot(value1[0], value1[1], "b.", label=value1[2])
  ax1.set_xlabel(xlabel)
  ax1.set_ylabel(value1[2], color="b")
  for tl in ax1.get_yticklabels():
    tl.set_color("b")
  ax2 = ax1.twinx()
  line2 = ax2.plot(value2[0], value2[1], "r.", label=value2[2])
  ax2.set_ylabel(value2[2], color="r")
  for tl in ax2.get_yticklabels():
    tl.set_color("r")
  lns = line1 + line2
  labs = [l.get_label() for l in lns]

  ax1.legend(lns, labs, loc="center right")
  plt.gcf().set_size_inches(18, 5)
  if show:
    plt.show()
  if saved:
    plt.savefig(fullpath, bbox_inches='tight', dpi=100)

def generate_graph_weight_population(generation, fits_ind, fits_group, saved, show, path):
      """
         Generate a graph and save it.
         Except generation to be on int and the data to be a ind and group fitnesses of one population.
       :param ngen:
       :return:
       """
      xlabel = "Population @ %s" % generation
      inds = (range(0, 256), fits_ind, "Individual Fitness")
      groups = (range(0, 256), fits_group, "Groups Fitness")
      _generate_graph_weight_population(xlabel, inds, groups, saved, show, "%s/ind_group_gen%s.png" % (path, generation))

def generate_graph_all_data(generations, fits_ind, fits_group, saved, show, path, ftype):
        """
           Generate a graph and save it.
           Except generation to be all the generation and fits_ind and fits_group to be all the min or max fits or avg.
         :param ngen:
         :return:
         """
        xlabel = "Generations"
        inds = (generations, fits_ind, "Individual Fitness %s" % ftype)
        groups = (generations, fits_group, "Groups Fitness %s" % ftype)
        _generate_graph_weight_population(xlabel, inds, groups, saved, show,
                                          "%s/all_%s_ind_group.png" % (path, ftype))


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