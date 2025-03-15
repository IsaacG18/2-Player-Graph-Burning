import numpy as np
import normal_graph_sim as ngs
import generate_naive_strategies as gns
import random

GREEN_NUMBER = -1

def heuristic_k_neighbour(adj_mat, ver_colours, red_player, turns):
    best_choice = -1
    if red_player:
        best_value = float('-inf')
        for i in np.random.permutation(np.where(ver_colours == 0)[0]):
            small_value = float('inf')
            for j in np.random.permutation(np.where(ver_colours == 0)[0]):
                if i != j:
                    current = np.copy(ver_colours)
                    current[i] += ngs.RED_NUMBER
                    current[j] += ngs.BLUE_NUMBER
                    for t in range(turns):
                        ngs.burn_graph(adj_mat, current)
                    small_value = min(ngs.get_value(current), small_value)
            if small_value > best_value:
                best_choice, best_value = i, small_value
    else:
        best_value = float('inf')
        for i in np.random.permutation(np.where(ver_colours == 0)[0]):
            current = np.copy(ver_colours)
            current[i] += ngs.BLUE_NUMBER
            for t in range(turns):
                ngs.burn_graph(adj_mat, current)
            value = ngs.get_value(current)
            if value<best_value:
                best_choice, best_value = i, value
    return best_choice


def fix_depth_minimax(adj_mat, ver_colours, red_player, turns):
    return random.choice(gns.minimax_alpha_beta_return_all_best(gns.generate_tree(adj_mat, turns, ver_colours, red_player), 1 , red_player)[1][1])

def heuristic_isolated_burn(adj_mat, ver_colours, func):
    best = (float("-inf"), float("inf"), -1)
    for i in np.random.permutation(np.where(ver_colours == 0)[0]):
        turns, last, first = 0, 0, True
        current = np.copy(ver_colours)
        current[i] += GREEN_NUMBER
        while last - np.sum(current)!= 0 or first:
            if first == True:
                first = False
            last = np.sum(current)
            green = np.max(adj_mat[np.where(current == GREEN_NUMBER)], 0)
            green[np.where(current!=0)]=0
            current += green*GREEN_NUMBER
            turns += 1
        best = func(best, (np.sum(current == GREEN_NUMBER), turns, i))
    return best

def better_than_value(play1, play2):
    if play2[0]>play1[0]:
        return play2
    if play2[0] == play1[0] and play2[1] < play1[1]:
        return play2
    return play1
        
def heuristic_simulated_burn(adj_mat, ver_colours, red_player, func):
    best = (float("-inf"), float("inf"), -1) 
    for i in np.random.permutation(np.where(ver_colours == 0)[0]):
        turns, last, first = 0, 0, True
        current = np.copy(ver_colours)
        if red_player:
            current[i] += ngs.RED_NUMBER
        else:
            current[i] += ngs.BLUE_NUMBER
        while last - np.sum(current)!= 0 or first:
            turns += 1
            if first == True:
                first = False
            last = np.sum(current)
            ngs.burn_graph(adj_mat, current)
        if red_player:
            best = func(best, (ngs.get_value(current), turns, i))
        else:
            best = func(best, (-ngs.get_value(current), turns, i))
    return best

def neighbourhood_heuristic(adj_mat, ver_colours):
    row_sums = np.sum(adj_mat, axis=1)
    zero_colour_indices = np.where(ver_colours == 0)[0]
    if len(zero_colour_indices) == 0:
        return None
    max_index = zero_colour_indices[np.argmax(row_sums[zero_colour_indices])]
    
    return max_index