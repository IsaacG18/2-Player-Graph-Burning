import generate_naive_strategies as gns
import holsticSearch as hs
import monte_carlo as mc
import random
import numpy as np
import heuristic_guided_search as hgs
import hashmap_gns as hg

# Setup for Naive search strategy
def setup_gns(matrix, ver_colours, red_player, args):
    return {"red_player": red_player, "depth": args["depth"],"node":gns.generate_tree(matrix, args["depth"], ver_colours, red_player) }



# Setup for Mini max version of the Navie search strategy
def setup_gns_mini_max(matrix, ver_colours, red_player, args):
    return {"red_player": red_player, "matrix": matrix, "ver_colours": ver_colours, "depth": args["depth"], "node": gns.generate_tree_mini_max(matrix, args["depth"], ver_colours, red_player)}


# Setup for prority search on a mini max search strategy
def setup_psmm(matrix, ver_colours, red_player, args):
    return {"red_player": red_player, "matrix": matrix, "ver_colours": ver_colours, 
            "depth": args["depth"], "func_list": args["func_list"], "func_sort": args["func_sort"], 
            "node": hgs.priority_search_mini_max(matrix, args["depth"], ver_colours, red_player, red_player, args["func_list"], args["func_sort"])}

# Setup for filter search on a mini max search strategy
def setup_fsmm(matrix, ver_colours, red_player, args):
    return {"red_player": red_player, "matrix": matrix, "ver_colours": ver_colours, 
            "depth": args["depth"], "func_list": args["func_list"], "func_cmp": args["func_cmp"], "count_min": args["count_min"], 
            "node": hgs.filter_search_mini_max(matrix, args["depth"], ver_colours, red_player, red_player, args["func_list"], args["func_cmp"], args["count_min"])}


# Setup for Hashmap version of the Navie search strategy
def setup_gns_hashmap(matrix, ver_colours, red_player, args):
    return {"red_player": red_player,"ver_colours": ver_colours, "depth": args["depth"], "node":hg.generate_tree_hashmap(matrix, args["depth"], ver_colours, red_player, {}) }


# Setup for default game
def setup_default(matrix, ver_colours, red_player, args):
    args["matrix"] = matrix
    args["ver_colours"] = ver_colours
    args["red_player"] = red_player
    return args


# Setup for Monte Carlo search stragegy
def setup_mc(matrix, ver_colours, red_player, args):
    args["node"] = mc.MCTS_Node(matrix, ver_colours, red_player)
    return args

# Setup for Random search stragegy
def setup_random(matrix, ver_colours, red_player, args):
    return {"ver_colours": ver_colours}

# Updates the navie turn search stragegy 
def update_gns(args, play):
    args["node"] = args["node"].get_child(play)
    return args

# Updates the navie turn search with hashmap stragegy 
def update_gns_hashmap(args, play):
    args["node"] = args["node"].get_child_by_ver( args["ver_colours"])
    return args


# Updates the minimax improvement to navie turn search stragegy
def update_gns_mini_max(args, play):
    if args["node"].get_child(play) is None:
        args["node"] = gns.generate_tree_mini_max(args["matrix"], args["depth"], args["ver_colours"], args["red_player"], play)
        return args
    args["node"] = args["node"].get_child(play)
    return args

# Updates the prority search on a mini max search strategy
def update_psmm(args, play):
    if args["node"].get_child(play) is None:
        args["node"] = hgs.priority_search_mini_max(args["matrix"], args["depth"], args["ver_colours"], args["red_player"], args["red_player"], args["func_list"], args["func_sort"], play)
        return args
    
    args["node"] = args["node"].get_child(play)
    return args

# Updates the filter search on a mini max search strategy
def update_fsmm(args, play):
    if args["node"].get_child(play) is None:
        args["node"] = hgs.filter_search_mini_max(args["matrix"], args["depth"], args["ver_colours"], args["red_player"], args["red_player"], args["func_list"], args["func_cmp"], args["count_min"], play)
        return args
    
    args["node"] = args["node"].get_child(play)
    return args

# Updates default that does nothing
def update_default(args, play):
    return args

# Updates the Monte Carlo search strategy
def update_mc(args, play):
    args["node"] = args["node"].perform_move(play)
    args["node"].parent = None
    return args

# Plays the navie turn search stragegy (works for with minimax)
def play_gns(args):
    result = gns.minimax_single(args["node"], args["red_player"])
    args["node"] = args["node"].get_child(result)
    return args, result
    
# Plays the navie turn with hashmap search stragegy
def play_gns_hashmap(args):
    result = hg.minimax_alpha_beta_hash(args["node"], args["red_player"], tuple(args["ver_colours"]))
    args["node"] = args["node"].get_child(result)
    return args, result

# Plays the Holtic Most Connected Search
def play_hmc(args):
    play = hs.holticMostConnected(args["matrix"], args["ver_colours"], args["red_player"], args["turns"])
    return args, play

# Play for holtic most advantages stragegy
def play_hma(args):
    play = hs.holticMostAdvantages(args["matrix"], args["ver_colours"], args["red_player"], args["turns"])
    return args, play

# Play for Monte Carlo Search stragegy
def play_mc(args):
    play = mc.search(args["node"], args["iterations"], args["exploration_constant"])
    args["node"] = args["node"].perform_move(play)
    args["node"].parent = None
    return args, play

# Play for random which picks a random play
def play_random(args):
    return args, random.choice(np.where(args["ver_colours"] == 0)[0])

# Play for Holsitc Isolated Highest Burn stragegy
def play_hihb(args):
    return args, hs.holsitcIsolatedHighestBurn(args["matrix"], args["ver_colours"], args["func"])[2]

# Play for Holsitc Highest Burn stragegy
def play_hhb(args):
    return args, hs.holsitcHighestBurn(args["matrix"], args["ver_colours"], args["red_player"], args["func"])[2]