import numpy as np
import normal_graph_sim as ngs
import alpha_beta as ab

def holticMostConnected(adj_mat, ver_colours, red_player, turns):
    best_choice = -1
    if red_player:
        best_value = float('-inf')
        for i in np.where(ver_colours == 0)[0]:
            small_value = float('inf')
            for j in np.where(ver_colours == 0)[0]:
                if i != j:
                    current = np.copy(ver_colours)
                    current[i] += ngs.RED_NUMBER
                    current[j] += ngs.BLUE_NUMBER
                    for i in range(turns):
                        ngs.burn_graph(adj_mat, current)
                    small_value = min(ngs.get_value(current), small_value)
            if small_value > best_value:
                best_choice, best_value = i, small_value
    else:
        best_value = float('inf')
        for i in np.where(ver_colours == 0)[0]:
            current = np.copy(ver_colours)
            current[i] += ngs.BLUE_NUMBER
            for i in range(turns):
                ngs.burn_graph(adj_mat, current)
            value = ngs.get_value(current)
            if value<best_value:
                best_choice, best_value = i, value
    return best_choice


def holticMostAdvantages(adj_mat, ver_colours, red_player, turns, map):
    return ab.minimax_alpha_beta(ab.generate_tree_hashmap(adj_mat, turns, ver_colours, red_player, map), 1 , red_player)[0]