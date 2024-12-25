import normal_graph_sim as ngs
import numpy as np
import copy
import generate_naive_strategies as gns
import holsticSearch as hs
import misc as m
import instatuated_player as ip
import time
import math



# Play a game against the Navie optimial strategy
# A player can do -1 to escape or enter a node value to play
# Once the game is done it will start over again
# The human player always goes first
# Only loads the stategy on the first game
def play_game_optermised(matrix, ver_colours):
    root = ngs.generate_tree(matrix, float('inf'), np.zeros(matrix.shape[0]), True)
    cur_node = copy.deepcopy(root)
    cur_ver_colours = np.copy(ver_colours)
    input_value = -2
    while input_value != -1:
        if np.all(cur_ver_colours != 0):
            print("Game Over, final score is: ", ngs.get_value(cur_ver_colours))
            ngs.create_graph(matrix, cur_ver_colours)
            cur_ver_colours = np.copy(ver_colours)
            cur_node = copy.deepcopy(root)
        ngs.create_graph(matrix, cur_ver_colours)
        try:
            input_value = int(input("Enter choice or quit by entering -1: "))
            if input_value < 0  or input_value >= cur_ver_colours.shape[0] or cur_ver_colours[input_value] != 0:
                if input_value == -1:
                    print("Quitting...")
                else:
                    print("Not a value input")
                continue
            cur_node = cur_node.get_child(input_value)
            cur_ver_colours[input_value] += ngs.RED_NUMBER
            if np.any(cur_ver_colours == 0):
                minimax_value = ngs.minimax_alpha_beta(cur_node, 1, False)
                print("Current player 2 Score: ",  minimax_value[0])
                cur_node = cur_node.get_child(cur_node, minimax_value[1][1])
                cur_ver_colours[minimax_value[1][1]] += ngs.BLUE_NUMBER
                ngs.burn_graph(matrix, cur_ver_colours)
            
            
        except ValueError:
            print("Not a value input")


#Player class which is a class to store a stragegy 
class player:
    def __init__(self, setup_fun, play_fun, update_fun, args):
        self.setup_fun = setup_fun
        self.play_fun = play_fun
        self.update_fun = update_fun
        self.args = args
# Setup does any precalcution the game needs and sets up the args for play
    def setup(self, matrix, ver_colours, red_player):
        self.args = self.setup_fun(matrix, ver_colours, red_player, self.args)

# Plays a turn of the game and returns the play, updates the args if nesseary
    def play(self):
        self.args, play = self.play_fun(self.args)
        return play 
# Update takes in the other players move and updates thea args
    def update(self, play):
        self.args = self.update_fun(self.args, play)


# Run takes in 2 different players, a game matrix, vertex colour array for the game and bool on to displaying
# Run players a game with 2 stragies
# Returns the final vertex colour array 
def run(p1, p2, matrix, ver_colours, display):
    play = 0
    if np.any(ver_colours == 0):
        p1.setup(matrix, ver_colours, True)
        play = p1.play()
        ver_colours[play] += ngs.RED_NUMBER
    if np.any(ver_colours == 0):
        p2.setup(matrix, ver_colours, False)
        play = p2.play()
        p1.update(play)
        ver_colours[play] += ngs.BLUE_NUMBER
        ngs.burn_graph(matrix, ver_colours)
    while np.any(ver_colours == 0):
        if display:
            ngs.create_graph(matrix, ver_colours)
        play = p1.play()
        p2.update(play)
        ver_colours[play] += ngs.RED_NUMBER
        if np.any(ver_colours == 0):
            play = p2.play()
            p1.update(play)
            ver_colours[play] += ngs.BLUE_NUMBER
            ngs.burn_graph(matrix, ver_colours)
            
    if display:
        ngs.create_graph(matrix, ver_colours)
    return ngs.get_value(ver_colours)

# Run Timer takes in 2 different players, a game matrix, vertex colour array for the game and bool on to displaying
# Run players a game with 2 stragies timing each step for each player 
# Returns the final vertex colour array returns the final times in 2 dictionaries        
def run_timer(p1, p2, matrix, ver_colours, display):
    p1_times = {'setup': 0, 'update': 0, 'play': 0}
    p2_times = {'setup': 0, 'update': 0, 'play': 0}

    play = 0

    if np.any(ver_colours == 0):
        start_time = time.time()
        p1.setup(matrix, ver_colours, True)
        p1_times['setup'] += time.time() - start_time

        start_time = time.time()
        play = p1.play()
        p1_times['play'] += time.time() - start_time

        ver_colours[play] += ngs.RED_NUMBER

    if np.any(ver_colours == 0):
        start_time = time.time()
        p2.setup(matrix, ver_colours, False)
        p2_times['setup'] += time.time() - start_time

        start_time = time.time()
        play = p2.play()
        p2_times['play'] += time.time() - start_time

        start_time = time.time()
        p1.update(play)
        p1_times['update'] += time.time() - start_time

        ver_colours[play] += ngs.BLUE_NUMBER
        ngs.burn_graph(matrix, ver_colours)

    while np.any(ver_colours == 0):
        if display:
            ngs.create_graph(matrix, ver_colours)

        start_time = time.time()
        play = p1.play()
        p1_times['play'] += time.time() - start_time

        start_time = time.time()
        p2.update(play)
        p2_times['update'] += time.time() - start_time

        ver_colours[play] += ngs.RED_NUMBER

        if np.any(ver_colours == 0):
            start_time = time.time()
            play = p2.play()
            p2_times['play'] += time.time() - start_time

            start_time = time.time()
            p1.update(play)
            p1_times['update'] += time.time() - start_time

            ver_colours[play] += ngs.BLUE_NUMBER
            ngs.burn_graph(matrix, ver_colours)

    if display:
        ngs.create_graph(matrix, ver_colours)

    return ngs.get_value(ver_colours), p1_times, p2_times


# Run takes in 1 players, a game matrix, vertex colour array for the game and bool to say if the human plays first
# Run players a game where each turn the human text inputs a value and the strategy decides how to play based on the state
# Returns the final vertex colour array 
def run_human(player, matrix, ver_colours, play_first):
    input_value = -2
    first_turn = True
    try:
        while input_value != -1 or np.any(ver_colours == 0):
            if play_first:
                ngs.create_graph(matrix, ver_colours)
                input_value = int(input("Enter choice or quit by entering -1: "))
                if input_value < 0  or input_value >= ver_colours.shape[0] or ver_colours[input_value] != 0:
                    if input_value == -1:
                        print("Quitting...")
                    else:
                        print("Not a value input")
                    continue
                ver_colours[input_value] += ngs.RED_NUMBER
                if first_turn:
                    player.setup(matrix, ver_colours, False)
                    first_turn=False
                else:
                    player.update(input_value)
                if np.any(ver_colours == 0):
                    ver_colours[player.play()] += ngs.BLUE_NUMBER
                    ngs.burn_graph(matrix, ver_colours)
            else:
                if first_turn:
                    player.setup(matrix, ver_colours, True)
                    first_turn=False
                ver_colours[player.play()] += ngs.RED_NUMBER_NUMBER
                if np.any(ver_colours == 0):
                    ngs.create_graph(matrix, ver_colours)
                    input_value = int(input("Enter choice or quit by entering -1: "))
                    if input_value < 0  or input_value >= ver_colours.shape[0] or ver_colours[input_value] != 0:
                        if input_value == -1:
                            print("Quitting...")
                        else:
                            print("Not a value input")
                        continue
                    ver_colours[input_value] += ngs.BLUE_NUMBER
                    ngs.burn_graph(matrix, ver_colours)
    except ValueError:
        print("Not a value input")
            
total = 0    
for i in range(10):
    matrix = m.create_path_graph_adj_matrix(30)
    ver_colours = np.zeros(matrix.shape[0])
    # p1 = player(ip.setup_gns, ip.play_gns, ip.update_gns, [float("inf")])
    # p2 = player(ip.setup_default, ip.play_hmc, ip.update_default, [3])
    # p3 = player(ip.setup_hma, ip.play_hma, ip.update_default, [3])
    # p4 = player(ip.setup_mc, ip.play_mc, ip.update_mc, [100,math.sqrt(2)])
    p5 = player(ip.setup_random, ip.play_random, ip.update_default, [])
    p6 = player(ip.setup_default, ip.play_hihb, ip.update_default, [hs.betterThanValue])
    p7 = player(ip.setup_default, ip.play_hhb, ip.update_default, [hs.betterThanValue])
    total += run(p7, p5, matrix, ver_colours, False)
    if i % 10 == 0:
        print(i)
print(total)