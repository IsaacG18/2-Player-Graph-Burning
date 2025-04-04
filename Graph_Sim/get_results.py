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
STAT_FILE = "stats.csv"
WR_FILE = "win_rate.csv"
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
FOLDER = "Last_All"
FV = ["_10_", "_15_","_20_"]
FE = [""]
EXTRA=""

# Sets what is visualised
PLOT_TYPE = res.BOX
# Set the data format for the heatmap
FORMATE = "d"

# Add filters to code this should be in the formate [(c.{COLUMN}, "{OPP}",  {EXPRESSION}), (c.{COLUMN}, "{OPP}",  {EXPRESSION}),...]
# opps include "==", ">", "!=", ">", "=>", "<=", "in", "not in"
# do not uses to select player to play against or as
FILTER=[]
# Sets distribution to be logorthimic data
LOG=True
# Set to get a heatmap
HEAT=False
# Set to get distibutions, data, stats
DATA=True
# Gets graphs of total time taken
GET_TIME=True
# Gets graphs of value of game
GET_VALUE=False


# Set if you want to VERSE to appear in the graphs
GRAPH_VERSE = False
# Set if you want to VERSE to appear in the stats
STAT_VERSE = False
VERSE = "GNSDFS"
PLAYER = FINAL_PLAYERS
G_PLAYERS, S_PLAYERS = PLAYER, PLAYER
#This decides if you run the set experiments or a custom version
CUSTOM = False

EXP_SET =   [  
               {"PLAYERS":HKN_PLAYERS,          "GV":False, "FOLDER":"Last_HKN",  "HEAT":False, "EXTRA":"",         "FVERTEX":FV},
               {"PLAYERS":FDM_PLAYERS,          "GV":False, "FOLDER":"Last_FDM",  "HEAT":False, "EXTRA":"",         "FVERTEX":FV},
               {"PLAYERS":GP_PLAYERS,            "GV":True,  "FOLDER":"Last_GP_F", "HEAT":False, "EXTRA":"G",        "FVERTEX":FV},
               {"PLAYERS":GP_PLAYERS[:-1],       "GV":True,  "FOLDER":"Last_GP_F", "HEAT":False, "EXTRA":"SIM",     "FVERTEX":FV},
               {"PLAYERS":F_PLAYERS,            "GV":True,  "FOLDER":"Last_GP_F", "HEAT":False, "EXTRA":"F",         "FVERTEX":FV},
               {"PLAYERS":MC_PLAYERS,           "GV":False, "FOLDER":"Last_MC"  , "HEAT":False, "EXTRA":"",         "FVERTEX":FV},
               {"PLAYERS":FINAL_PLAYERS,        "GV":False, "FOLDER":"Last_all" , "HEAT":False,  "EXTRA":"all1015",  "FVERTEX":FV[:-1]},
               {"PLAYERS":FINAL_PLAYERS[:-3],   "GV":False, "FOLDER":"Last_all" , "HEAT":True,  "EXTRA":"ex1015",   "FVERTEX":FV[:-1]},
               {"PLAYERS":FINAL_PLAYERS[2:],    "GV":False, "FOLDER":"Last_all" , "HEAT":True,  "EXTRA":"all20",    "FVERTEX":FV[-1:]},
               {"PLAYERS":FINAL_PLAYERS[2:-3],  "GV":False, "FOLDER":"Last_all" , "HEAT":True,  "EXTRA":"ex20",     "FVERTEX":FV[-1:]},
               ]




def get_multiple_distribution(folder, filter_name=None, column=c.VALUE, names_lists=None, bins=10, plot_type=res.HIST, title=None, data_filters=[[]], file_path=None, log=False):
    """
    
    Parameters:
        folder (str): Path to the folder containing CSV files.
        filter_name (str, optional): Filter for selecting which files
        column (str/bool): Column to be used for distribution.
        names_lists (list, optional): Names for different data groups.
        bins (int): Number of bins for histogram.
        plot_type (str): Type of plot to be displayed.
        title (str, optional): Title of the plot.
        data_filters (list): Filters applied to the data.
        file_path (str, optional): Path to save the plot.
        log (bool): Whether to apply log scaling.
    """
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
    """
    Parameters:
        folder (str): Path to the folder containing CSV files.
        filter_name (str, optional): Filter for selecting which files
        data_filters (list): Filters applied to the data.
    
    Returns:
        list: Win rate results. (WINS, DRAWS, LOSES)
    """
    data = res.combine_csv(res.get_csv_files(folder, filter_name), folder)
    try:
        return [res.get_win_rate(dict) for dict in [res.get_filtered_rows(data, data_filter) for data_filter in data_filters]]
    except AttributeError as e:
        if filter_name is None:
            raise RuntimeError(f"There is no data that comes from folder: {folder} for WR")
        else:
            raise RuntimeError(f"There is no data that comes from folder: {folder} and filter_name {filter_name} for WR")
    

def get_stats(folder, filter_name=None, column=c.VALUE, data_filters=[[]]):
    """
    
    Parameters:
        folder (str): Path to the folder containing CSV files.
        filter_name (str, optional): Filter for selecting which files
        column (str/bool): Column to be analyzed. Column name or bool for player 1 total time and false for player 2
        data_filters (list): Filters applied to the data.
    
    Returns:
        list: Computed statistics in formate [mean, medium, std, sample size]
    """
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
    """
    
    Parameters:
        players (list): List of player names.
        player_1 (bool): Determines which player to filter.
        against (str, optional): Opponent player name.
        extra (list, optional): Additional filters.
    
    Returns:
        list: Filters for data selection.
    """
    if player_1:
        return [[(c.PLAYER1, "==",  player)]+extra if against is None else [(c.PLAYER1, "==",  player), (c.PLAYER2, "==", against)]+extra for player in players]
    else:
        return [[(c.PLAYER2, "==",  player)]+extra if against is None else [(c.PLAYER2, "==",  player), (c.PLAYER1, "==", against)]+extra for player in players]
    

def get_verse_winrate(folder,fv,fe, players,win_rates, filter=[]):
    """
    Parameters:
        folder (str): Path to the folder containing CSV files.
        fv (str): Filter vertex.
        fe (str): Filter edges.
        players (list): List of player names.
        win_rates (list): List to store win rate results.
        filter (list, optional): Additional filters.
    
    Returns:
        np.array: Confusion matrix with win minuse loses.
    """
    num_players = len(players)
    confusion_matrix = np.zeros((num_players, num_players), dtype=int)
    for i in range(num_players):
        for j in range(num_players):
            result = get_win_rate(folder, filter_name=fv+fe, data_filters=player_vs_filter([players[i]], True, players[j], filter))
            win_rates.append([folder+"_"+players[i]+"_"+players[j]+fv+fe]+result)
            confusion_matrix[i, j] = result[0][0]-result[0][2]
    return confusion_matrix
    

def get_set_Plots(folder,fv,fe, players, againsts, extra = "", filters=[], log = False, pt=res.BOX):
    """
    Parameters:
        folder (str): Path to the folder containing CSV files.
        fv (str): Filter vertex.
        fe (str): Filter edges.
        players (list): List of players.
        againsts (str): opponents.
        extra (str, optional): Extra string for file naming.
        filters (list, optional): Filters to apply.
        log (bool, optional): Whether to apply log scaling.
        pt (str): Type of plot.
    """
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
    """
    
    Parameters:
        folder (str): Path to the folder containing CSV files.
        fv (str): Filter vertex.
        fe (str): Filter edges.
        players (list): List of players.
        againsts (list): List of opponents.
        win_rates (list): List to store win rates.
        filter (list, optional): Additional filters.
    
    Returns:
        list: Updated win rates list.
    """
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


def get_means_std_err(row, players):
    """
    
    Parameters:
        row (list): A row of data including mean, std, and start
        players (list): List of players.

    Returns:
        A list of means and std errors for the row
    """
    row_means = []
    row_std_errors = []
    for i in range(len(players)):
        mean = row[i+1][0]
        std = row[i+1][2]
        sample_size = row[i+1][3]
        std_error = std / np.sqrt(sample_size)
        row_means.append(mean)
        row_std_errors.append(std_error)
    return (row_means, row_std_errors)
            

def get_all_bars(folder, players,stats, fv, extra):
    """
    
    Parameters:
        folder (str): Path to the folder containing CSV files.
        players (list): List of players.
        stats (list): Statistical data.
        fv (str): Fitler vertexs
        extra (str): Extra string for file naming.
    """
    try:
        for j in [True, False]:
            first_means, first_std_err= [], []
            second_means, second_std_err = [], []
            for row in stats:
                if EVERYONE_FIRST+TI in row[0]:
                    row_means, row_std_errors = get_means_std_err(row, players)
                    first_means.append(row_means)
                    first_std_err.append(row_std_errors)
                if EVERYONE_SECOND+TI in row[0]:
                    row_means, row_std_errors = get_means_std_err(row, players)
                    second_means.append(row_means)
                    second_std_err.append(row_std_errors)
            res.create_plot(first_means, first_std_err, players, fv, j, f"{folder}{IMAGE}/{extra}{EVERYONE_FIRST}{TI}{str(j)}BAR")
            res.create_plot(second_means, second_std_err, players, fv, j, f"{folder}{IMAGE}/{extra}{EVERYONE_SECOND}{TI}{str(j)}BAR")
    except Exception as e:
        print(f"ERROR WITH BAR: {folder}, {players} {fv}, {extra}. ERROR IS {e}")


def run_tests(players, folder, gv, sv, extra,heat, fv, logs):
    """
    Parameters:
        players (list): List of players.
        folder (str): Path to the folder containing CSV files.
        gv (bool): Graph Against flag.
        sv (bool): Statistics Against flag.
        extra (str): Extra string for file naming.
        heat (bool): Whether to generate a heatmap.
        fv (list): List of Filter Vertex
        logs (list): Logging the data.
    """
    g_player = players
    s_player = players
    print(f"Wge are plotting and gathering stats from {players}")
    if gv:
        s_player = s_player +[VERSE]
        g_player = g_player +[VERSE]
    elif sv:
        s_player = s_player +[VERSE]

    print(f"We are getting data about these strategies {g_player}")
    if os.path.isdir(folder):
        os.makedirs(folder+IMAGE, exist_ok=True)
    else:
        print(f"Folder: {folder} does not exists")
        return

    if heat:
        print("We have started the Heatmap process this can take a monment")
        try:
            for v in fv:
                print(f"We are working in {v} vertices")
                win_rates=[]
                confusion_matrix =get_verse_winrate(folder,v,"", g_player, win_rates)
                res.plot_confusion_matrix_heatmap(confusion_matrix, g_player, FORMATE, TITLE,f"{folder}{IMAGE}/{PR}{v}{extra}")
        except Exception as e:
            print(f"ERROR AT PLOTTING AND DATA: {folder}, {players} {fv}, {extra}. ERROR IS: {e}")

    print(f"We are plotting and gathering stats")
    for a, log in enumerate(logs):
        print(f"Log: {log}, Plot type: {PLOT_TYPE}, Verse: {VERSE}")
        win_rates=[]
        stat=[]
        try:
            for v in fv:
                for fe in FE:
                    get_set_Plots(folder,v,fe, g_player, VERSE, extra+str(log), FILTER, log, PLOT_TYPE)
                    if a== 0:
                        get_all_WR(folder,v,fe, s_player, VERSE, win_rates, FILTER)
                        get_all_stat(folder,v,fe, s_player, VERSE, stat, FILTER)
                    
            if a== 0:
                with open(folder+IMAGE+"/"+extra+STAT_FILE, mode="w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["Names"]+s_player)
                    for row in stat:
                        writer.writerow([row[0]] + [item for item in row[1:]]) 
                with open(folder+IMAGE+"/"+extra+WR_FILE, mode="w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["Names"]+s_player)
                    for row in win_rates:
                        writer.writerow([row[0]] + [item for item in row[1:]])
                get_all_bars(folder, g_player, stat, fv, extra)
        except Exception as e:
            print(f"ERROR AT PLOTTING AND DATA: {folder}, {players} {fv}, {extra}. ERROR IS: {e}")
        
            

def main():
    if CUSTOM:
        run_tests(PLAYER, FOLDER, GRAPH_VERSE, STAT_VERSE, EXTRA,HEAT, FV, [LOG])
    else:
        for exp in EXP_SET:
            run_tests(exp["PLAYERS"], exp["FOLDER"], exp["GV"], False, exp["EXTRA"],exp["HEAT"], exp["FVERTEX"], [False, True])
        
if __name__ == "__main__":
    main()
