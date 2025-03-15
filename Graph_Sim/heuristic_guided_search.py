import numpy as np
import normal_graph_sim as ngs
import heurstic_search as hs
import generate_naive_strategies as gns
import random

GREEN_NUMBER = -1


def neighbourhood_burn_list(adj_mat, ver_colours, red_player):
    return_list = []
    for i in np.random.permutation(np.where(ver_colours == 0)[0]):
        turns = 1
        current = np.copy(ver_colours)
        if red_player:
            current[i] += ngs.RED_NUMBER
        else:
            current[i] += ngs.BLUE_NUMBER
        ngs.burn_graph(adj_mat, current)
        if red_player:
            return_list.append((ngs.get_value(current), turns, i))
        else:
            return_list.append((-ngs.get_value(current), turns, i))
    return return_list 

def neighbourhood_list(adj_mat, ver_colours, red_player):
    return_list = []
    row_sums = np.sum(adj_mat, axis=1)
    for i in np.random.permutation(np.where(ver_colours == 0)[0]):
        return_list.append((row_sums[i], 1, i))
    return return_list 

def best_play_list(adj_mat, ver_colours, red_player):
    return_list = []
    for i in np.random.permutation(np.where(ver_colours == 0)[0]):
        turns = 1
        value = 0
        current = np.copy(ver_colours)
        if red_player:
            current[i] += ngs.RED_NUMBER
            for j in np.random.permutation(np.where(current == 0)[0]):
                blue_play = np.copy(current)
                blue_play[j] += ngs.BLUE_NUMBER
                ngs.burn_graph(adj_mat, blue_play)
                value = min(value, ngs.get_value(blue_play))

        else:
            current[i] += ngs.BLUE_NUMBER
            ngs.burn_graph(adj_mat, current)
            value = ngs.get_value(current)
        
        ngs.burn_graph(adj_mat, current)
        if red_player:
            return_list.append((ngs.get_value(current), turns, i))
        else:
            return_list.append((-value, turns, i))
    return return_list 


def heuristic_simulated_burn_list(adj_mat, ver_colours, red_player):
    return_list = []
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
            return_list.append((ngs.get_value(current), turns, i))
        else:
            return_list.append((-ngs.get_value(current), turns, i))
    return return_list 

def heuristic_isolated_burn_list(adj_mat, ver_colours, red_player):
    return_list = []
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
        return_list.append((np.sum(current == GREEN_NUMBER), turns, i))
    return return_list 


def sort_list(list, func):
    if len(list) <= 1:
        return list
    pivot_index = random.randint(0, len(list) - 1)
    pivot = list[pivot_index]
    less, greater = [], []
    for x in list:
        if x ==pivot:
            continue
        if x==func(pivot, x):
            greater.append(x)
        else:
            less.append(x)
    return sort_list(greater, func)+ [pivot] + sort_list(less, func)
    

def guided_priority_dfs(adj_mat, depth, ver_colours, red_player, func_list, func_sort, choice = 0):
    root_node = gns.Node([],choice, ver_colours)
    update_tree_priority(adj_mat, ver_colours, root_node, depth, red_player, func_list, func_sort)
    return root_node


def update_tree_priority(adj_mat, ver_colours, parent, depth, red_player, func_list, func_sort):
    if depth <= 0:
        return
    if red_player:
        max_value = float("-inf")
        children =  sort_list(func_list(adj_mat, ver_colours, red_player), func_sort)
        for _,_,i in children:
            red_cur, cur_red_node = gns.play_red(ver_colours,i, parent)
            update_tree_priority(adj_mat, red_cur, cur_red_node, depth-1, False, func_list, func_sort)
            if cur_red_node.children == []:
                cur_red_node.value = ngs.get_value(red_cur)
            parent.value = max(max_value, cur_red_node.value)
            max_value = max(max_value, cur_red_node.value)
            if max_value > 0:
                return
    else:
        min_value = float('inf')
        children = sort_list(func_list(adj_mat, ver_colours, red_player), func_sort)
        for _,_,j in children:
            blue_cur, cur_blue_node = gns.play_blue(ver_colours,j, parent, adj_mat)
            update_tree_priority(adj_mat, blue_cur, cur_blue_node, depth-1, True, func_list, func_sort)
            min_value = gns.blue_leaf_node_value(cur_blue_node, blue_cur, min_value)
            parent.value = min_value
            if min_value < 0:
                return



def filter_dfs(adj_mat, depth, ver_colours, red_player, func_list, func_sort, choice = 0):
    root_node = gns.Node([],choice, ver_colours)
    update_tree_filter(adj_mat, ver_colours, root_node, depth, red_player, func_list, func_sort)
    return root_node


def update_tree_filter(adj_mat, ver_colours, parent, depth, red_player, func_list, func_sort):
    count = 0
    if depth <= 0:
        return
    if red_player:
        max_value = float("-inf")
        children =  sort_list(func_list(adj_mat, ver_colours, red_player), func_sort)
        for _,_,i in children:
            
            red_cur, cur_red_node = gns.play_red(ver_colours,i, parent)
            update_tree_filter(adj_mat, red_cur, cur_red_node, depth-1, False, func_list, func_sort)
            if cur_red_node.children == []:
                cur_red_node.value = ngs.get_value(red_cur)
            parent.value = max(max_value, cur_red_node.value)
            max_value = max(max_value, cur_red_node.value)
            if max_value > 0:
                return
            count += 1
            if len(children)/2<count:
                return
    else:
        min_value = float('inf')
        children = sort_list(func_list(adj_mat, ver_colours, red_player), func_sort)
        for _,_,j in children:
            blue_cur, cur_blue_node = gns.play_blue(ver_colours,j, parent, adj_mat)
            update_tree_filter(adj_mat, blue_cur, cur_blue_node, depth-1, True, func_list, func_sort)
            min_value = gns.blue_leaf_node_value(cur_blue_node, blue_cur, min_value)
            parent.value = min_value
            if min_value < 0:
                return
            count += 1
            if len(children)/2<count:
                return
