import generate_naive_strategies as gns
import holsticSearch as hs
import monte_carlo as mc
import random
import numpy as np
import heuristic_guided_search as hgs
# Setup for Naive search strategy
def setup_gns(matrix, ver_colours, red_player, args):
    return [gns.generate_tree(matrix, args[0], ver_colours, red_player), red_player, args[0]]

def reset_gns(args):
    return [args[2]]

# Setup for Mini max version of the Navie search strategy
def setup_gns_mini_max(matrix, ver_colours, red_player, args):
    return [gns.generate_tree_mini_max(matrix, args[0], ver_colours, red_player), red_player, matrix, ver_colours, args[0]]

def reset_gns_mini_max(args):
    return [args[4]]


def setup_psmm(matrix, ver_colours, red_player, args):
    return [hgs.priority_search_mini_max(matrix, args[0], ver_colours, red_player, red_player, args[1], args[2]), red_player, matrix, ver_colours, args[0], args[1], args[2]]

def reset_psmm(args):
    return [args[4], args[5], args[6]]

def setup_fsmm(matrix, ver_colours, red_player, args):
    return [hgs.filter_search_mini_max(matrix, args[0], ver_colours, red_player, red_player, args[1], args[2]), red_player, matrix, ver_colours, args[0], args[1], args[2], args[3]]

def reset_fsmm(args):
    return [args[4], args[5], args[6], args[7]]

# Setup for Hashmap version of the Navie search strategy
def setup_gns_hashmap(matrix, ver_colours, red_player, args):
    return [gns.generate_tree_hashmap(matrix, args[0], ver_colours, red_player), red_player, {}, args[0]]

def reset_gns_hashmap(args):
    return [args[3]]

# Plays the navie turn search stragegy (works for both minimax and hashmap version)
def play_gns(args):
    result = gns.minimax_alpha_beta(args[0], 1, args[1])
    args[0] = args[0].get_child(result[1][1])
    return args, args[0].choice

# Updates the navie turn search stragegy (works for both minimax and hashmap version)
def update_gns(args, play):
    args[0] = args[0].get_child(play)
    return args

def update_gns_mini_max(args, play):
    if args[0].get_child(play) is None:
        return [gns.generate_tree_mini_max(args[2], args[4], args[3], args[1], play), args[1], args[2], args[3], args[4]]
    
    args[0] = args[0].get_child(play)
    return args

def update_psmm(args, play):
    if args[0].get_child(play) is None:
        return   [hgs.priority_search_mini_max(args[2], args[4], args[3], args[1], args[1], args[5], args[6], play), args[1], args[2], args[3], args[4], args[5], args[6]]
    
    args[0] = args[0].get_child(play)
    return args

def update_fsmm(args, play):
    if args[0].get_child(play) is None:
        return   [hgs.filter_search_mini_max(args[2], args[4], args[3], args[1], args[1], args[5], args[6], args[7], play), args[1], args[2], args[3], args[4], args[5], args[6], args[7]]
    
    args[0] = args[0].get_child(play)
    return args

# Setup for default game
def setup_default(matrix, ver_colours, red_player, args):
    return [matrix, ver_colours, red_player] + args

def reset_default(args):
    return args[3:]

def play_hmc(args):
    play = hs.holticMostConnected(args[0], args[1], args[2], args[3])
    return args, play

def update_default(args, play):
    return args
# Setup for holtic most advantages stragegy
def setup_hma(matrix, ver_colours, red_player, args):
    return [matrix, ver_colours, red_player] + args
# Play for holtic most advantages stragegy
def play_hma(args):
    play = hs.holticMostAdvantages(args[0], args[1], args[2], args[3])
    return args, play

def setup_mc(matrix, ver_colours, red_player, args):
    return [mc.MCTS_Node(matrix, ver_colours, red_player)] + args

def reset_mc(args):
    return args[1:]

def update_mc(args, play):
    args[0] = args[0].perform_move(play)
    args[0].parent = None
    return args

def play_mc(args):
    play = mc.search(args[0], args[1], args[2])
    args[0] = args[0].perform_move(play)
    args[0].parent = None
    return args, play

def setup_random(matrix, ver_colours, red_player, args):
    return [ver_colours]

def reset_random(args):
    return []

def play_random(args):
    return args, random.choice(np.where(args[0] == 0)[0])

def play_hihb(args):
    return args, hs.holsitcIsolatedHighestBurn(args[0], args[1], args[3])[2]

def play_hhb(args):
    return args, hs.holsitcHighestBurn(args[0], args[1], args[2], args[3])[2]