import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
from scipy.sparse.csgraph import connected_components
from scipy.sparse import csr_matrix

COLOUR_MAP = {0: 'green', 1: 'red', 2: 'blue', 3: 'purple'}
RED_NUMBER = 1
BLUE_NUMBER = 2
PURPLE_NUMBER = 3

def colour_point(ver_colours, count, points, colour):
    if count >= len(points):
        return count
    if ver_colours[points[count]] != 0:
        count+= 1
    if count >= len(points):
        return count
    ver_colours[points[count]] = colour
    return count

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
    
    
def get_value(ver_colours):
    return np.count_nonzero(ver_colours == RED_NUMBER) - np.count_nonzero(ver_colours == BLUE_NUMBER)

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

def sim_graph(adj_mat, red_points, blue_points, display_amount=1):
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
        last_ver = burn_graph(adj_mat, ver_colours)
    if (display_amount >= 0):
        create_graph(adj_mat, ver_colours)
    return ver_colours


def generate_connected_graph(x):
    con_mat = np.zeros((x,x))
    connect = [x-1]
    for i in range(x-2,-1,-1):
        connection = random.randint(i+1, x-1)
        con_mat[connection, i], con_mat[i, connection] = 1, 1
        connect.append(i)
    return con_mat

def generate_connected_graph_v2(matrix):
    graph = csr_matrix(matrix)
    n_components, labels = connected_components(csgraph=graph, directed=False)

    if n_components == 1:
        return matrix
    
    components = {i: [] for i in range(n_components)}
    for node, label in enumerate(labels):
        components[label].append(node)

    for i in range(n_components - 1):
        node1 = components[i][0]
        node2 = components[i + 1][0]
        matrix[node1][node2] = 1
        matrix[node2][node1] = 1 

    return matrix

def generate_matrix(x, num_gen=2, split_num=1):
    upper_triangle = np.random.randint(0, num_gen, size=(x, x))
    upper_triangle[np.where(upper_triangle< split_num )] = 0
    upper_triangle[np.where(upper_triangle >= split_num )] = 1
    upper_triangle = np.triu(upper_triangle, 1) 
    adj_mat = upper_triangle + upper_triangle.T + generate_connected_graph(x)
    adj_mat[adj_mat==2]=1
    return adj_mat

def generate_matrix_v2(x, num_gen=2, split_num=1):
    upper_triangle = np.random.randint(0, num_gen, size=(x, x))
    upper_triangle[np.where(upper_triangle< split_num )] = 0
    upper_triangle[np.where(upper_triangle >= split_num )] = 1
    upper_triangle = np.triu(upper_triangle, 1) 
    adj_mat = upper_triangle + upper_triangle.T
    adj_mat[adj_mat==2]=1
    return generate_connected_graph_v2(adj_mat)


def find_winner(adj_mat, red, blue):
    ver = sim_graph(adj_mat, red,blue,-1)
    if np.count_nonzero(ver == RED_NUMBER) > np.count_nonzero(ver == BLUE_NUMBER):
        return 1
    elif np.count_nonzero(ver == RED_NUMBER) < np.count_nonzero(ver == BLUE_NUMBER):
        return 2
    else:
        return 0
