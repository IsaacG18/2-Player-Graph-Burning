import generate_naive_strategies as gns
import holsticSearch as hs
import monte_carlo as mc
import random
import numpy as np
import heuristic_guided_search as hgs

# Setup for Naive search strategy
def setup_gns(matrix, ver_colours, red_player, args):
    return [gns.generate_tree(matrix, args[0], ver_colours, red_player), red_player]


# Setup for Mini max version of the Navie search strategy
def setup_gns_mini_max(matrix, ver_colours, red_player, args):
    return [gns.generate_tree_mini_max(matrix, args[0], ver_colours, red_player), red_player, matrix, ver_colours, args[0]]


# Setup for prority search on a mini max search strategy
def setup_psmm(matrix, ver_colours, red_player, args):
    return [hgs.priority_search_mini_max(matrix, args[0], ver_colours, red_player, red_player, args[1], args[2]), red_player, matrix, ver_colours, args[0], args[1], args[2]]

# Setup for filter search on a mini max search strategy
def setup_fsmm(matrix, ver_colours, red_player, args):
    return [hgs.filter_search_mini_max(matrix, args[0], ver_colours, red_player, red_player, args[1], args[2]), red_player, matrix, ver_colours, args[0], args[1], args[2], args[3]]


# Setup for Hashmap version of the Navie search strategy
def setup_gns_hashmap(matrix, ver_colours, red_player, args):
    return [gns.generate_tree_hashmap(matrix, args[0], ver_colours, red_player), red_player, {}]

# Setup for default game
def setup_default(matrix, ver_colours, red_player, args):
    return [matrix, ver_colours, red_player] + args

# Setup for holtic most advantages stragegy
def setup_hma(matrix, ver_colours, red_player, args):
    return [matrix, ver_colours, red_player] + args

# Setup for Monte Carlo search stragegy
def setup_mc(matrix, ver_colours, red_player, args):
    return [mc.MCTS_Node(matrix, ver_colours, red_player)] + args

# Setup for Random search stragegy
def setup_random(matrix, ver_colours, red_player, args):
    return [ver_colours]

# Updates the navie turn search stragegy 
def update_gns(args, play):
    args[0] = args[0].get_child(play)
    return args

# Updates the minimax improvement to navie turn search stragegy
def update_gns_mini_max(args, play):
    if args[0].get_child(play) is None:
        return [gns.generate_tree_mini_max(args[2], args[4], args[3], args[1], play), args[1], args[2], args[3], args[4]]
    
    args[0] = args[0].get_child(play)
    return args

# Updates the prority search on a mini max search strategy
def update_psmm(args, play):
    if args[0].get_child(play) is None:
        return   [hgs.priority_search_mini_max(args[2], args[4], args[3], args[1], args[1], args[5], args[6], play), args[1], args[2], args[3], args[4], args[5], args[6]]
    
    args[0] = args[0].get_child(play)
    return args

# Updates the filter search on a mini max search strategy
def update_fsmm(args, play):
    if args[0].get_child(play) is None:
        return   [hgs.filter_search_mini_max(args[2], args[4], args[3], args[1], args[1], args[5], args[6], args[7], play), args[1], args[2], args[3], args[4], args[5], args[6], args[7]]
    
    args[0] = args[0].get_child(play)
    return args

# Updates default that does nothing
def update_default(args, play):
    return args

# Updates the Monte Carlo search strategy
def update_mc(args, play):
    args[0] = args[0].perform_move(play)
    args[0].parent = None
    return args

# Plays the navie turn search stragegy (works for both minimax and hashmap version)
def play_gns(args):
    result = gns.minimax_alpha_beta(args[0], 1, args[1])
    args[0] = args[0].get_child(result[1][1])
    return args, args[0].choice

# Plays the Holtic Most Connected Search
def play_hmc(args):
    play = hs.holticMostConnected(args[0], args[1], args[2], args[3])
    return args, play

# Play for holtic most advantages stragegy
def play_hma(args):
    play = hs.holticMostAdvantages(args[0], args[1], args[2], args[3])
    return args, play

# Play for Monte Carlo Search stragegy
def play_mc(args):
    play = mc.search(args[0], args[1], args[2])
    args[0] = args[0].perform_move(play)
    args[0].parent = None
    return args, play

# Play for random which picks a random play
def play_random(args):
    return args, random.choice(np.where(args[0] == 0)[0])

# Play for Holsitc Isolated Highest Burn stragegy
def play_hihb(args):
    return args, hs.holsitcIsolatedHighestBurn(args[0], args[1], args[3])[2]

# Play for Holsitc Highest Burn stragegy
def play_hhb(args):
    return args, hs.holsitcHighestBurn(args[0], args[1], args[2], args[3])[2]