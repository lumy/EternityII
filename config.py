
IMG="./Eternity/"

population_file_saved="try01.dill"
population_file_base="test_9pieces.txt"
size_line=3
total = size_line * size_line
corner_pos = [0, size_line - 1, total - size_line, total - 1]
border_bot_pos = range(corner_pos[2] + 1, corner_pos[3])
border_top_pos = range(corner_pos[0] + 1, corner_pos[1])
border_left_pos = range(corner_pos[0] + size_line, corner_pos[2], size_line)
border_right_pos = range(corner_pos[1] + size_line, corner_pos[3], size_line)
border_pos = border_top_pos + border_bot_pos  + border_left_pos + border_right_pos
inside_pos = [x for x in range(0, total) if x not in corner_pos and x not in border_pos]

score_group_max = 4 * total
NGEN = 100
NPOPULATION = 10


mutate_inpd=0.4
selection_ind_value_step=1
elitism_percentage=10
