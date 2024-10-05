import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

COLOUR_MAP = {0: 'green', 1: 'red', 2: 'blue', 3: 'purple'}
RED_NUMBER = 1
BLUE_NUMBER = 2

def create_graph(adj_mat, ver_colours, ver_name):
    rows, cols = np.where(adj_mat == 1)
    edges = zip(rows.tolist(), cols.tolist()) 
    gr = nx.Graph()
    gr.add_nodes_from(ver_name)
    gr.add_edges_from(edges)
    ver_colours_mapped = [COLOUR_MAP[colour] for colour in ver_colours]
    nx.draw(gr, node_color=ver_colours_mapped, node_size=500, with_labels=True)
    plt.show()

def sim_graph(adj_mat, red_start, blue_start, display_amount=1):
    ver_colours = np.zeros(adj_mat.shape[0])
    ver_colours[red_start], ver_colours[blue_start] = RED_NUMBER,BLUE_NUMBER
    last_ver = np.zeros(ver_colours.shape[0])
    names = np.arange(ver_colours.shape[0])
    count = 0
    while(np.sum(ver_colours-last_ver)!= 0):
        count += 1
        if (count%display_amount == 0):
            create_graph(adj_mat, ver_colours, names)
        red, blue = np.max(adj_mat[np.where(ver_colours == RED_NUMBER)], 0), np.max(adj_mat[np.where(ver_colours == BLUE_NUMBER)], 0)
        red[np.where(ver_colours!=0)]=0
        blue[np.where(ver_colours!=0)]=0
        last_ver = np.copy(ver_colours)
        ver_colours += red+blue*BLUE_NUMBER
    create_graph(adj_mat, ver_colours, names)

adj_mat = np.array([
    [0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 1, 0, 1],
    [1, 0, 0, 1, 0]
])

sim_graph(adj_mat, 0, 1)


    

