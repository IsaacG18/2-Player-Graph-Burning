import normal_graph_sim as ngs
import numpy as np
import copy
class Node:
    def __init__(self, choice={}, ver_colour=None, value=None, children=None):
        self.value = value
        self.choice = choice   
        self.children = children if children is not None else []
        self.ver_colour = ver_colour


    def get_child(self, choice):
        for child in self.children:
            for states in child.choice:
                if child.choice[states] == choice:
                    return child
        return None
    
    def get_child_by_ver(self, ver_colour):
        for child in self.children:
            if np.array_equal(child.ver_colour, ver_colour):
                return child
        return None
    

def minimax_alpha_beta_hash(node, maximizing_player, curr_ver):
    if not node.children:
        return -1

    if maximizing_player:
        max_eval = float('-inf')
        max_choice = -1
        for child in node.children:
            if (max_eval < child.value):
                max_choice = child.choice[curr_ver]
                max_eval =  child.value
        return max_choice 
    else:
        min_eval = float('inf')
        min_choice = -1
        for child in node.children:
            if (min_eval > child.value):
                min_choice = child.choice[curr_ver]
                min_eval =  child.value
        return min_choice
    
def generate_tree_hashmap(adj_mat, depth, ver_colours, red, map = {}):
    root_node = Node({tuple(ver_colours):-1},0, ver_colours)
    update_tree_hashmap(adj_mat, ver_colours, root_node, depth, red, map)
    return root_node
    
def update_tree_hashmap(adj_mat, ver_colours, parent, depth, red, map):
    if depth <= 0:
        return
    if red:
        max_value = float("-inf")
        for i in np.random.permutation(np.where(ver_colours == 0)[0]):
            red_cur = np.copy(ver_colours)
            red_cur[i] += ngs.RED_NUMBER
            if tuple(red_cur) + (red,) in map:
                cur_red_node = map[tuple(red_cur) + (red,)]
                cur_red_node.choice[tuple(ver_colours)] = i
                parent.children.append(cur_red_node)
                parent.value = max(max_value, cur_red_node.value)
                max_value = max(max_value, cur_red_node.value)
            else:
                cur_red_node = Node({tuple(ver_colours):i}, red_cur)
                parent.children.append(cur_red_node)
                update_tree_hashmap(adj_mat, red_cur, cur_red_node, depth-1, False, map)
                if cur_red_node.children == []:
                    cur_red_node.value = ngs.get_value(red_cur)
                map[tuple(red_cur)  + (red,)] = cur_red_node
                parent.value = max(max_value, cur_red_node.value)
                max_value = max(max_value, cur_red_node.value)
                
    else:
        min_value = float('inf')
        for j in np.random.permutation(np.where(ver_colours == 0)[0]):
            blue_cur = np.copy(ver_colours)
            blue_cur[j] += ngs.BLUE_NUMBER
            ngs.burn_graph(adj_mat, blue_cur)
            if tuple(blue_cur) + (red,) in map:
                cur_blue_node = map[tuple(blue_cur) + (red,)]
                cur_blue_node.choice[tuple(ver_colours)] = j
                parent.children.append(cur_blue_node)
                parent.value = min(min_value, cur_blue_node.value)
                min_value = min(min_value, cur_blue_node.value)
            else:
                cur_blue_node = Node({tuple(ver_colours):j}, blue_cur)
                map[tuple(blue_cur) + (red,)] = cur_blue_node
                parent.children.append(cur_blue_node)
                update_tree_hashmap(adj_mat, blue_cur, cur_blue_node, depth-1, True, map)
                if cur_blue_node.children == []:
                    cur_blue_node.value = ngs.get_value(blue_cur)
                map[tuple(blue_cur) + (red,)] = cur_blue_node
                parent.value = min(min_value, cur_blue_node.value)
                min_value = min(min_value, cur_blue_node.value)