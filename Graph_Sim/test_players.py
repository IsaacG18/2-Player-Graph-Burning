import holsticSearch as hs
import instatuated_player as ip
import heuristic_guided_search as hgs
import play as p
import math

NUMBER_GEN = 100
SPLIT_HIGH = 90
SPLIT_MIDDLE = 70
SPLIT_LOW = 50
SPLIT_LOWEST = 30

p1_1 = ip.gns_player("GNS", float("inf"))
p1_mm_1 = ip.gns_mini_max_player("GNSMM", float("inf"))
p1_hash_1 = ip.gns_mini_max_player("Hashmap", float("inf"))
p2_psmm = ip.psmm_player("PSMM", float("inf"), hgs.heuristicBurnList, hs.betterThanValue)
p2_fsmm = ip.fsmm_player("FSMM",float("inf"), hgs.heuristicBurnList, hs.betterThanValue, 2)
p2_psmm_1 = ip.psmm_player("PSMM Iso", float("inf"), hgs.heuristicBurnListIsolated, hs.betterThanValue)
p2_fsmm_1 = ip.fsmm_player("FSMM Iso",float("inf"), hgs.heuristicBurnListIsolated, hs.betterThanValue, 2)
p3_mc = ip.mc_player("MC",100, math.sqrt(2))
p3_random = ip.random_player("Random")
p4_hma_1 = ip.hma_player("HMA1", 1)
p4_hmc_1 = ip.hmc_player("HMC1", 1)
p4_hma_2 = ip.hma_player("HMA2", 2)
p4_hmc_2 = ip.hmc_player("HMC2", 2)
p4_hma_3 = ip.hma_player("HMA3", 3)
p4_hmc_3 = ip.hmc_player("HMC3", 3)
p4_hma_4 = ip.hma_player("HMA3", 4)
p4_hmc_4 = ip.hmc_player("HMC4", 4)
p4_hma_5 = ip.hma_player("HMA5", 5)
p4_hmc_5 = ip.hmc_player("HMC5", 5)
p4_hmc_6 = ip.hmc_player("HMC6", 6)
p4_hmc_7 = ip.hmc_player("HMC7", 7)
p4_hmc_8 = ip.hmc_player("HMC8", 8)
p4_hmc_9 = ip.hmc_player("HMC9", 9)
p4_hmc_10 = ip.hmc_player("HMC10", 10)
p4_hihb = ip.hihb_player("HIHB", hs.betterThanValue)
p4_hmc = ip.hhb_player("HBB", hs.betterThanValue)

# test_players_random([p1_1, p1_mm_1, p1_hash_1, p2_psmm, p2_fsmm, p3_mc, p3_random, p4_hma, p4_hmc, p4_hihb, p4_hmc],10, 10, 9, 10, "test.csv")

def test_players(list_players, vertex_count, iterations, file, folder):
    p.test_players_random(list_players, vertex_count, NUMBER_GEN, SPLIT_HIGH, iterations, "HIGH_"+file, folder)
    p.test_players_random(list_players, vertex_count, NUMBER_GEN, SPLIT_MIDDLE, iterations, "MID_"+file, folder)
    p.test_players_random(list_players, vertex_count, NUMBER_GEN, SPLIT_LOW, iterations, "LOW_"+file, folder)
    p.test_players_random(list_players, vertex_count, NUMBER_GEN, SPLIT_LOWEST, iterations, "LOWEST_"+file, folder)

def test_hash():
    test_players([p1_1, p1_mm_1, p1_hash_1, p2_psmm, p2_fsmm,p2_psmm_1, p2_fsmm_1], 5, 100, "TreeSearch_5.csv", "data_heuristic")
    test_players([p1_1, p1_mm_1, p1_hash_1, p2_psmm, p2_fsmm,p2_psmm_1, p2_fsmm_1], 10, 100, "TreeSearch_10.csv", "data_heuristic")
    test_players([p1_1, p1_mm_1, p1_hash_1, p2_psmm, p2_fsmm,p2_psmm_1, p2_fsmm_1], 15, 50, "TreeSearch_15.csv", "data_heuristic")
    test_players([p1_1, p1_mm_1, p1_hash_1, p2_psmm, p2_fsmm,p2_psmm_1, p2_fsmm_1], 20, 30, "TreeSearch_20.csv", "data_heuristic")
    test_players([p1_mm_1, p1_hash_1, p2_psmm, p2_fsmm,p2_psmm_1, p2_fsmm_1], 25, 30, "TreeSearch_25.csv", "data_heuristic")
    test_players([p1_mm_1, p1_hash_1, p2_psmm, p2_fsmm,p2_psmm_1, p2_fsmm_1], 30, 30, "TreeSearch_30.csv", "data_heuristic")


def test_heurisitic():
    hp = [p4_hma_1, p4_hmc_1, p4_hma_2, p4_hmc_2, p4_hma_3,p4_hmc_3, p4_hma_4, p4_hmc_4, p4_hma_5, p4_hmc_5, p4_hmc_6, p4_hmc_7, p4_hmc_8, p4_hmc_9, p4_hmc_10]
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

