import numpy as np
import normal_graph_sim as ngs
import generate_naive_strategies as gns
import random

GREEN_NUMBER = -1

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
                    for t in range(turns):
                        ngs.burn_graph(adj_mat, current)
                    small_value = min(ngs.get_value(current), small_value)
            if small_value > best_value:
                best_choice, best_value = i, small_value
    else:
        best_value = float('inf')
        for i in np.where(ver_colours == 0)[0]:
            current = np.copy(ver_colours)
            current[i] += ngs.BLUE_NUMBER
            for t in range(turns):
                ngs.burn_graph(adj_mat, current)
            value = ngs.get_value(current)
            if value<best_value:
                best_choice, best_value = i, value
    return best_choice


def holticMostAdvantages(adj_mat, ver_colours, red_player, turns):
    return random.choice(gns.minimax_alpha_beta_return_all_best(gns.generate_tree(adj_mat, turns, ver_colours, red_player), 1 , red_player)[1][1])

def holsitcIsolatedHighestBurn(adj_mat, ver_colours, func):
    best_value, best_turn, best_play = float("-inf"), float("inf"), -1
    for i in np.where(ver_colours == 0)[0]:
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
        best_value, best_turn, best_play = func(best_value, best_turn, best_play, np.sum(current == GREEN_NUMBER), turns, i)
    return best_play

def betterThanValue(best_value, best_turn, best_play, cur_value, cur_turn, cur_play):
    if cur_value>best_value:
        return cur_value, cur_turn, cur_play
    if cur_value == best_value and cur_turn < best_turn:
        return cur_value, cur_turn, cur_play
    return best_value, best_turn, best_play
        
def holsitcHighestBurn(adj_mat, ver_colours, red_player, func):
    best_turn, best_play, best_value = float("inf"), -1, float("-inf")
    for i in np.where(ver_colours == 0)[0]:
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
            best_value, best_turn, best_play = func(best_value, best_turn, best_play, ngs.get_value(current), turns, i)
        else:
            best_value, best_turn, best_play = func(best_value, best_turn, best_play, -ngs.get_value(current), turns, i)
    return best_play