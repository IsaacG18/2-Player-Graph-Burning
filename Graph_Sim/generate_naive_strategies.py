import normal_graph_sim as ngs
import numpy as np
import copy
class Node:
    def __init__(self, choice=None, ver_colour=None, value=None, children=None):
        self.value = value
        self.choice = choice   
        self.children = children if children is not None else []
        self.ver_colour = ver_colour


    def get_child(self, choice):
        for child in self.children:
            if child.choice == choice:
                return child
        return None
    

    
    
def minimax_alpha_beta_return_all_best(node, depth, maximizing_player, alpha=float('-inf'), beta= float('inf')):
    if not node.children or depth == 0:
        return node.value, node.choice

    if maximizing_player:
        max_eval = float('-inf')
        max_choice = list()
        for child in node.children:
            eval, choice = minimax_alpha_beta_return_all_best(child, depth - 1, False, alpha, beta)
            if (max_eval < eval):
                max_choice = [choice]
                max_eval =  eval
                alpha = max(alpha, eval)
            elif (max_eval == eval):                
                max_choice.append(choice)
            if beta <= alpha:
                break  
        return max_eval, (node.choice, max_choice)
    else:
        min_eval = float('inf')
        min_choice = list()
        for child in node.children:
            eval, choice = minimax_alpha_beta_return_all_best(child, depth - 1, True, alpha, beta)
            if (min_eval > eval):
                min_choice = [choice]
                min_eval =  eval
                beta = min(beta, eval)
            elif (min_eval == eval):
                min_choice.append(choice)
            if beta <= alpha:
                break 
        return min_eval, (node.choice, min_choice)


def minimax_alpha_beta(node, depth, maximizing_player, alpha=float('-inf'), beta= float('inf')):
    if not node.children or depth == 0:
        return node.value, [node.choice]

    if maximizing_player:
        max_eval = float('-inf')
        max_choice = []
        for child in node.children:
            eval, choice = minimax_alpha_beta(child, depth - 1, False, alpha, beta)
            if (max_eval < eval):
                max_choice = choice
                max_eval =  eval
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, [node.choice] + max_choice
    else:
        min_eval = float('inf')
        min_choice = []
        for child in node.children:
            eval, choice = minimax_alpha_beta(child, depth - 1, True, alpha, beta)
            if (min_eval > eval):
                min_choice = choice
                min_eval =  eval
            beta = min(beta, eval)
            if beta <= alpha:
                break 
        return min_eval, [node.choice] + min_choice



def play_red(ver_colours,i, parent):
    red_cur = np.copy(ver_colours)
    red_cur[i] += ngs.RED_NUMBER
    cur_red_node = Node(i, red_cur)
    parent.children.append(cur_red_node)
    return red_cur, cur_red_node

def play_blue(ver_colours,j, parent, adj_mat):
    blue_cur = np.copy(ver_colours)
    blue_cur[j] += ngs.BLUE_NUMBER
    ngs.burn_graph(adj_mat, blue_cur)
    cur_blue_node = Node(j, blue_cur)
    parent.children.append(cur_blue_node)
    return blue_cur, cur_blue_node

def red_leaf_node_value(cur_red_node, red_cur, max_value):
    if cur_red_node.children == []:
        cur_red_node.value = ngs.get_value(red_cur)
    return max(max_value, cur_red_node.value)

def blue_leaf_node_value(cur_blue_node, blue_cur, min_value):
    if cur_blue_node.children == []:
        cur_blue_node.value = ngs.get_value(blue_cur)
    return min(min_value, cur_blue_node.value)
    

def generate_tree(adj_mat, depth, ver_colours, red):
    root_node = Node([],0, ver_colours)
    update_tree(adj_mat, ver_colours, root_node, depth, red)
    return root_node

def update_tree(adj_mat, ver_colours, parent, depth, red):
    if depth <= 0:
        return
    if red:
        max_value = float("-inf")
        for i in np.where(ver_colours == 0)[0]:
            red_cur, cur_red_node = play_red(ver_colours,i, parent)
            update_tree(adj_mat, red_cur, cur_red_node, depth-1, False)
            max_value = red_leaf_node_value(cur_red_node, red_cur, max_value)
            parent.value = max_value
    else:
        min_value = float('inf')
        for j in np.where(ver_colours == 0)[0]:
            blue_cur, cur_blue_node = play_blue(ver_colours,j, parent, adj_mat)
            update_tree(adj_mat, blue_cur, cur_blue_node, depth-1, True)
            if cur_blue_node.children == []:
                cur_blue_node.value = ngs.get_value(blue_cur)
            min_value = blue_leaf_node_value(cur_blue_node, blue_cur, min_value)
            parent.value = min_value



def generate_tree_mini_max(adj_mat, depth, ver_colours, red, choice = 0):
    root_node = Node([],choice, ver_colours)
    update_tree_mini_max(adj_mat, ver_colours, root_node, depth, red)
    return root_node
    


def update_tree_mini_max(adj_mat, ver_colours, parent, depth, red):
    if depth <= 0:
        return
    if red:
        max_value = float("-inf")
        for i in np.where(ver_colours == 0)[0]:
            red_cur, cur_red_node = play_red(ver_colours,i, parent)
            update_tree_mini_max(adj_mat, red_cur, cur_red_node, depth-1, False)
            max_value = red_leaf_node_value(cur_red_node, red_cur, max_value)
            parent.value = max_value
            if max_value > 0:
                return
    else:
        min_value = float('inf')
        for j in np.where(ver_colours == 0)[0]:
            blue_cur, cur_blue_node = play_blue(ver_colours,j, parent, adj_mat)
            update_tree_mini_max(adj_mat, blue_cur, cur_blue_node, depth-1, True)
            min_value = blue_leaf_node_value(cur_blue_node, blue_cur, min_value)
            parent.value = min_value
            if min_value < 0:
                return
        






def print_tree(node, level=0):
    indent = ' ' * (level * 4)  
    if node.value is not None:
        if level %2 == 1:
            print(f"{indent}Red: {node.value} {node.choice}")
        else:
            print(f"{indent}Blue: {node.value} {node.choice}")     
    else:
        print(f"{indent}Node:")

    for child in node.children:
        print_tree(child, level + 1)

def total_leafs(node):
    total = 0
    if node.children == []:
        return 1
    for child in node.children:
        total += total_leafs(child)
    return total