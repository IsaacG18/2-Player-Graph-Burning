import normal_graph_sim as ngs
import numpy as np
import copy
class Node:
    def __init__(self, choice=None, ver_colour=None, value=None, children=None):
        self.value = value
        self.choice = choice   
        self.children = children if children is not None else []
        self.ver_colour = ver_colour


def minimax_alpha_beta_return_all_best(node, depth, alpha, beta, maximizing_player):
    if not node.children or depth == 0:
        return node.value, node.choice

    if maximizing_player:
        max_eval = float('-inf')
        max_choice = list()
        for child in node.children:
            eval, choice = minimax_alpha_beta_return_all_best(child, depth - 1, alpha, beta, False)
            if (max_eval < eval):
                max_choice = [choice]
                max_eval =  eval
            elif (max_eval == eval):                
                max_choice.append(choice)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  
        return max_eval, (node.choice, max_choice)
    else:
        min_eval = float('inf')
        min_choice = list()
        for child in node.children:
            eval, choice = minimax_alpha_beta_return_all_best(child, depth - 1, alpha, beta, True)
            if (min_eval > eval):
                min_choice = [choice]
                min_eval =  eval
            elif (min_eval == eval):
                min_choice.append(choice)
            beta = min(beta, eval)
            if beta <= alpha:
                break 
        return min_eval, (node.choice, min_choice)


def minimax_alpha_beta(node, depth, alpha, beta, maximizing_player):
    if not node.children or depth == 0:
        return node.value, [node.choice]

    if maximizing_player:
        max_eval = float('-inf')
        max_choice = []
        for child in node.children:
            eval, choice = minimax_alpha_beta(child, depth - 1, alpha, beta, False)
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
            eval, choice = minimax_alpha_beta(child, depth - 1, alpha, beta, True)
            if (min_eval > eval):
                min_choice = choice
                min_eval =  eval
            beta = min(beta, eval)
            if beta <= alpha:
                break 
        return min_eval, [node.choice] + min_choice

def generate_tree(adj_mat, depth, ver_colours, red):
    root_node = Node([],0, ver_colours)
    update_tree(adj_mat, ver_colours, root_node, depth, red)
    return root_node

def get_value(ver_colours):
    return np.count_nonzero(ver_colours == ngs.RED_NUMBER) - np.count_nonzero(ver_colours == ngs.BLUE_NUMBER)
    


def update_tree(adj_mat, ver_colours, parent, depth, red):
    if depth <= 0:
        return
    if red:
        max_value = float("-inf")
        for i in np.where(ver_colours == 0)[0]:
            red_cur = np.copy(ver_colours)
            red_cur[i] += ngs.RED_NUMBER
            cur_red_node = Node(i, red_cur)
            parent.children.append(cur_red_node)
            update_tree(adj_mat, red_cur, cur_red_node, depth-1, False)
            if cur_red_node.children == []:
                cur_red_node.value = get_value(red_cur)
            parent.value = max(max_value, cur_red_node.value)
            max_value = max(max_value, cur_red_node.value)
    else:
        min_value = float('inf')
        for j in np.where(ver_colours == 0)[0]:
            blue_cur = np.copy(ver_colours)
            blue_cur[j] += ngs.BLUE_NUMBER
            ngs.burn_graph(adj_mat, blue_cur)
            cur_blue_node = Node(j, blue_cur)
            parent.children.append(cur_blue_node)
            update_tree(adj_mat, blue_cur, cur_blue_node, depth-1, True)
            if cur_blue_node.children == []:
                cur_blue_node.value = get_value(blue_cur)
            parent.value = min(min_value, cur_blue_node.value)
            min_value = min(min_value, cur_blue_node.value)


def generate_tree_mini_max(adj_mat, depth, ver_colours, red):
    root_node = Node([],0, ver_colours)
    update_tree_mini_max(adj_mat, ver_colours, root_node, depth, red)
    return root_node
    


def update_tree_mini_max(adj_mat, ver_colours, parent, depth, red):
    if depth <= 0:
        return
    if red:
        max_value = float("-inf")
        for i in np.where(ver_colours == 0)[0]:
            red_cur = np.copy(ver_colours)
            red_cur[i] += ngs.RED_NUMBER
            cur_red_node = Node(i, red_cur)
            parent.children.append(cur_red_node)
            update_tree_mini_max(adj_mat, red_cur, cur_red_node, depth-1, False)
            if cur_red_node.children == []:
                cur_red_node.value = get_value(red_cur)
            parent.value = max(max_value, cur_red_node.value)
            max_value = max(max_value, cur_red_node.value)
            if max_value > 0:
                return
    else:
        min_value = float('inf')
        for j in np.where(ver_colours == 0)[0]:
            blue_cur = np.copy(ver_colours)
            blue_cur[j] += ngs.BLUE_NUMBER
            ngs.burn_graph(adj_mat, blue_cur)
            cur_blue_node = Node(j, blue_cur)
            parent.children.append(cur_blue_node)
            update_tree_mini_max(adj_mat, blue_cur, cur_blue_node, depth-1, True)
            if cur_blue_node.children == []:
                cur_blue_node.value = get_value(blue_cur)
            parent.value = min(min_value, cur_blue_node.value)
            min_value = min(min_value, cur_blue_node.value)
            if min_value < 0:
                return
        


def generate_tree_hashmap(adj_mat, depth, ver_colours, red, map = {}):
    root_node = Node([],0, ver_colours)
    generate_tree_hashmap(adj_mat, ver_colours, root_node, depth, red, map)
    return root_node
    
    


def update_tree_hashmap(adj_mat, ver_colours, parent, depth, red, map):
    if depth <= 0:
        return
    if red:
        max_value = float("-inf")
        for i in np.where(ver_colours == 0)[0]:
            red_cur = np.copy(ver_colours)
            red_cur[i] += ngs.RED_NUMBER
            if tuple(red_cur) in map:
                cur_red_node = map[tuple(red_cur)]
                parent.value = max(max_value, cur_red_node.value)
                max_value = max(max_value, cur_red_node.value)
            else:
                cur_red_node = Node(i, red_cur)
                parent.children.append(cur_red_node)
                update_tree_hashmap(adj_mat, red_cur, cur_red_node, depth-1, False, map)
                if cur_red_node.children == []:
                    cur_red_node.value = get_value(red_cur)
                map[tuple(red_cur)] = cur_red_node
                parent.value = max(max_value, cur_red_node.value)
                max_value = max(max_value, cur_red_node.value)
                
    else:
        min_value = float('inf')
        for j in np.where(ver_colours == 0)[0]:
            blue_cur = np.copy(ver_colours)
            blue_cur[j] += ngs.BLUE_NUMBER
            ngs.burn_graph(adj_mat, blue_cur)
            if tuple(blue_cur) in map:
                cur_blue_node = map[tuple(blue_cur)]
                parent.value = min(min_value, cur_blue_node.value)
                min_value = min(min_value, cur_blue_node.value)
            else:
                cur_blue_node = Node(j, blue_cur)
                parent.children.append(cur_blue_node)
                update_tree_mini_max(adj_mat, blue_cur, cur_blue_node, depth-1, True, map)
                if cur_blue_node.children == []:
                    cur_blue_node.value = get_value(blue_cur)
                map[tuple(blue_cur)] = cur_blue_node
                parent.value = min(min_value, cur_blue_node.value)
                min_value = min(min_value, cur_blue_node.value)


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


def create_path_graph_adj_matrix(n):
    adj_matrix = np.zeros((n, n), dtype=int)
    for i in range(n - 1):
        adj_matrix[i, i + 1] = 1
        adj_matrix[i + 1, i] = 1
    return adj_matrix

matrix = create_path_graph_adj_matrix(7)
matrix[1,0], matrix[0,1] = 0, 0
matrix[0,2], matrix[2,0] = 1, 1
ver_colours = np.zeros(matrix.shape[0])
# names = np.arange(ver_colours.shape[0])
# ngs.create_graph(matrix, ver_colours, names)
# root = generate_tree(matrix, 1000, np.zeros(matrix.shape[0]), True)
# print_tree(root)

def get_child(root, choice):
    for child in root.children:
        if child.choice == choice:
            return child
    return None

def play_game(matrix, ver_colours):
    names = np.arange(ver_colours.shape[0])
    root = generate_tree(matrix, 100, np.zeros(matrix.shape[0]), True)
    cur_node = copy.deepcopy(root)
    cur_ver_colours = np.copy(ver_colours)
    input_value = -2
    while input_value != -1:
        if np.all(cur_ver_colours != 0):
            print("Game Over, final score is: ", get_value(cur_ver_colours))
            ngs.create_graph(matrix, cur_ver_colours, names)
            cur_ver_colours = np.copy(ver_colours)
            cur_node = copy.deepcopy(root)
        ngs.create_graph(matrix, cur_ver_colours, names)
        try:
            input_value = int(input("Enter choice or quit by entering -1: "))
            if input_value < 0  or input_value >= cur_ver_colours.shape[0] or cur_ver_colours[input_value] != 0:
                if input_value == -1:
                    print("Quitting...")
                else:
                    print("Not a value input")
                continue
            cur_node = get_child(cur_node, input_value)
            cur_ver_colours[input_value] += ngs.RED_NUMBER
            if np.any(cur_ver_colours == 0):
                minimax_value = minimax_alpha_beta(cur_node, 1, -10000, 10000, False)
                print("Current player 2 Score: ",  minimax_value[0])
                cur_node = get_child(cur_node, minimax_value[1][1])
                cur_ver_colours[minimax_value[1][1]] += ngs.BLUE_NUMBER
                ngs.burn_graph(matrix, cur_ver_colours)
            

            
        except ValueError:
            print("Not a value input")
        

    
play_game(matrix, ver_colours)
# print(minimax_alpha_beta(root, 10, -100, 100, True))