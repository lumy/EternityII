import copy
import pickle

import ind

# Coins Hautgauche, Hautdroit, basGauche, basDroit
CORNER_POS = [0, 15, 240, 255]
# Mask des coins Hautgauche, Hautdroit, basGauche, basDroit
MASK_CORNERS = [[0, None, None, 0], [0, 0, None, None], [None, None, 0, 0], [None, 0, 0, None]]
BORDER_TOP = range(1, 15)
BORDER_BOT = range(241, 255)
BODER_LEFT = [31, 47, 63, 79, 95, 111, 127, 143, 159, 175, 191, 207, 223, 239]
BORDER_RIGHT = [16, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224]
# Tout les position de X pour les Bords
BORDER_POS = BORDER_TOP + BORDER_BOT + BODER_LEFT + BORDER_RIGHT
# Represent les mask des Bordures
MASK_TOP = [0, None, None, None]
MASK_BOT = [None, None, 0, None]
MASK_LEFT = [None, 0, None, None]
MASK_RIGHT = [None, None, None, 0]
inds = ind.get_population()




class Node():
  def __init__(self, ind):
    self.line_id = ind[0]
    self.init = ind[1]
    # N S W E -> N E S W
    self.ind = [ind[1][0], ind[1][3], ind[1][1], ind[1][2]]
    self.father = None
    self.nodes = []
    self.rotation = 0
  def __repr__(self):
    return str(self.ind)

  def fit_to_border(self, type):
    while not self.mask(type):
      self.rotate()

  def mask(self, mask):
    """
      return True if the mask is ok with the content
    :param mask: list of None and 0
    :return:
    """
    def _mask(m, c):
      if c < 4:
        if m[c] == None and self.ind[c] != 0: # We don't want the 0 to be set anywhere
          return _mask(m, c + 1)
        if m[c] == self.ind[c]:
          return _mask(m, c + 1)
        else:
          return False
      return True
    return _mask(mask, 0)

  def copy(self):
    """
    Copy as the inital position
    :return:
    """
    return Node((self.line_id, self.init))

  def can_match(self, new_mask):
    n = self.copy()
    for i in range(0, 4):
      if n.mask(new_mask):
        return True
      n.rotate()
    return False


  def count(self, obj):
    """
        Use to count how many occurencences of the color in the current ind
    :param obj:
    :return:
    """
    return len([x for x in self.content if x == obj])

  def rotate(self):
    self.ind = self.ind[1:] + [self.ind[0]]
    self.rotation += 1
    if self.rotation >= 4:
      self.rotation = 0


def find_right_pos(list, new_mask):
  r = []
  for ind in list:
    if ind.can_match(new_mask):
      ind.fit_to_border(new_mask)
      r.append(ind)
  return r

SAVING = []
def save_tree(elem):
  def _save_tree(n, r):
    if n.father is None:
      r.append(n)
    else:
      _save_tree(n.father, r)
      r.append(n)
  tree = []
  _save_tree(elem, tree)
  SAVING.append(tree)
  print len(SAVING)

def runner(root, elem, list, pos=0):
  """
  The first elem is in a list with a good position
   we need to recursively find all the other possibilities.
     Going to first in the right way
  :param elem:
  :param list:
  :return:
  """
  # print "elem ", elem
  new_list = copy.deepcopy(list)
  if elem in list:
    new_list.pop(list.index(elem))
    # print "New Len List ", len(list)
  # print "Runner:(%s)" % len(new_list), pos
  # sleep(2)
  if pos < 14:
    new_mask = [0, None, None, elem.ind[1]]
  elif pos == 14:
    new_mask = [0, 0, None, elem.ind[1]]
  elif pos > 14 and pos < 29:
    new_mask = [elem.ind[2], 0, None, None]
  elif pos == 29:
    new_mask = [elem.ind[2], 0, 0, None]
  elif pos > 29 and pos < 44:
    new_mask = [None, elem.ind[3], 0, None]
  elif pos == 44:
    new_mask = [None, elem.ind[3], 0, 0]
  elif pos > 44 and pos < 59:
    new_mask = [None, None, elem.ind[0], 0]
  else:
    count = lambda x, c: c if x.father == None else count(x.father, c + 1)
    #print "We arrived on a corner: ", count(elem, 1)
    if elem.ind[0] != root.ind[2]:
      print "Can't save a false tree"
      return # Exception
    # print "Saving a solutiong"
    save_tree(elem)
    # Completed
    return
  # print "Looking for mask ", new_mask
  possible_pos = find_right_pos(new_list, new_mask)
  if len(possible_pos) == 0:
    # print "Dead End."
    return
  elem.nodes = possible_pos
  # print "Nodes: ", len(elem.nodes)
  for n in elem.nodes:
    n.father = elem
    runner(root, n, new_list, pos=pos+1)

def print_elem(node):
  def _print_elem(n):
    if n.father is None:
      print n
      return
    else:
      _print_elem(n.father)
      print n
  _print_elem(node)

corner = [Node(i) for i in inds if i[1].count(0) == 2]
border = [Node(i) for i in inds if i[1].count(0) == 1]

#fit_to_border(corner[0], MASK_CORNERS[0])
corner[0].fit_to_border(MASK_CORNERS[0])
runner(corner[0], corner[0], corner[1:] + border)
with open("borders.txt", "wb") as f:
  pickle.dump(SAVING, f)
print len(SAVING)
