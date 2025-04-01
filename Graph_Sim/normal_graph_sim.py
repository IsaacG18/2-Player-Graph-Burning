import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

RED_NUMBER = 1
BLUE_NUMBER = 2
PURPLE_NUMBER = 3

COLOUR_MAP = {0: 'green', RED_NUMBER: 'red', BLUE_NUMBER: 'blue', PURPLE_NUMBER: 'purple'}

# colour_point takes in a vertor of points, current index, list of points, and colour
# If the index is over the amount of points it returns the current count
# If the vertex is alread coloured it increments count else it colour it in
# Return the final count
def colour_point(ver_colours, count, points, colour):
    if count >= len(points):
        return count
    if ver_colours[points[count]] != 0:
        count+= 1
    if count >= len(points):
        return count
    ver_colours[points[count]] = colour
    return count

# burn_graph takes adjecteny matrix, and vector of vertexs colours 
# It first finds all points that are adjectent to red and blue vertexs
# It then does the same with purple and then makes them all purple that are white
# For every red and blue adject vertex that is white it convert it to that colour
def burn_graph(adj_mat, ver_colours):
    red, blue = np.array([]),np.array([])
    if_red, if_blue = len(np.where(ver_colours == RED_NUMBER)[0]) != 0, len(np.where(ver_colours == BLUE_NUMBER)[0]) != 0
    
    if if_red: red = np.max(adj_mat[np.where(ver_colours == RED_NUMBER)], 0)
    if if_blue:blue = np.max(adj_mat[np.where(ver_colours == BLUE_NUMBER)], 0)

    if np.where(ver_colours >= PURPLE_NUMBER)[0].size > 0:
        purple = np.max(adj_mat[np.where(ver_colours >= PURPLE_NUMBER)], 0)
        purple[np.where(ver_colours!=0)]=0
        ver_colours += purple*PURPLE_NUMBER
    
    if if_red: red[np.where(ver_colours!=0)]=0
    if if_blue:blue[np.where(ver_colours!=0)]=0

    if if_red: ver_colours += red
    if if_blue: ver_colours += blue*BLUE_NUMBER
    
# get_value takes a vertex of colour
# returns number of red vertex minus number of blue vertexs
def get_value(ver_colours):
    return np.count_nonzero(ver_colours == RED_NUMBER) - np.count_nonzero(ver_colours == BLUE_NUMBER)

# create_graph takes a adjectancy matrix and vertex of colour
# Using this creates a graph of this a colour it in using the vector
def create_graph(adj_mat, ver_colours):
    ver_name = np.arange(ver_colours.shape[0])
    rows, cols = np.where(adj_mat == 1)
    edges = zip(rows.tolist(), cols.tolist()) 
    gr = nx.Graph()
    gr.add_nodes_from(ver_name)
    gr.add_edges_from(edges)
    ver_colours_mapped = [COLOUR_MAP[colour] for colour in ver_colours]
    nx.draw(gr, node_color=ver_colours_mapped, node_size=500, with_labels=True)
    plt.show()

# sim_graph takes in adjectency matrix, list of vertexs for the red player and the blue player, and display amounts
# Plays out a game using the list of plays for each player till the game is complete and display the game after display amounts terms
def sim_graph(adj_mat, red_points, blue_points, display_amount=-1):
    blue_count, red_count = 0,0
    ver_colours = np.zeros(adj_mat.shape[0])
    last_ver = np.zeros(ver_colours.shape[0])
    count = 0
    if (display_amount >= 0):
        create_graph(adj_mat, ver_colours)
    first = True
    while(np.sum(ver_colours-last_ver)!= 0 or first):
        first = False
        red_count = colour_point(ver_colours, red_count, red_points, RED_NUMBER)
        blue_count = colour_point(ver_colours, blue_count, blue_points, BLUE_NUMBER)
        count += 1
        if (display_amount > 0 and count%display_amount == 0):
            create_graph(adj_mat, ver_colours)
        last_ver = np.copy(ver_colours)
        burn_graph(adj_mat, ver_colours)
    if (display_amount >= 0):
        create_graph(adj_mat, ver_colours)
    return ver_colours

# generate_connected_graph takes in an size of the matrix
# Create an empty matrix then loop through each vertex and make a random connection to a prevous node
# returns connect xbyx adjancy matrix with x-1 edges
def generate_connected_graph(x):
    con_mat = np.zeros((x,x))
    for i in range(x-2,-1,-1):
        connection = random.randint(i+1, x-1)
        con_mat[connection, i], con_mat[i, connection] = 1, 1
    return con_mat


# generate_matrix takes in an size of the matrix, a max of a random number and a number to split above and below
# Create an empty matrix, populate it with random numbers then set all points above split to 1 the rest as 0
# Then make the matrix sysmetric then call generate_connected_graph to make the matrix connected
# returns an adjancy matrix
def generate_matrix(x, num_gen=2, split_num=1):
    upper_triangle = np.random.randint(0, num_gen, size=(x, x))
    upper_triangle[np.where(upper_triangle< split_num )] = 0
    upper_triangle[np.where(upper_triangle >= split_num )] = 1
    upper_triangle = np.triu(upper_triangle, 1) 
    adj_mat = upper_triangle + upper_triangle.T + generate_connected_graph(x)
    adj_mat[adj_mat==2]=1
    return adj_mat

# find_winner takes in an adjancy matrix, and a set of red points and blue points
# It calls run simulator then finds the winning plater
# returns 1 if player 1 wins, 2 if player 2 wins, 0 if it a draw
def find_winner(adj_mat, red_points, blue_points):
    ver = sim_graph(adj_mat, red_points, blue_points)
    if np.count_nonzero(ver == RED_NUMBER) > np.count_nonzero(ver == BLUE_NUMBER):
        return 1
    elif np.count_nonzero(ver == RED_NUMBER) < np.count_nonzero(ver == BLUE_NUMBER):
        return 2
    else:
        return 0

