import numpy as np
import normal_graph_sim as ngs
import holsticSearch as hs
import generate_naive_strategies as gns
import random


def heuristicBurnList(adj_mat, ver_colours, red_player):
    return_list = []
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
            return_list.append((ngs.get_value(current), turns, i))
        else:
            return_list.append((-ngs.get_value(current), turns, i))
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
    

def priority_search_mini_max(adj_mat, depth, ver_colours, red_player, max, func_list, func_sort, choice = 0):
    root_node = gns.Node([],choice, ver_colours)
    if max:
        update_tree_max_priority(adj_mat, ver_colours, root_node, depth, red_player, func_list, func_sort)
    else:
        update_tree_mini_priority(adj_mat, ver_colours, root_node, depth, red_player, func_list, func_sort)
    return root_node
    


def update_tree_max_priority(adj_mat, ver_colours, parent, depth, red_player, func_list, func_sort):
    if depth <= 0:
        return
    if red_player:
        max_value = float("-inf")
        children =  sort_list(func_list(adj_mat, ver_colours, red_player), func_sort)
        for _,_,i in children:
            red_cur, cur_red_node = gns.play_red(ver_colours,i, parent)
            update_tree_max_priority(adj_mat, red_cur, cur_red_node, depth-1, False, func_list, func_sort)
            if cur_red_node.children == []:
                cur_red_node.value = ngs.get_value(red_cur)
            parent.value = max(max_value, cur_red_node.value)
            max_value = max(max_value, cur_red_node.value)
            if max_value > 0:
                return
    else:
        min_value = float('inf')
        for j in np.where(ver_colours == 0)[0]:
            blue_cur, cur_blue_node = gns.play_blue(ver_colours,j, parent, adj_mat)
            update_tree_max_priority(adj_mat, blue_cur, cur_blue_node, depth-1, True, func_list, func_sort)
            min_value = gns.blue_leaf_node_value(cur_blue_node, blue_cur, min_value)
            parent.value = min_value
            if min_value < 0:
                return
            

def update_tree_mini_priority(adj_mat, ver_colours, parent, depth, red_player, func_list, func_sort):
    if depth <= 0:
        return
    if red_player:
        max_value = float("-inf")
        for i in np.where(ver_colours == 0)[0]:
            red_cur, cur_red_node = gns.play_red(ver_colours,i, parent)
            update_tree_mini_priority(adj_mat, red_cur, cur_red_node, depth-1, False, func_list, func_sort)
            max_value = gns.red_leaf_node_value(cur_red_node, red_cur, max_value)
            parent.value = max_value
            if max_value > 0:
                return
    else:
        min_value = float('inf')
        children = sort_list(func_list(adj_mat, ver_colours, red_player), func_sort)
        for _,_,j in children:
            blue_cur, cur_blue_node = gns.play_blue(ver_colours,j, parent, adj_mat)
            update_tree_mini_priority(adj_mat, blue_cur, cur_blue_node, depth-1, True, func_list, func_sort)
            min_value = gns.blue_leaf_node_value(cur_blue_node, blue_cur, min_value)
            parent.value = min_value
            if min_value < 0:
                return

