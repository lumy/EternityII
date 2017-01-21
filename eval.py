NORTH = 0
WEST = 1
SOUTH = 2
EAST = 3

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

def eval_solution(populations):
  """
    Evaluate the whole population on the solution.
  :param populations:
  :return:
  """

  # 0 a 15
  # print populations
  # print type(populations)
  values = [eval_position(populations, x) for x in range(0, 256)]
  # Fitness = (number of good position * 100.0) / 256 (total element)
  note = sum(values) * 100 / 256 # Total
  return (values, note)
