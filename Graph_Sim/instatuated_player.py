import generate_naive_strategies as gns
import heurstic_search as hs
import monte_carlo as mc
import random
import numpy as np
import heuristic_guided_search as hgs
import hashmap_gns as hg


#Player class which is a class to store a stragegy 
class player:
    def __init__(self, name):
        self.name =  name
# Setup does any precalcution the game needs and sets up the args for play
    def setup(self, matrix, ver_colours, red_player):
        self.matrix = matrix
        self.ver_colours = ver_colours
        self.red_player = red_player
# Plays a turn of the game and returns the play, updates the args if nesseary
    def play(self):
        pass
# Update takes in the other players move and updates thea args
    def update(self, play):
        pass
# Reset convert the arguement to what they where like at initilisation
    def reset(self):
        pass
# Returns the name arguement of the player
    def get_name(self):
        return self.name
    
class gns_player(player):
    def __init__(self, name, depth):
        super().__init__(name)
        self.depth = depth
    def setup(self, matrix, ver_colours, red_player):
        self.node = gns.generate_tree(matrix, self.depth, ver_colours, red_player)
        self.red_player = red_player
    def update(self, play):
        self.node = self.node.get_child(play)
    def play(self):
        result = gns.minimax_single(self.node, self.red_player)
        self.node = self.node.get_child(result)
        return result
    
class gns_dfs_player(gns_player):
    def __init__(self, name, depth):
        super().__init__(name, depth)
    def setup(self, matrix, ver_colours, red_player):
        player.setup(self, matrix, ver_colours, red_player)
        self.node = gns.generate_tree_dfs(self.matrix, self.depth, self.ver_colours, self.red_player)
    def update(self, play):
        if self.node.get_child(play) is None:
            self.node = gns.generate_tree_dfs(self.matrix, self.depth, self.ver_colours, self.red_player, play)
            return
        self.node = self.node.get_child(play)

class gns_hashmap_player(gns_player):
    def __init__(self, name, depth):
        super().__init__(name, depth)
    def setup(self, matrix, ver_colours, red_player):
        player.setup(self, matrix, ver_colours, red_player)
        self.node = hg.generate_tree_hashmap(matrix, self.depth, ver_colours, red_player, {})
    def update(self, play):
        self.node = self.node.get_child_by_ver(self.ver_colours)
        if self.node.get_child_by_ver(self.ver_colours) is None:
            self.node = hg.generate_tree_hashmap(self.matrix, self.depth, self.ver_colours, self.red_player, {}, play)
            return
        self.node = self.node.get_child_by_ver(self.ver_colours)
    def play(self):
        result = hg.minimax_alpha_beta_hash(self.node, self.red_player, tuple(self.ver_colours))
        self.node = self.node.get_child(result)
        return result
    
class gp_dfs_player(gns_player):
    def __init__(self, name, depth, func_list, func_sort):
        super().__init__(name, depth)
        self.func_list = func_list
        self.func_sort = func_sort
    def setup(self, matrix, ver_colours, red_player):
        player.setup(self, matrix, ver_colours, red_player)
        self.node = hgs.guided_priority_dfs(self.matrix, self.depth, self.ver_colours, self.red_player, self.func_list,  self.func_sort)
    def update(self, play):
        if self.node.get_child(play) is None:
             self.node = hgs.guided_priority_dfs(self.matrix, self.depth, self.ver_colours, self.red_player, self.func_list,  self.func_sort, play)
             return
        self.node = self.node.get_child(play) 

class f_dfs_player(gns_player): 
    def __init__(self, name, depth, func_list, func_cmp):
        super().__init__(name, depth)
        self.func_list = func_list
        self.func_cmp = func_cmp
    def setup(self, matrix, ver_colours, red_player):
        player.setup(self, matrix, ver_colours, red_player)
        self.node = hgs.filter_dfs(self.matrix, self.depth, self.ver_colours, self.red_player, self.func_list,  self.func_cmp)
    def update(self, play):
        if self.node.get_child(play) is None:
             self.node = hgs.filter_dfs(self.matrix, self.depth, self.ver_colours, self.red_player, self.func_list, self.func_cmp, play)
             return
        self.node = self.node.get_child(play) 

class mc_player(player):
    def __init__(self, name, iterations, exploration_constant):
        super().__init__(name)
        self.iterations = iterations
        self.exploration_constant = exploration_constant
    def setup(self, matrix, ver_colours, red_player):
        self.node = mc.MCTS_Node(matrix, ver_colours, red_player)
        super().setup(matrix, ver_colours, red_player)
    def update(self, play):
        self.node = self.node.perform_move(play)
        self.node.parent = None
    def play(self):
        play = mc.search(self.node, self.iterations, self.exploration_constant)
        self.node = self.node.perform_move(play)
        self.node.parent = None
        return play
    
class random_player(player):
    def play(self):
        return random.choice(np.where(self.ver_colours == 0)[0])
    
class hkn_player(player):
    def __init__(self, name, turns):
        self.turns = turns
        super().__init__(name)
    def play(self):
        return hs.heuristic_k_neighbour(self.matrix, self.ver_colours, self.red_player, self.turns)

class fdm_player(player):
    def __init__(self, name, turns):
        self.turns = turns
        super().__init__(name)
    def play(self):
        return hs.fix_depth_minimax(self.matrix, self.ver_colours, self.red_player, self.turns)
    
class fdm_set_player_2_3(player):
    def play(self):
        if self.red_player:
            return hs.fix_depth_minimax(self.matrix, self.ver_colours, self.red_player, 2)
        else:
            return hs.fix_depth_minimax(self.matrix, self.ver_colours, self.red_player, 3)
        
class fdm_set_player_4_3(player):
    def play(self):
        if self.red_player:
            return hs.fix_depth_minimax(self.matrix, self.ver_colours, self.red_player, 4)
        else:
            return hs.fix_depth_minimax(self.matrix, self.ver_colours, self.red_player, 3)
        
class fdm_set_player_2_1(player):
    def play(self):
        if self.red_player:
            return hs.fix_depth_minimax(self.matrix, self.ver_colours, self.red_player, 2)
        else:
            return hs.fix_depth_minimax(self.matrix, self.ver_colours, self.red_player, 1)
        
class fdm_set_player_4_1(player):
    def play(self):
        if self.red_player:
            return hs.fix_depth_minimax(self.matrix, self.ver_colours, self.red_player, 4)
        else:
            return hs.fix_depth_minimax(self.matrix, self.ver_colours, self.red_player, 1)

class hib_player(player):
    def __init__(self, name, func):
        super().__init__(name)
        self.func = func
    def play(self):
        return hs.heuristic_isolated_burn(self.matrix, self.ver_colours, self.func)[2]
    
class hsb_player(player):
    def __init__(self, name, func):
        super().__init__(name)
        self.func = func
    def play(self):
        return hs.heuristic_simulated_burn(self.matrix, self.ver_colours, self.red_player, self.func)[2]


class hnh_player(player):
    def __init__(self, name):
        super().__init__(name)
    def play(self):
        return hs.neighbourhood_heuristic(self.matrix, self.ver_colours)