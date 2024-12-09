import normal_graph_sim as ngs
import numpy as np
import copy



def get_child(root, choice):
    for child in root.children:
        if child.choice == choice:
            return child
    return None
def play_game(matrix, ver_colours):
    names = np.arange(ver_colours.shape[0])
    root = ngs.generate_tree(matrix, float('inf'), np.zeros(matrix.shape[0]), True)
    cur_node = copy.deepcopy(root)
    cur_ver_colours = np.copy(ver_colours)
    input_value = -2
    while input_value != -1:
        if np.all(cur_ver_colours != 0):
            print("Game Over, final score is: ", ngs.get_value(cur_ver_colours))
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
                minimax_value = ngs.minimax_alpha_beta(cur_node, 1, -10000, 10000, False)
                print("Current player 2 Score: ",  minimax_value[0])
                cur_node = get_child(cur_node, minimax_value[1][1])
                cur_ver_colours[minimax_value[1][1]] += ngs.BLUE_NUMBER
                ngs.burn_graph(matrix, cur_ver_colours)
            
            
        except ValueError:
            print("Not a value input")