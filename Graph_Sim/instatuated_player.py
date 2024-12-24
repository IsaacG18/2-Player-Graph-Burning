import generate_naive_strategies as gns
import holsticSearch as hs

# Setup for Naive search strategy
def setup_gns(matrix, ver_colours, red_player, args):
    return [gns.generate_tree(matrix, args[0], ver_colours, red_player), red_player]

# Setup for Mini max version of the Navie search strategy
def setup_gns_mini_max(matrix, ver_colours, red_player, args):
    return [gns.generate_tree_mini_max(matrix, args[0], ver_colours, red_player), red_player]

# Setup for Hashmap version of the Navie search strategy
def setup_gns_hashmap(matrix, ver_colours, red_player, args):
    return [gns.generate_tree_hashmap(matrix, args[0], ver_colours, red_player), red_player, {}]

# Plays the navie turn search stragegy (works for both minimax and hashmap version)
def play_gns(args):
    result = gns.minimax_alpha_beta(args[0], 1, args[1])
    args[0] = args[0].get_child(result[1][1])
    return args, args[0].choice

# Updates the navie turn search stragegy (works for both minimax and hashmap version)
def update_gns(args, play):
    args[0] = args[0].get_child(play)
    return args

# Setup for default game
def setup_default(matrix, ver_colours, red_player, args):
    return [matrix, ver_colours, red_player] + args

def play_hmc(args):
    play = hs.holticMostConnected(args[0], args[1], args[2], args[3])
    return args, play

def update_default(args, play):
    return args
# Setup for holtic most advantages stragegy
def setup_hma(matrix, ver_colours, red_player, args):
    return [matrix, ver_colours, red_player] + args + [{}]
# Play for holtic most advantages stragegy
def play_hma(args):
    play = hs.holticMostAdvantages(args[0], args[1], args[2], args[3], args[4])
    return args, play


