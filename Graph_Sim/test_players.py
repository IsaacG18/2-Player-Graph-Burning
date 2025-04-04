import heurstic_search as hs
import instatuated_player as ip
import heuristic_guided_search as hgs
import play as p
import math
import os
import numpy as np




gns = ip.gns_player("GNS", float("inf"))
gns_dfs  = ip.gns_dfs_player("GNSDFS", float("inf"))
gns_hash = ip.gns_hashmap_player("Hashmap", float("inf"))
gp_dfs_sim = ip.gp_dfs_player("GPDFS_Sim", float("inf"), hgs.heuristic_simulated_burn_list, hs.better_than_value)
f_dfs_sim = ip.f_dfs_player("FDFS_Sim",float("inf"), hgs.heuristic_simulated_burn_list, hs.better_than_value)
gp_dfs_iso = ip.gp_dfs_player("GPDFS_Iso", float("inf"), hgs.heuristic_isolated_burn_list, hs.better_than_value)
f_dfs_iso = ip.f_dfs_player("FDFS_Iso",float("inf"), hgs.heuristic_isolated_burn_list, hs.better_than_value)
gp_dfs_nl = ip.gp_dfs_player("GPDFS_NL", float("inf"), hgs.neighbourhood_list, hs.better_than_value)
f_dfs_nl = ip.f_dfs_player("FDFS_NL",float("inf"), hgs.neighbourhood_list, hs.better_than_value)
gp_dfs_nbl = ip.gp_dfs_player("GPDFS_NBL", float("inf"), hgs.neighbourhood_burn_list, hs.better_than_value)
f_dfs_nbl = ip.f_dfs_player("FDFS_NBL",float("inf"), hgs.neighbourhood_burn_list, hs.better_than_value)
gp_dfs_bpl = ip.gp_dfs_player("GPDFS_BPL", float("inf"), hgs.best_play_list, hs.better_than_value)
f_dfs_bpl = ip.f_dfs_player("FDFS_BPL",float("inf"), hgs.best_play_list, hs.better_than_value)
mc50 = ip.mc_player("MC50",50, math.sqrt(2))
mc100 = ip.mc_player("MC100",100, math.sqrt(2))
mc150 = ip.mc_player("MC150",150, math.sqrt(2))
mc200 = ip.mc_player("MC200",200, math.sqrt(2))
mc250 = ip.mc_player("MC250",250, math.sqrt(2))
random = ip.random_player("Random")
fdm_1 = ip.fdm_player("FDM1", 1)
hkn_1 = ip.hkn_player("HKN1", 1)
fdm_2 = ip.fdm_player("FDM2", 2)
hkn_2 = ip.hkn_player("HKN2", 2)
fdm_3 = ip.fdm_player("FDM3", 3)
hkn_3 = ip.hkn_player("HKN3", 3)
fdm_4 = ip.fdm_player("FDM4", 4)
hkn_4 = ip.hkn_player("HKN4", 4)
hkn_5 = ip.hkn_player("HKN5", 5)
hkn_6 = ip.hkn_player("HKN6", 6)
hkn_7 = ip.hkn_player("HKN7", 7)
hkn_8 = ip.hkn_player("HKN8", 8)
hkn_9 = ip.hkn_player("HKN9", 9)
hkn_10 = ip.hkn_player("HKN10", 10)
fdm_set_4_3 = ip.fdm_set_player_4_3("FDM_SET_4_3")
fdm_set_2_3 = ip.fdm_set_player_2_3("FDM_SET_2_3")
hib = ip.hib_player("HIB", hs.better_than_value)
hsb = ip.hsb_player("HSB", hs.better_than_value)
hnh = ip.hnh_player("HNH")

# Final Set Experiment Strategies 
FINAL_PLAYERS = [gns, gns_hash, gns_dfs , 
                 f_dfs_nl, f_dfs_nbl, 
                 gp_dfs_nl, gp_dfs_nbl, gp_dfs_iso, 
                 fdm_set_4_3, fdm_set_2_3, 
                 mc150, mc200, random, hib, hsb, hnh,
                 hkn_1, hkn_2,]
# Fix Depth Minimax Experiment Strategies 
FDM_PLAYERS = [gns_dfs, fdm_1, fdm_2, fdm_3, fdm_4]
# Highest Kth Neighbour Experiment Strategies 
HKN_PLAYERS = [gns_dfs, hkn_1, hkn_2, hkn_3, hkn_4, hkn_5, hkn_6]
# Guided Priority and Filter DFS Experiment Strategies 
GP_F_PLAYERS = [gns_dfs , gp_dfs_sim, f_dfs_sim, gp_dfs_iso, f_dfs_iso, gp_dfs_nl, f_dfs_nl, gp_dfs_nbl, f_dfs_nbl, gp_dfs_bpl, f_dfs_bpl]
# Monte Carlo Experiment Strategies
MC_PLAYERS = [gns_dfs, mc50, mc100, mc150,mc200,mc250]

#SET FILENAME AND FOLDER AS INDEX 0 of TUPLE and PLAYERS AS INDEX 1
SUGGESTED_PLAYER_NAMES = [("Last_HNK", HKN_PLAYERS), ("Last_FDM", FDM_PLAYERS), ("Last_GP_F", GP_F_PLAYERS), ("Last_MC", MC_PLAYERS), ("Last_all", FINAL_PLAYERS)]


# Number for Matrix Generator
NUMBER_GEN = 100

# List of players to be tested
PLAYERS = FINAL_PLAYERS
# Default filename and folder for output storage
FILENAME = "PLACE_HOLDER"
FOLDER = "PLACE_HOLDER"
# Different vertex sizes for testing
SIZE = [10, 15, 20]
# Different edge sizes for testing
EDGE_LIKELIHOOD = [95, 100]
# Number of iterations for each test
ITER = 100



def test_players(list_players, vertex_count, iterations, file, folder):
    """
    Tests players with different probability an edge exists
    and saves results as CSV files.

    Parameters:
    - list_players: List of players to test
    - vertex_count: Number of vertices in the test graph
    - iterations: Number of test iterations
    - file: Base filename for output
    - folder: Folder to save results
    """
    for el in EDGE_LIKELIHOOD:
        p.test_players_random(list_players, vertex_count, NUMBER_GEN, el, iterations, f"{file}_{el}.csv", folder)
        print(f"Completed on Likelihood {el} with graph size {vertex_count}")

def test_all_players(players, filename, foldername, sizes, iter):
    """
    Runs tests for all players across different vertex sizes.

    Parameters:
    - players: List of players
    - filename: Base name for output files
    - foldername: Directory to store results
    - sizes: List of vertex sizes to test
    - iter: Number of iterations per test
    """
    print("Start Running comparison...")
    os.makedirs(foldername, exist_ok=True)
    for i in sizes:
        test_players(players, i, iter, f"{filename}_{i}", foldername)

# THIS IS A EXPERIMENTAL TOOL NONE-PRODUCTION TESTED
def play_against_robot_gen(player, vertex_count, num_gen, split_num, first):
    p.test_human_against_player_gen(player, vertex_count, num_gen, split_num, first)

# THIS IS A EXPERIMENTAL TOOL NONE-PRODUCTION TESTED
def play_against_robot_matrix(player, edges, size, first):
    p.test_human_against_player(player, p.manual_gen_matrix(edges, size), first)


def main():
    test_all_players(FINAL_PLAYERS, FILENAME, FILENAME, SIZE, ITER)
if __name__ == "__main__":
    main() 



