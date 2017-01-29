"""
Package use for drawing the game
"""
import os
import pygame
import config
from ind import Ind
from puzzle import Puzzle

IPIECES=[]

class Image():
  def __init__(self, uid, surface):
    self.uid = uid
    self.surface = surface

  def copy(self, instance=None):
    if instance is None:
      return Image(self.uid, self.surface.copy())
    return Image(self.uid, instance)

def _init_ipieces():
  global IPIECES
  pygame.init()
  IPIECES = []
  imgs = os.listdir(config.IMG)
  for imgp in imgs:
    fullpath = config.IMG + imgp
    if ".png" in fullpath:
      surface = pygame.transform.scale(pygame.image.load(fullpath), (60, 60))
      IPIECES.append(Image(int(imgp[:imgp.find(".")]), surface))

def _sort_uid(linds):
  l = []
  for ind in linds:
    piece = next((x for x in IPIECES if x.uid == ind.uid), None)
    if piece == None:
      print ind.uid
      raise IndexError
    angle, c = 0, ind.rotation
    while c > 0:
      c -= 1
      angle += 90
    l.append(piece.copy(pygame.transform.rotate(piece.surface, angle)))
  return l

def _show_game(l):
  screen = pygame.display.set_mode((960, 960))
  x, y = 0,0
  screen.fill((0, 0, 0))
  for ind in l:
    screen.blit(ind.surface, [x, y])
    x += 60
    if x >= 960:
      x = 0
      y += 60
  pygame.display.flip()
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return

def _prepare(linds):
  if len(IPIECES) == 0:
    _init_ipieces()
  if isinstance(linds, Puzzle):
    _prepare(linds.get_pieces())
    return
  lfinal = _sort_uid(linds)
  return lfinal

def draw(linds):
  """
    Function to call when u want to show the Puzzle.
  :param linds: A Puzzle or a list of individuals
  :return:
  """
  lfinal = _prepare(linds)
  _show_game(lfinal)
  return

def save(linds, file_path):
  lfinal = _prepare(linds)
  screen = pygame.display.set_mode((960, 960))
  pygame.display.iconify()
  x, y = 0, 0
  screen.fill((0, 0, 0))
  for ind in lfinal:
    screen.blit(ind.surface, [x, y])
    x += 60
    if x >= 960:
      x = 0
      y += 60
  pygame.image.save(screen, "%s.jpeg" % file_path)

if __name__ == '__main__':
  l = []
  with open("e2pieces.txt") as f:
    l = f.readlines()
    l = [Ind(x + 1, [int(i) for i in l[x].split()]) for x in range(0, len(l))]
    l[0].rotate()
