import Graph_Sim.heurstic_search as hs
import instatuated_player as ip
import heuristic_guided_search as hgs
import play as p
import math

NUMBER_GEN = 100
SPLIT_HIGH = 90
SPLIT_MIDDLE = 70
SPLIT_LOW = 50
SPLIT_LOWEST = 30

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
fdm_set = ip.fdm_set_player("FDM_SET")
hib = ip.hib_player("HIB", hs.better_than_value)
hsb = ip.hsb_player("HBB", hs.better_than_value)


def test_players(list_players, vertex_count, iterations, file, folder):
    p.test_players_random(list_players, vertex_count, NUMBER_GEN, SPLIT_HIGH, iterations, "HIGH_"+file, folder)
    p.test_players_random(list_players, vertex_count, NUMBER_GEN, SPLIT_MIDDLE, iterations, "MID_"+file, folder)
    p.test_players_random(list_players, vertex_count, NUMBER_GEN, SPLIT_LOW, iterations, "LOW_"+file, folder)
    p.test_players_random(list_players, vertex_count, NUMBER_GEN, SPLIT_LOWEST, iterations, "LOWEST_"+file, folder)

def test_hash():
    test_players([gns, gns_dfs , gns_hash, gp_dfs_sim, f_dfs_sim,gp_dfs_iso, f_dfs_iso], 5, 100, "TreeSearch_5.csv", "data_heuristic")
    test_players([gns, gns_dfs , gns_hash, gp_dfs_sim, f_dfs_sim,gp_dfs_iso, f_dfs_iso], 10, 100, "TreeSearch_10.csv", "data_heuristic")
    test_players([gns, gns_dfs , gns_hash, gp_dfs_sim, f_dfs_sim,gp_dfs_iso, f_dfs_iso], 15, 50, "TreeSearch_15.csv", "data_heuristic")
    test_players([gns, gns_dfs , gns_hash, gp_dfs_sim, f_dfs_sim,gp_dfs_iso, f_dfs_iso], 20, 30, "TreeSearch_20.csv", "data_heuristic")
    test_players([gns_dfs , gns_hash, gp_dfs_sim, f_dfs_sim,gp_dfs_iso, f_dfs_iso], 25, 30, "TreeSearch_25.csv", "data_heuristic")
    test_players([gns_dfs , gns_hash, gp_dfs_sim, f_dfs_sim,gp_dfs_iso, f_dfs_iso], 30, 30, "TreeSearch_30.csv", "data_heuristic")


def test_heurisitic():
    hp = [hkn_1, hkn_2, hkn_3, hkn_4, hkn_5, hkn_6, hkn_7, hkn_8, hkn_9, hkn_10]
    test_players(hp, 10, 100, "Heurisitic_10.csv", "data_heuristic")
    test_players(hp, 20, 100, "Heurisitic_20.csv", "data_heuristic")
    test_players(hp, 30, 100, "Heurisitic_30.csv", "data_heuristic")
    test_players(hp, 40, 100, "Heurisitic_40.csv", "data_heuristic")
    test_players(hp, 50, 100, "Heurisitic_50.csv", "data_heuristic")
    test_players(hp, 60, 100, "Heurisitic_60.csv", "data_heuristic")
    test_players(hp, 70, 100, "Heurisitic_70.csv", "data_heuristic")
    test_players(hp, 80, 100, "Heurisitic_80.csv", "data_heuristic")
    test_players(hp, 90, 100, "Heurisitic_90.csv", "data_heuristic")
    test_players(hp, 100, 100, "Heurisitic_100.csv", "data_heuristic")
   


test_heurisitic()

