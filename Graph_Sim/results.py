
import os
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
import pandas as pd
import statistics
import numpy as np


def data_csv(file_name, folder_path, data=None):
    file_path = os.path.join(folder_path, file_name)
    data_new = pd.read_csv(file_path)
    if data is None or data.empty:
        data = pd.DataFrame(columns=data_new.columns)
        return data_new
    return pd.concat([data, data_new], ignore_index=True)

def combine_csv(file_list, folders):
    data = None 
    folder_list = folders
    if type(folders) != list:
        folder_list = [folders] * len(file_list)

    for file_name, folder_path in zip(file_list, folder_list):
        data = data_csv(file_name, folder_path, data) 
    return data

def stats(data):
    return_list = []
    for list in data:
        mean = statistics.mean(list)
        median = statistics.median(list)
        std_dev = statistics.stdev(list)
        return_list.append([mean,median,std_dev])
    return return_list
        


def plot_scatter(data, xLabel, yLabel, title=None, save_path=None):
    plt.figure(figsize=(10, 5))
    grouped_data = defaultdict(lambda: ([], []))
    for p1_name, X, Y in data:
        grouped_data[p1_name][0].append(X)
        grouped_data[p1_name][1].append(Y)

    for p1_name, (X, Y) in grouped_data.items():
        plt.scatter(X, Y, label=p1_name, alpha=0.7)
    if title:
        plt.title(title)
    else:
        plt.title("Scatter Plot")
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.legend()
    plt.grid(True)
    plt.legend(title="Distributions")
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")  
    else:
        plt.show()



def get_filtered_rows(data, filters):

    filtered_data = data.copy()


    for col, op, value in filters:
        if op == "==":
            filtered_data = filtered_data[filtered_data[col] == value]
        elif op == "!=":
            filtered_data = filtered_data[filtered_data[col] != value]
        elif op == ">":
            filtered_data = filtered_data[filtered_data[col] > value]
        elif op == ">=":
            filtered_data = filtered_data[filtered_data[col] >= value]
        elif op == "<":
            filtered_data = filtered_data[filtered_data[col] < value]
        elif op == "<=":
            filtered_data = filtered_data[filtered_data[col] <= value]
        elif op == "in":
            filtered_data = filtered_data[filtered_data[col].isin(value)]
        elif op == "not in":
            filtered_data = filtered_data[~filtered_data[col].isin(value)]
        else:
            raise ValueError(f"Unsupported operator: {op}")

    return filtered_data.to_dict(orient="records")

def get_column_values(data_dict, column, player1_total=False, player2_total=False):
    if type(column) == list and len(column)+player1_total+player2_total>1:
        extracted_data = []
        for row in data_dict:
            extracted_row = [row[key] for key in column]
            if player1_total:
                extracted_row.append(row["P1SetupTime"] + row["P1UpdateTime"] + row["P1PlayTime"])
            if player2_total:
                extracted_row.append(row["P2SetupTime"] + row["P2UpdateTime"] + row["P2PlayTime"])
            extracted_data.append(extracted_row)
        return extracted_data
    elif type(column) == list:
        extracted_data = []
        for row in data_dict:
            if player1_total:
                extracted_data.append(row["P1SetupTime"] + row["P1UpdateTime"] + row["P1PlayTime"])
            elif player2_total:
                extracted_data.append(row["P2SetupTime"] + row["P2UpdateTime"] + row["P2PlayTime"])
            else:
                extracted_data.append(row[column[0]])
        return extracted_data
    else:
        return [row[column] for row in data_dict if column in row]
    

def get_win_rate(data_dict):
    total_wins = 0
    total_ties = 0
    total_loses = 0
    for row in data_dict:
        if row["Value"] > 0:
            total_wins += 1
        elif row["Value"] == 0:
            total_ties += 1
        else:
            total_loses += 1
    return total_wins, total_ties, total_loses
        

    
def get_total_times(data_dict):
    player1_total = []
    player2_total = []
    for row in data_dict:
        player1_total.append(row["P1SetupTime"] + row["P1UpdateTime"] + row["P1PlayTime"])
        player2_total.append(row["P2SetupTime"] + row["P2UpdateTime"] + row["P2PlayTime"])
    return player1_total,player2_total
    

def display_multiple_distributions(data_lists, ylabel, names_lists=None, bins=10, plot_type="hist", title=None, save_path=None):
    plt.figure(figsize=(10, 6))
    if names_lists is None: names_lists = [f"Distribution {i+1}" for i in range(len(data_lists))]
    if plot_type == "bar_beside":
            labels = []
            handles = []
            unique_values = sorted(set(np.concatenate(data_lists)))
            bar_width = 0.8 / len(data_lists)
            for i, values in enumerate(data_lists):
                counts = [values.count(uv) if uv in values else 0 for uv in unique_values]
                bars = plt.bar([uv + i * bar_width for uv in unique_values], counts, width=bar_width, alpha=0.6, label=names_lists[i])
                if names_lists[i] not in labels:
                    handles.append(bars[0])
                    labels.append(names_lists[i])
    elif plot_type == "violin":
        sns.violinplot(data=data_lists, inner="quartile")
        plt.xticks(range(len(names_lists)), names_lists)
    else:
        for values, name in zip(data_lists, names_lists):
            if plot_type == "hist":
                sns.histplot(values, bins=bins, kde=False, label=name, alpha=0.3)
            elif plot_type == "density":
                sns.kdeplot(values, label=name, fill=True, alpha=0.3)
            elif plot_type == "bar":
                unique_values, counts = np.unique(values, return_counts=True)
                plt.bar(unique_values, counts, alpha=0.3, label=name)
            else:
                raise ValueError("Unsupported plot_type. Use 'hist' or 'density'.")
    
    if title:
        plt.title(title)

    
    plt.xlabel("Players")
    plt.ylabel(ylabel)

    # plt.legend(title="Distributions")
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")  
    else:
        plt.show()

def get_csv_files(folder_path, substring_filter=None):
    try:
        if not os.path.isdir(folder_path):
            raise FileNotFoundError(f"The folder '{folder_path}' does not exist.")
        
        # Get all .csv files
        csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
        
        # Apply substring filter if provided
        if substring_filter:
            csv_files = [file for file in csv_files if substring_filter in file]
        
        return csv_files
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# data = combine_csv(["Heurisitic_30_95.csv","Heurisitic_30_100.csv"],["data_heuristic","data_heuristic"])
# data = combine_csv(["Heurisitic_30_95.csv","Heurisitic_30_100.csv"],"data_heuristic")




# display_multiple_distributions([get_column_values(dict_1, "Value"), get_column_values(dict_2, "Value")], "Value", ["FDM_SET", "FDM2"])



