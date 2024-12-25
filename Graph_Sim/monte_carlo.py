import math
import random
import numpy as np
import normal_graph_sim as ngs

class MCTS_Node:
    def __init__(self, matrix, ver_colour, red_player, parent = None):
        self.matrix = matrix
        self.ver_colour = ver_colour
        self.parent = parent
        self.children = {}
        self.calculated_children = {}
        self.children_expanded = 0
        self.visits = 0
        self.value = 0
        self.red_player = red_player

    def is_fully_expanded(self):
        return self.children_expanded == (len(self.get_legal_moves()))

    def get_legal_moves(self):
        return np.where(self.ver_colour == 0)[0]

    def perform_move(self, move):
        if move not in self.calculated_children:
            new_ver = np.copy(self.ver_colour)
            if self.red_player:
                new_ver[move] += ngs.RED_NUMBER
            else:
                new_ver[move] += ngs.BLUE_NUMBER
                ngs.burn_graph(self.matrix, new_ver)
            self.calculated_children[move] = MCTS_Node(self.matrix, new_ver, not self.red_player, self)
        return self.calculated_children[move]

    def is_terminal(self):
        return np.all(self.ver_colour != 0)

    def get_reward(self):
        return ngs.get_value(self.ver_colour)


def search(root, iterations, exploration_constant):
    for _ in range(iterations):
        node = select(root, exploration_constant, root.red_player)
        if not node.is_terminal():
            node = expand(node)
        reward = simulate(node)
        backpropagate(node, reward)
    max_value, max_index = float('-inf'), -1
    for i in root.children:
        if root.calculated_children[i].visits > max_value:
            max_index, max_value = i, root.calculated_children[i].visits
    return max_index

def select(node, exploration_constant, red_player):
    if not node.is_terminal() and node.is_fully_expanded():
        max_value, max_node = float('-inf'), None
        for i in node.children:
            cur_value = uct_value(node.calculated_children[i], exploration_constant, red_player)
            if cur_value > max_value:
                max_node, max_value = node.calculated_children[i], cur_value
        return select(max_node, exploration_constant, not red_player)
    return node

def uct_value(node, exploration_constant, red_player):
    if node.visits == 0:
        return float('inf')
    if red_player:
        return (node.value / node.visits + exploration_constant * math.sqrt(math.log(node.parent.visits) / node.visits))
    return (-node.value / node.visits + exploration_constant * math.sqrt(math.log(node.parent.visits) / node.visits))

def expand(node):
    move = random.choice([move for move in node.get_legal_moves() if move not in node.children])
    node.children[move] = True
    node.children_expanded += 1
    return node.perform_move(move)

def simulate(node):
    if not node.is_terminal():
        return simulate(node.perform_move(random.choice(node.get_legal_moves())))
    return node.get_reward()

def backpropagate(node, reward):
    if node is not None:
        node.visits += 1
        node.value += reward
        backpropagate(node.parent, reward)

