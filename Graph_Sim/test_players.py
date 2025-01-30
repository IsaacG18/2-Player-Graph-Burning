import heurstic_search as hs
import instatuated_player as ip
import heuristic_guided_search as hgs
import play as p
import math

NUMBER_GEN = 100


gns = ip.gns_player("GNS", float("inf"))
gns_dfs  = ip.gns_dfs_player("GNSDF", float("inf"))
gns_hash = ip.gns_hashmap_player("Hashmap", float("inf"))
gp_dfs_sim = ip.gp_dfs_player("GPDFS Sim", float("inf"), hgs.heuristic_simulated_burn_list, hs.better_than_value)
f_dfs_sim = ip.f_dfs_player("FDFS Sim",float("inf"), hgs.heuristic_simulated_burn_list, hs.better_than_value, 2)
gp_dfs_iso = ip.gp_dfs_player("GPDFS Iso", float("inf"), hgs.heuristic_isolated_burn_list, hs.better_than_value)
f_dfs_iso = ip.f_dfs_player("FDFS Iso",float("inf"), hgs.heuristic_isolated_burn_list, hs.better_than_value, 2)
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

ALL_PLAYERS = [gns, gns_dfs , gns_hash, gp_dfs_sim, f_dfs_sim,gp_dfs_iso, f_dfs_iso, 
                mc, random, fdm_1, fdm_2, fdm_3, fdm_4, fdm_set_2_3, fdm_set_4_3, hib, hsb,
                hkn_1, hkn_2, hkn_3, hkn_4, hkn_5, hkn_6, hkn_7, hkn_8, hkn_9, hkn_10]

TEST_PLAYERS = [gns, gns_dfs , gns_hash, gp_dfs_sim, f_dfs_sim,gp_dfs_iso, f_dfs_iso, mc, random, fdm_set_2_3, fdm_set_4_3, fdm_4, hib, hsb, hkn_2]

def test_players(list_players, vertex_count, iterations, file, folder):
    p.test_players_random(list_players, vertex_count, NUMBER_GEN, 100, iterations, file+"_100.csv", folder)
    p.test_players_random(list_players, vertex_count, NUMBER_GEN, 95, iterations, file+"_95.csv", folder)
    p.test_players_random(list_players, vertex_count, NUMBER_GEN, 90, iterations, file+"_90.csv", folder)
    p.test_players_random(list_players, vertex_count, NUMBER_GEN, 85, iterations, file+"_85.csv", folder)
    p.test_players_random(list_players, vertex_count, NUMBER_GEN, 80, iterations, file+"_80.csv", folder)
    p.test_players_random(list_players, vertex_count, NUMBER_GEN, 75, iterations, file+"_75.csv", folder)

def test_hash():
    test_players([gns, gns_dfs , gns_hash, gp_dfs_sim, f_dfs_sim,gp_dfs_iso, f_dfs_iso], 5, 100, "TreeSearch_5", "data_heuristic")
    test_players([gns, gns_dfs , gns_hash, gp_dfs_sim, f_dfs_sim,gp_dfs_iso, f_dfs_iso], 10, 100, "TreeSearch_10", "data_heuristic")
    test_players([gns, gns_dfs , gns_hash, gp_dfs_sim, f_dfs_sim,gp_dfs_iso, f_dfs_iso], 15, 50, "TreeSearch_15", "data_heuristic")
    test_players([gns, gns_dfs , gns_hash, gp_dfs_sim, f_dfs_sim,gp_dfs_iso, f_dfs_iso], 20, 30, "TreeSearch_20", "data_heuristic")
    test_players([gns_dfs , gns_hash, gp_dfs_sim, f_dfs_sim,gp_dfs_iso, f_dfs_iso], 25, 30, "TreeSearch_25", "data_heuristic")
    test_players([gns_dfs , gns_hash, gp_dfs_sim, f_dfs_sim,gp_dfs_iso, f_dfs_iso], 30, 30, "TreeSearch_30", "data_heuristic")


def test_heurisitic():
    # hp = [hkn_1, hkn_2, hkn_3, hkn_4, hkn_5, hkn_6, hkn_7, hkn_8, gns_dfs]
    hp = [fdm_1, fdm_2, fdm_3, fdm_4, fdm_set_4_3, fdm_set_2_3, gns_dfs]
    test_players(hp, 10, 50, "fdm_10", "data_fdm_2")
    test_players(hp, 20, 50, "fdm_20", "data_fdm_2")
    test_players(hp, 30, 50, "fdm_30", "data_fdm_2")
    
    

def test_all_players(players):
    # test_players(players, 10, 50, "all_10", "all_data")
    # test_players(players, 15, 50, "all_15", "all_data")
    test_players(players, 20, 50, "all_20", "all_data")
   
test_heurisitic()

