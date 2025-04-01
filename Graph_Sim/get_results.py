import results as res
import csv
import numpy as np
import matplotlib.pyplot as plt
import const as c
import os

# Constant that deal with folders and other infomation
TIME_LABEL ="Total Time Taken (Seconds)"
TIME_LABEL_LOG ="Total Time Taken (Seconds Scale Log)"
ALL_FIRST = "_A_F"
EVERYONE_FIRST = "_E_F"
ALL_SECOND = "_A_S"
EVERYONE_SECOND= "_E_S"
VAL = "_V"
TI = "_T"
IMAGE = "_image"
STAT_FILE = "/stats.csv"
WR_FILE = "/win_rate.csv"
PR = "PlayerRate"
TITLE=""


#Set of Experiments
FINAL_PLAYERS = [
           "GNS","Hashmap",
           "GNSDFS",
           "FDFS_NL","FDFS_NBL", 
           "GPDFS_Iso", "GPDFS_NL", "GPDFS_NBL",
           "FDM_SET_4_3", "FDM_SET_2_3", 
           "HNH", "MC150", "MC200", 
           "HKN1","HKN2",
           "HSB", "HIB", "Random",
           ]

HKN_PLAYERS = ["HKN1","HKN2", "HKN3","HKN4","HKN5", "HKN6"]

FDM_PLAYERS = ["FDM1","FDM2", "FDM3","FDM4"]

GP_PLAYERS = ["GPDFS_NL", "GPDFS_NBL", "GPDFS_BPL", "GPDFS_Iso","GPDFS_Sim"]

F_PLAYERS = ["FDFS_NL", "FDFS_NBL", "FDFS_BPL", "FDFS_Iso", "FDFS_Sim"]

MC_PLAYERS = ["MC50","MC100","MC150","MC200", "MC250"]


# Sets what is visualised
FOLDER = "Last_HKN"
FV = ["_10_", "_15_", "_20_"]
FE = ["","95", "100"]
EXTRA=""

# Sets what is visualised
PLOT_TYPE = res.BOX
FILTER=[]
LOG=False
HEAT=False
DATA=True
GET_TIME=True
GET_VALUE=False
FORMATE = "d"

# Sets out what players are used
GRAPH_VERSE = False
STAT_VERSE = False
VERSE = "GNSDFS"
PLAYER = HKN_PLAYERS
G_PLAYERS, S_PLAYERS = PLAYER, PLAYER
if GRAPH_VERSE:
    G_PLAYERS = G_PLAYERS + [VERSE]
if STAT_VERSE:
    S_PLAYERS = S_PLAYERS + [VERSE]



def get_multiple_distribution(folder, filter_name=None, column=c.VALUE, names_lists=None, bins=10, plot_type=res.HIST, title=None, data_filters=[[]], file_path=None, log=False):
    data = res.combine_csv(res.get_csv_files(folder, filter_name), folder)
    dicts = None
    try:
        dicts = [res.get_filtered_rows(data, data_filter) for data_filter in data_filters]
    except AttributeError as e:
        if filter_name is None:
            raise RuntimeError(f"There is no data that comes from folder: {folder} for distribution")
        else:
            raise RuntimeError(f"There is no data that comes from folder: {folder} and filter_name {filter_name} for distribution")
    data = [] 
    ylabel = ""
    for dict in dicts:
        if type(column) == str:
            data.append(res.get_column_values(dict, column))
            ylabel = column
        elif column == True:
            data.append(res.get_column_values(dict, [], True))
            if log:
                ylabel = TIME_LABEL_LOG
            else:
                ylabel = TIME_LABEL
        else:
            data.append(res.get_column_values(dict, [], False, True))
            if log:
                ylabel = TIME_LABEL_LOG
            else:
                ylabel = TIME_LABEL
    res.display_multiple_distributions(data,ylabel,names_lists, bins, plot_type, title, file_path, log=log)




def get_win_rate(folder, filter_name=None,data_filters=[[]]):
    data = res.combine_csv(res.get_csv_files(folder, filter_name), folder)
    try:
        return [res.get_win_rate(dict) for dict in [res.get_filtered_rows(data, data_filter) for data_filter in data_filters]]
    except AttributeError as e:
        if filter_name is None:
            raise RuntimeError(f"There is no data that comes from folder: {folder} for WR")
        else:
            raise RuntimeError(f"There is no data that comes from folder: {folder} and filter_name {filter_name} for WR")
    

def get_stats(folder, filter_name=None, column=c.VALUE, data_filters=[[]]):
    data = res.combine_csv(res.get_csv_files(folder, filter_name), folder)
    dicts = None
    try:
        dicts = [res.get_filtered_rows(data, data_filter) for data_filter in data_filters]
    except AttributeError as e:
        if filter_name is None:
            raise RuntimeError(f"There is no data that comes from folder: {folder} for stats")
        else:
            raise RuntimeError(f"There is no data that comes from folder: {folder} and filter_name {filter_name} for stats")
    data = []
    for dict in dicts:
        if type(column) == str:
            data.append(res.get_column_values(dict, column))
        elif column == True:
            data.append(res.get_column_values(dict, [], True))
        else:
            data.append(res.get_column_values(dict, [], False, True))
    try:
        return res.stats(data)
    except:
        if filter_name is None:
            print(f"There is something wrong with the data that is comes from folder: {folder}")
        else:
            print(f"There is something wrong with the data that is comes from folder: {folder} and filter_name {filter_name}")
        return []

 
    
def player_vs_filter(players, player_1, against=None, extra=[]):
    if player_1:
        return [[(c.PLAYER1, "==",  player)]+extra if against is None else [(c.PLAYER1, "==",  player), (c.PLAYER2, "==", against)]+extra for player in players]
    else:
        return [[(c.PLAYER2, "==",  player)]+extra if against is None else [(c.PLAYER2, "==",  player), (c.PLAYER1, "==", against)]+extra for player in players]
    

def get_verse_winrate(folder,fv,fe, players,win_rates, filter=[]):
    num_players = len(players)
    confusion_matrix = np.zeros((num_players, num_players), dtype=int)
    for i in range(num_players):
        for j in range(num_players):
            result = get_win_rate(folder, filter_name=fv+fe, data_filters=player_vs_filter([players[i]], True, players[j], filter))
            win_rates.append([folder+"_"+players[i]+"_"+players[j]+fv+fe]+result)
            confusion_matrix[i, j] = result[0][0]-result[0][2]
    return confusion_matrix
    

def get_set_Plots(folder,fv,fe, players, againsts, extra = "", filters=[], log = False, pt=res.BOX):
    if GET_TIME:
        get_multiple_distribution(folder, filter_name=fv+fe, column=True, names_lists=players, bins=25, plot_type=pt, title=None,
                            data_filters=player_vs_filter(players, True, againsts,filters), file_path=f"{folder}{IMAGE}/{pt}{extra}{fv}{fe}{ALL_FIRST}{TI}", log=log )
        get_multiple_distribution(folder, filter_name=fv+fe, column=False, names_lists=players, bins=25, plot_type=pt, title=None,
                            data_filters=player_vs_filter(players, False, againsts,filters), file_path=f"{folder}{IMAGE}/{pt}{extra}{fv}{fe}{ALL_SECOND}{TI}", log=log)
        get_multiple_distribution(folder, filter_name=fv+fe, column=True, names_lists=players, bins=25, plot_type=pt, title=None,
                            data_filters=player_vs_filter(players, True, extra=filters) , file_path=f"{folder}{IMAGE}/{pt}{extra}{fv}{fe}{EVERYONE_FIRST}{TI}", log=log)
        get_multiple_distribution(folder, filter_name=fv+fe, column=False, names_lists=players, bins=25, plot_type=pt, title=None,
                            data_filters=player_vs_filter(players, False, extra=filters), file_path=f"{folder}{IMAGE}/{pt}{extra}{fv}{fe}{EVERYONE_SECOND}{TI}", log=log)
    if GET_VALUE:
        get_multiple_distribution(folder, filter_name=fv+fe, column=c.VALUE, names_lists=players, bins=25, plot_type=pt, title=None,
                            data_filters=player_vs_filter(players, True, againsts,filters), file_path=f"{folder}{IMAGE}/{pt}{extra}{fv}{fe}{ALL_FIRST}{VAL}", log=log )
        get_multiple_distribution(folder, filter_name=fv+fe, column=c.VALUE, names_lists=players, bins=25, plot_type=pt, title=None,
                            data_filters=player_vs_filter(players, False, againsts,filters), file_path=f"{folder}{IMAGE}/{pt}{extra}{fv}{fe}{ALL_SECOND}{VAL}", log=log)
        get_multiple_distribution(folder, filter_name=fv+fe, column=c.VALUE, names_lists=players, bins=25, plot_type=pt, title=None,
                            data_filters=player_vs_filter(players, True, extra=filters) , file_path=f"{folder}{IMAGE}/{pt}{extra}{fv}{fe}{EVERYONE_FIRST}{VAL}", log=log)
        get_multiple_distribution(folder, filter_name=fv+fe, column=c.VALUE, names_lists=players, bins=25, plot_type=pt, title=None,
                            data_filters=player_vs_filter(players, False, extra=filters), file_path=f"{folder}{IMAGE}/{pt}{extra}{fv}{fe}{EVERYONE_SECOND}{VAL}", log=log)


def get_all_WR(folder,fv,fe, players, againsts, win_rates,filter=[]):
    win_rates.append([folder+ALL_FIRST+fv+fe]+get_win_rate(folder, filter_name=fv+fe,data_filters=player_vs_filter(players, True, againsts,filter)))
    win_rates.append([folder+ALL_SECOND+fv+fe]+get_win_rate(folder, filter_name=fv+fe,data_filters=player_vs_filter(players, False, againsts,filter)))
    win_rates.append([folder+EVERYONE_FIRST+fv+fe]+get_win_rate(folder, filter_name=fv+fe,data_filters=player_vs_filter(players, True,extra=filter)))
    win_rates.append([folder+EVERYONE_SECOND+fv+fe]+get_win_rate(folder, filter_name=fv+fe,data_filters=player_vs_filter(players, False,extra=filter)))
    return win_rates

def get_all_stat(folder,fv,fe, players, againsts,stat,filter=[]):
    stat.append([folder+ALL_FIRST+TI+fv+fe]+get_stats(folder, filter_name=fv+fe,column=True,data_filters=player_vs_filter(players, True, againsts,filter)))
    stat.append([folder+ALL_SECOND+TI+fv+fe]+get_stats(folder, filter_name=fv+fe, column=False, data_filters=player_vs_filter(players, False, againsts,filter)))
    stat.append([folder+EVERYONE_FIRST+TI+fv+fe]+get_stats(folder, filter_name=fv+fe, column=True, data_filters=player_vs_filter(players, True,extra=filter)))
    stat.append([folder+EVERYONE_SECOND+TI+fv+fe]+get_stats(folder, filter_name=fv+fe, column=False, data_filters=player_vs_filter(players, False,extra=filter)))
    stat.append([folder+ALL_FIRST+VAL+fv+fe]+get_stats(folder, filter_name=fv+fe, data_filters=player_vs_filter(players, True, againsts,filter)))
    stat.append([folder+ALL_SECOND+VAL+fv+fe]+get_stats(folder, filter_name=fv+fe, data_filters=player_vs_filter(players, False, againsts,filter)))
    stat.append([folder+EVERYONE_FIRST+VAL+fv+fe]+get_stats(folder, filter_name=fv+fe, data_filters=player_vs_filter(players, True,extra=filter)))
    stat.append([folder+EVERYONE_SECOND+VAL+fv+fe]+get_stats(folder, filter_name=fv+fe, data_filters=player_vs_filter(players, False,extra=filter)))

def main():
    if os.path.isdir(FOLDER):
        os.makedirs(FOLDER+IMAGE, exist_ok=True)
    else:
        print(f"Folder: {FOLDER} does not exists")
        return

    if HEAT:
        for i in FV:
            win_rates=[]
            confusion_matrix =get_verse_winrate(FOLDER,i,"", G_PLAYERS, win_rates)
            res.plot_confusion_matrix_heatmap(confusion_matrix, G_PLAYERS, FORMATE, TITLE,f"{FOLDER}{IMAGE}/{PR}{i}")

    if DATA:
        win_rates=[]
        stat=[]
        for fv in FV:
            for fe in FE:
                get_set_Plots(FOLDER,fv,fe, G_PLAYERS, VERSE, EXTRA, FILTER, LOG, PLOT_TYPE)
                get_all_WR(FOLDER,fv,fe, S_PLAYERS, VERSE, win_rates, FILTER)
                get_all_stat(FOLDER,fv,fe, S_PLAYERS, VERSE, stat, FILTER)
                        
        with open(FOLDER+IMAGE+STAT_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Names"]+S_PLAYERS)
            for row in stat:
                writer.writerow([row[0]] + [item for item in row[1:]]) 
        with open(FOLDER+IMAGE+WR_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Names"]+S_PLAYERS)
            for row in win_rates:
                writer.writerow([row[0]] + [item for item in row[1:]]) 
if __name__ == "__main__":
    main()