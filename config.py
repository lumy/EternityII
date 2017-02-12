
IMG="./Eternity/"

population_file_saved="try01.dill"

# population_file_base="test_4pieces.txt"
# size_line=2

# population_file_base="test_9pieces.txt"
# size_line=3

population_file_base="e2pieces.txt"
size_line=16

total = size_line * size_line
corner_pos = [0, size_line - 1, total - size_line, total - 1]
border_bot_pos = range(corner_pos[2] + 1, corner_pos[3])
border_top_pos = range(corner_pos[0] + 1, corner_pos[1])
border_left_pos = range(corner_pos[1] + size_line, corner_pos[3], size_line)
border_right_pos = range(corner_pos[0] + size_line, corner_pos[2], size_line)
border_pos = border_top_pos + border_bot_pos  + border_left_pos + border_right_pos
inside_pos = [x for x in range(0, total) if x not in corner_pos and x not in border_pos]

score_group_max = 4 * total
NGEN = 2000

mutate_inpd=0.001
selection_ind_value_step=1
elitism_percentage_start=10
elitism_percentage_up=4
gen_modulo_elitism=100

# NGEN % gen_modulo_elitism : 2000 / 100 = 20
# 20 * elitism_percentage_up : 20 * 4 = 80
# 80 + elitism_percentage_start : 80 + 10 = 90
# elitism_percentage_end = 90
