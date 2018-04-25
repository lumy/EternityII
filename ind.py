"""
 - Load all tils.
 - Ind objet is the representation of a unique tile. See [Ind](#Ind) description.

A schema is an int representing a color/schema for a til.

### mask-description
      
A mask is a list of None (No-Color specify) or a schema (0 is border: grey)

eg: [None, None, 1, 1]
"""
#!/usr/bin/env python
import copy
import config


def get_population():
  """
  Load the basic Population from the file e2pieces.txt
  :return: a list of (UID:int, [schema:int, schema:int, schema:int, schema:int]
  """
  with open(config.population_file_base) as f:
    l = f.readlines()
  l = [(x + 1, [int(i) for i in l[x].split()]) for x in range(0, len(l))]
  return l


class Ind(object):
  """

       Ind class represent a til:

         - Ind.uid unique id for schema repr
         - Ind.content list int [schema:int, schema:int, schema:int, schema:int] directions in order North Est South Weast
         - Ind.rotation number of clockwork rotation apploied (range 0, 3)
  """

  def __init__(self, func, lines):
    """
    The func, lines args are actually gonna be change, for an iterator or for simple uid,content, rotation arguments.
    The idea was to not initialize on the file but on randomized lines.

    :param func: function that take lines in params and return one line -> uid, [North-schema South-schema Weast-schema East-schema].
    :param lines: Lines|arg to be given to func
    """
    self.uid, dirs = func(lines)
    n, s, e, w = dirs
    self.content = [n, e, s, w]
    self.rotation = 0

  def __getitem__(self, index):
    """
      :return:  schema -> int
    """
    return self.content[index]

  def __setitem__(self, key, value):
    """ Shouldn't be used
    """
    raise NotImplemented("Not Authorized")
#    self.content[key] = value

  def best_value_of_mask(self, mask):
    """
    Find the best value possible for a mask.
    :param mask: mask to test against.
    :return: value between 0 and 4 that represant individual connection/score.
    """
    t = [self._mask_(mask, c_index=0), self._mask_(mask, c_index=1), self._mask_(mask, c_index=2),
         self._mask_(mask, c_index=3)]
    return t[t.index(max(t))]

  def _mask_(self, mask, c_index=0):
    """
        :param mask: list of None and 0.
        :param c_index: See [Mask](#mask)
        :return: value of fitness [0-4].
    """
    def _mask(m, index, c):
      if c < 4:
        if index >= 4:
          index = 0
        if m[c] == None or m[c] == self.content[index]:
          return 1 + _mask(m, index + 1, c + 1)
        else:
          return 0 + _mask(m, index + 1, c + 1)
      return 0

    return _mask(mask, c_index, 0)

  def mask(self, mask, c_index=0):
    """
      test a [Mask](#mask-description)
      :param mask: [Mask](#mask-description)
      :param c_index: index content to start at, this simulate rotation.
      :return: True if the mask fit.
    """
    if 4 == self._mask_(mask, c_index=c_index):
      return True
    return False

  def count(self, obj):
    """
        Use to count how many occurencences of the schema in the current ind
    :param obj:
    :return:
    """
    return len([x for x in self.content if x == obj])

  def rotate(self):
    """
      Rotate the ind.
    """
    self.content = self.content[1:] + [self.content[0]]
    self.rotation += 1
    if self.rotation >= 4:
      self.rotation = 0

  def rotates(self, nb):
    """
    :param nb: rotates nb times.
    """
    while nb > 0:
      nb -= 1
      self.rotate()

  def __repr__(self):
    return "n:%s e:%s s:%s w:%s" % (self.content[0], self.content[1], self.content[2], self.content[3])

__md__ = [
  "get_population",
  "Ind"
]

__all__ = [
  "get_population",
  "Ind",
  ]

if __name__ == '__main__':
  # should have test / test_ind.py
  i = Ind(lambda x: (0, [1, 0, 0, 17]), None)
  mask = [0, 0, None, None]
  assert i.mask(mask) == False, "shouldn't fit %s %s" % (i, mask)
  i.rotate()
  assert i.mask(mask) == True, "should fit %s %s" % (i, mask)
  i.rotate()
  assert i.mask(mask) == False, "shouldn't fit %s %s" % (i, mask)
  get_population()
