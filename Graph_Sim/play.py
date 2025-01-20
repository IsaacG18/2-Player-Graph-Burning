import normal_graph_sim as ngs
import numpy as np
import copy
import time
import os
import csv
import copy



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
        ver_colours[play] += ngs.BLUE_NUMBER
        ngs.burn_graph(matrix, ver_colours)
        p1.update(play)
    while np.any(ver_colours == 0):
        if display:
            ngs.create_graph(matrix, ver_colours)
        play = p1.play()
        ver_colours[play] += ngs.RED_NUMBER
        p2.update(play)
        if np.any(ver_colours == 0):
            play = p2.play()
            ver_colours[play] += ngs.BLUE_NUMBER
            ngs.burn_graph(matrix, ver_colours)
            p1.update(play)
            
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
    turns = []
    if np.any(ver_colours == 0):
        start_time = time.time()
        p1.setup(matrix, ver_colours, True)
        p1_times['setup'] += time.time() - start_time

        start_time = time.time()
        play = p1.play()
        p1_times['play'] += time.time() - start_time
        turns.append(play)
        ver_colours[play] += ngs.RED_NUMBER
    if np.any(ver_colours == 0):
        start_time = time.time()
        p2.setup(matrix, ver_colours, False)
        p2_times['setup'] += time.time() - start_time
        start_time = time.time()
        play = p2.play()
        p2_times['play'] += time.time() - start_time
        turns.append(play)

        ver_colours[play] += ngs.BLUE_NUMBER
        ngs.burn_graph(matrix, ver_colours)

        start_time = time.time()
        p1.update(play)
        p1_times['update'] += time.time() - start_time

    while np.any(ver_colours == 0):
        if display:
            ngs.create_graph(matrix, ver_colours)

        start_time = time.time()
        play = p1.play()
        p1_times['play'] += time.time() - start_time
        turns.append(play)
        ver_colours[play] += ngs.RED_NUMBER

        start_time = time.time()
        p2.update(play)
        p2_times['update'] += time.time() - start_time

        

        if np.any(ver_colours == 0):
            start_time = time.time()
            play = p2.play()
            p2_times['play'] += time.time() - start_time
            turns.append(play)
            ver_colours[play] += ngs.BLUE_NUMBER
            ngs.burn_graph(matrix, ver_colours)

            start_time = time.time()
            p1.update(play)
            p1_times['update'] += time.time() - start_time

    if display:
        ngs.create_graph(matrix, ver_colours)
    return ngs.get_value(ver_colours), p1_times, p2_times, turns


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
                ver_colours[player.play()] += ngs.RED_NUMBER
                if np.any(ver_colours == 0):
                    ngs.create_graph(matrix, ver_colours)
                    input_value = int(input("Enter choice or quit by entering -1: "))
                    while input_value < 0  or input_value >= ver_colours.shape[0] or ver_colours[input_value] != 0:
                        if input_value == -1:
                            print("Quitting...")
                            continue
                        else:
                            print("Not a value input")
                            input_value = int(input("Enter choice or quit by entering -1: "))
                    ver_colours[input_value] += ngs.BLUE_NUMBER
                    ngs.burn_graph(matrix, ver_colours)
                    player.update(input_value)
    except ValueError:
        print("Not a value input")


# write_game takes in 2 players, a csv file, and a game matrix
# write_game plays a game wtih the 2 players calling run timer then writes players names, times, games matrix and score to csv file
def write_game(p1, p2, file, folder, matrix):
    value, p1_times, p2_times, turns = run_timer(p1, p2, matrix, np.zeros(matrix.shape[0]), False)
    file_path = os.path.join(folder, file)
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([p1.get_name(), p2.get_name(), value, len(turns), turns,
                        p1_times['setup'], p1_times['update'], p1_times['play'], 
                        p1_times['setup'] + p1_times['update'] + p1_times['play'],
                        p2_times['setup'], p2_times['update'], p2_times['play'], 
                        p2_times['setup'] + p2_times['update'] + p2_times['play'], np.array2string(matrix)])


# test_players_random takes in a list of players, a nummber of vertexs, number generator, a number to split the genertor number, number times to run, and name of csv file
# test_players_random generates a matrix of a game which, every player plays against every other player on the matrix and writes it to csv file, it does this iterative times
def test_players_random(list_players, vertex_count, num_gen, split_num, iterations,file,folder):
    for _ in range(iterations):
        matrix = ngs.generate_matrix_v2(vertex_count, num_gen, split_num)
        for i in range(len(list_players)):
            for j in range(i, len(list_players)):
                if i != j:
                    write_game(list_players[i],list_players[j],file,folder,matrix)
                    write_game(list_players[j],list_players[i],file,folder,matrix)
                else:
                    write_game(list_players[i],copy.deepcopy(list_players[i]),file,folder,matrix)

# test_players_list_random takes in a list of player match ups, a nummber of vertexs, number generator, a number to split the genertor number, number times to run, and name of csv file
# test_players_list_random generates a matrix of a game which, every match up on the matrix and writes it to csv file, it does this iterative times
def test_players_list_random(list_players_vs, vertex_count, num_gen, split_num, iterations, file, folder):
    for _ in range(iterations):
        matrix = ngs.generate_matrix_v2(vertex_count, num_gen, split_num)
        for p1, p2 in list_players_vs:
            if p1 != p2:
                write_game(p1,p2,file,folder,matrix)
            else:
                write_game(p1,copy.deepcopy(p1),file,folder,matrix)

# test_players_set takes in a list of players, list of matrixs, and name of csv file
# test_players_random loops through every game matrix, every player plays against every other player on the matrix and writes it to csv file
def test_players_set(list_players, list_matrix, file, folder):
    for matrix in list_matrix:
        for i in range(len(list_players)):
            for j in range(i, len(list_players)):
                if i != j:
                    write_game(list_players[i],list_players[j],file,folder,matrix)
                    write_game(list_players[j],list_players[i],file,matrix)
                else:
                    write_game(list_players[i],copy.deepcopy(list_players[i]),file,folder,matrix)

# test_players_set takes in a list of player match ups, list of matrixs, and name of csv file
# test_players_random loops through every game matrix, every match up on the matrix and writes it to csv file
def test_players_list_set(list_players_vs, list_matrix, file, folder):
    for matrix in list_matrix:
        for p1, p2 in list_players_vs:
            if p1 != p2:
                write_game(p1,p2,file,folder,matrix)
            else:
                write_game(p1,copy.deepcopy(p1),file,folder,matrix)
                