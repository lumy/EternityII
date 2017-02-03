"""
Use to represent an individual a 4 int direciton and a rotation. (and an uid to keep the line reference)
"""
import copy

def get_population():
  """
  Load the basic Population from the file e2pieces.txt
  :return: a list of int
  """
  with open("e2pieces.txt") as f:
    l = f.readlines()
  l = [(x + 1, [int(i) for i in l[x].split()]) for x in range(0, len(l))]
  return l

class Ind(object):
  def __init__(self, f, l):
    """
       The Individual reorganize the line in CLOCKWORK MOD (orange ?) so it can easily rotate them.
    :param uid: Represant the id of the tile for final printing
    :param line: Line in order North South Weast East.
    """
    self.uid, dir = f(l)
    n, s, w, e = dir
    self.content = [n, e, s, w]
    self.rotation = 0

  def __getitem__(self, item):
    return copy.copy(self.content[item])

  def __setitem__(self, key, value):
    self.content[key] = value

  def mask(self, mask):
    """
      return True if the mask is ok with the content
    :param mask: list of None and 0
    :return:
    """
    def _mask(m, c):
      if c < 4:
        if m[c] == None:
          return _mask(m, c + 1)
        if m[c] == self.content[c]:
          return _mask(m, c + 1)
        else:
          return False
      return True
    return _mask(mask, 0)

  def count(self, obj):
    """
        Use to count how many occurencences of the color in the current ind
    :param obj:
    :return:
    """
    return len([x for x in self.content if x == obj])

  def rotate(self):
    self.content = self.content[1:] + [self.content[0]]
    self.rotation += 1
    if self.rotation >= 4:
      self.rotation = 0

  def rotates(self, nb):
    while nb > 0:
      nb -= 1
      self.rotate()

  def __repr__(self):
    return "n:%s e:%s s:%s w:%s" % (self.content[0], self.content[1], self.content[2], self.content[3])


if __name__ == '__main__':
  i = Ind(lambda x: (0, [1, 0, 0, 17]), None)

  print i.mask([0, 0, None, None])
  i.rotate()
  print i.mask([0, 0, None, None])
  i.rotate()
  print i.mask([0, 0, None, None])
  print i
