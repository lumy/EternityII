"""
  Configuration:
    can be reloaded at runtime.
"""
import math

IMG="./Eternity/"

population_file_saved="try01.dill"

population_file_base="./eternity/e2pieces.txt"

# NGEN % gen_modulo_elitism : 2000 / 100 = 20
# 20 * elitism_percentage_up : 20 * 4 = 80
# 80 + elitism_percentage_start : 80 + 10 = 90
# elitism_percentage_end = 90
NGEN = 2000
mutate_inpd=0.01
selection_ind_value_step=1
elitism_percentage_start=10
elitism_percentage_up=4
gen_modulo_elitism=100

# diff = connection_completions - score
select_light = 25.0
select_medium = 70.0
# select_heavy for other

size_line = int(round(math.sqrt(256)))
total = size_line * size_line
corner_pos = [0, size_line - 1, total - size_line, total - 1]
border_bot_pos = range(corner_pos[2] + 1, corner_pos[3])
border_top_pos =  range(corner_pos[0] + 1, corner_pos[1])
border_left_pos = range(corner_pos[1] + size_line, corner_pos[3], size_line)
border_right_pos = range(corner_pos[0] + size_line, corner_pos[2], size_line)
border_pos = list(border_top_pos) + list(border_bot_pos) + \
  list(border_left_pos) + list(border_right_pos)
inside_pos =  [x for x in range(0, total) if x not in corner_pos and x not in border_pos]
score_group_max = 4 * total

__all__ = [ "init"
]
__md__ = [
    "init"
]
