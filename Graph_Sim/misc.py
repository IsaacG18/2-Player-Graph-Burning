import normal_graph_sim as ngs
import numpy as np
import copy


def check_winning_strat_single(x, num_gen=2, split_num=1):
    adj_mat = ngs.generate_matrix(x, num_gen, split_num)
    p1, losers = 0, []
    if ngs.find_winner(adj_mat, [0], [1]) != 2:
        losers.append(1)
    else:
        losers.append(0)
        p1 = 1
    for i in range(2, x):
        if ngs.find_winner(adj_mat, [p1], [i]) != 2:
            losers.append(i)
        else:
            losers.append(p1)
            p1 = i
            for x in losers:
                if ngs.find_winner(adj_mat, [p1], [x]) == 2:
                    ngs.sim_graph(adj_mat, [p1],[x],0)
                    ngs.sim_graph(adj_mat, [p1],[losers[-1]],0)
                    return 0
    return 1

def create_path_graph_adj_matrix(n):
    adj_matrix = np.zeros((n, n), dtype=int)
    for i in range(n - 1):
        adj_matrix[i, i + 1] = 1
        adj_matrix[i + 1, i] = 1
    return 



        
    