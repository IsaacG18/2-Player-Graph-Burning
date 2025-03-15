import heurstic_search as hs
import instatuated_player as ip
import heuristic_guided_search as hgs
import play as p
import math
import normal_graph_sim as ngs
import numpy as np
import copy

NUMBER_GEN = 100


gns = ip.gns_player("GNS", float("inf"))
gns_dfs  = ip.gns_dfs_player("GNSDF", float("inf"))
gns_hash = ip.gns_hashmap_player("Hashmap", float("inf"))
gp_dfs_sim = ip.gp_dfs_player("GPDFS_Sim", float("inf"), hgs.heuristic_simulated_burn_list, hs.better_than_value)
f_dfs_sim = ip.f_dfs_player("FDFS_Sim",float("inf"), hgs.heuristic_simulated_burn_list, hs.better_than_value, 2)
gp_dfs_iso = ip.gp_dfs_player("GPDFS_Iso", float("inf"), hgs.heuristic_isolated_burn_list, hs.better_than_value)
f_dfs_iso = ip.f_dfs_player("FDFS_Iso",float("inf"), hgs.heuristic_isolated_burn_list, hs.better_than_value, 2)
gp_dfs_nl = ip.gp_dfs_player("GPDFS_NL", float("inf"), hgs.neighbourhood_list, hs.better_than_value)
f_dfs_nl = ip.f_dfs_player("FDFS_NL",float("inf"), hgs.neighbourhood_list, hs.better_than_value, 2)
gp_dfs_nbl = ip.gp_dfs_player("GPDFS_NBL", float("inf"), hgs.neighbourhood_burn_list, hs.better_than_value)
f_dfs_nbl = ip.f_dfs_player("FDFS_NBL",float("inf"), hgs.neighbourhood_burn_list, hs.better_than_value, 2)
gp_dfs_bpl = ip.gp_dfs_player("GPDFS_BPL", float("inf"), hgs.best_play_list, hs.better_than_value)
f_dfs_bpl = ip.f_dfs_player("FDFS_BPL",float("inf"), hgs.best_play_list, hs.better_than_value, 2)
mc = ip.mc_player("MC",100, math.sqrt(2))
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
hsb = ip.hsb_player("HBB", hs.better_than_value)
hnh = ip.hnh_player("HNH")

ALL_PLAYERS = [gns, gns_dfs , gns_hash, gp_dfs_sim, f_dfs_sim,gp_dfs_iso, f_dfs_iso, 
                mc, random, fdm_1, fdm_2, fdm_3, fdm_4, fdm_set_2_3, fdm_set_4_3, hib, hsb, hnh,
                hkn_1, hkn_2, hkn_3, hkn_4, hkn_5, hkn_6, hkn_7, hkn_8, hkn_9, hkn_10]

FINAL_PLAYERS = [gns, gns_dfs , gns_hash, 
                 f_dfs_nl, f_dfs_nbl, 
                 gp_dfs_nl, gp_dfs_nbl, gp_dfs_iso, 
                 fdm_set_4_3, fdm_set_2_3, 
                 mc, random, hib, hsb, hnh,
                 hkn_1, hkn_2, hkn_3,]

def test_players(list_players, vertex_count, iterations, file, folder):
    p.test_players_random(list_players, vertex_count, NUMBER_GEN, 100, iterations, file+"_100.csv", folder)
    p.test_players_random(list_players, vertex_count, NUMBER_GEN, 95, iterations, file+"_95.csv", folder)
    p.test_players_random(list_players, vertex_count, NUMBER_GEN, 90, iterations, file+"_90.csv", folder)
    p.test_players_random(list_players, vertex_count, NUMBER_GEN, 85, iterations, file+"_85.csv", folder)
    p.test_players_random(list_players, vertex_count, NUMBER_GEN, 80, iterations, file+"_80.csv", folder)
    p.test_players_random(list_players, vertex_count, NUMBER_GEN, 75, iterations, file+"_75.csv", folder)

    
    

def test_all_players(players, filename, foldername, sizes, iter):
    for i in sizes:
        test_players(players, i, iter, f"{filename}_{i}", foldername)
  

