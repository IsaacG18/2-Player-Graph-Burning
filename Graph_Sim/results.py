
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import statistics
import const as c

# Visualization and data processing constants
FIGSIZE_X = 10 
FIGSIZE_Y = 8
BBOX_INCHES="tight"
DPI=300
ALPHA=0.7
ANNOT = True
CMAP = "YlGnBu"
ANNOT_SIZE = 10
MAP_X_LAB = "Opponent"
MAP_Y_LAB = "Player"
X_LABEL_DIS = "Player"
Y_LABEL_DIS = "Denisty"
SET_STYLE = "whitegrid"
HIST = "hist"
DEN = "density"
VIO = "violin"
BOX="box"
XTICK_FONTSIZE=20
XTICK_ROTATION=0
YTICK_FONTSIZE =20
LINEWIDTH = 1.2
SATURATION=0.75
INNER = "quartile"
PALETTE="Set2"
X_LABEL_FONTSIZE = 22
Y_LABEL_FONTSIZE = 22
LEGEND_FONTSIZE = 20
TITLE_FONTSIZE = 20

def data_csv(file_name, folder_path, data=None):
    """
    Read a CSV file and optionally concatenate with existing data.
    
    Args:
        file_name (str): Name of the CSV file to read
        folder_path (str): Path to the folder containing the file
        data (pd.DataFrame, optional): Existing DataFrame to concatenate with
    
    Returns:
        pd.DataFrame: The loaded data (concatenated with existing data if provided)
    """
    file_path = os.path.join(folder_path, file_name)
    data_new = pd.read_csv(file_path)
    if data is None or data.empty:
        data = pd.DataFrame(columns=data_new.columns)
        return data_new
    return pd.concat([data, data_new], ignore_index=True)

def combine_csv(file_list, folders):
    """
    Combine multiple CSV files into a single DataFrame.
    
    Args:
        file_list (list): List of CSV file names
        folders (str or list): Folder path(s) containing the files
    
    Returns:
        pd.DataFrame: Combined data from all CSV files
    """
    data = None 
    folder_list = folders
    if type(folders) != list:
        folder_list = [folders] * len(file_list)

    for file_name, folder_path in zip(file_list, folder_list):
        data = data_csv(file_name, folder_path, data) 
    return data

def stats(data):
    """
    Calculate basic statistics (mean, median, std dev) for each list in the input.
    
    Args:
        data (list of lists): Input data to analyze
    
    Returns:
        list: List of [mean, median, std_dev] for each input list
    """
    return_list = []
    for list in data:
        mean = statistics.mean(list)
        median = statistics.median(list)
        std_dev = statistics.stdev(list)
        return_list.append([mean,median,std_dev])
    return return_list


def plot_confusion_matrix_heatmap(confusion_matrix, players, format="d", title=None, save_path=None):
    """
    Plot a confusion matrix as a heatmap.
    
    Args:
        confusion_matrix (2D array): The confusion matrix data
        players (list): List of player names for axis labels
        format (str, optional): Format string for annotations
        title (str, optional): Plot title
        save_path (str, optional): Path to save the figure (if None, shows plot)
    """
    fig, ax = plt.subplots(figsize=(FIGSIZE_X, FIGSIZE_Y))

    sns.heatmap(
        confusion_matrix, 
        annot=ANNOT, 
        cmap=CMAP,
        fmt=format,
        xticklabels=players,
        yticklabels=players, 
        ax=ax,
        annot_kws={"size": ANNOT_SIZE}
    )
    ax.set_xlabel(MAP_X_LAB)
    ax.set_ylabel(MAP_Y_LAB)
    if title:
        plt.title(title)
    else:
        plt.title("")

    if save_path:
        plt.savefig(save_path, dpi=DPI, bbox_inches=BBOX_INCHES)  
    else:
        plt.show()


def get_filtered_rows(data, filters):
    """
    Filter rows from a DataFrame based on multiple conditions.
    
    Args:
        data (pd.DataFrame): Input data to filter
        filters (list): List of filter conditions (column, operator, value)
    
    Returns:
        list: Filtered data as a list of dictionaries
    """
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
    """
    Extract column values from a list of dictionaries.
    
    Args:
        data_dict (list of dicts): Input data
        column (str or list): Column name(s) to extract
        player1_total (bool): Whether to calculate P1 total
        player2_total (bool): Whether to calculate P2 total
    
    Returns:
        list: Extracted values
    """
    if type(column) == list and len(column)+player1_total+player2_total>1:
        extracted_data = []
        for row in data_dict:
            extracted_row = [row[key] for key in column]
            if player1_total:
                extracted_row.append(row[c.P1ST] + row[c.P1UT] + row[c.P1PT])
            if player2_total:
                extracted_row.append(row[c.P2ST] + row[c.P2UT] + row[c.P2PT])
            extracted_data.append(extracted_row)
        return extracted_data
    elif type(column) == list:
        extracted_data = []
        for row in data_dict:
            if player1_total:
                extracted_data.append(row[c.P1ST] + row[c.P1UT] + row[c.P1PT])
            elif player2_total:
                extracted_data.append(row[c.P2ST] + row[c.P2UT] + row[c.P2PT])
            else:
                extracted_data.append(row[column[0]])
        return extracted_data
    else:
        return [row[column] for row in data_dict if column in row]
    

def get_win_rate(data_dict):
    """
    Calculate win/tie/loss counts from match data.
    
    Args:
        data_dict (list of dicts): Match data containing 'VALUE' field
    
    Returns:
        tuple: (wins, ties, losses) counts
    """
    total_wins = 0
    total_ties = 0
    total_loses = 0
    for row in data_dict:
        if row[c.VALUE] > 0:
            total_wins += 1
        elif row[c.VALUE] == 0:
            total_ties += 1
        else:
            total_loses += 1
    return total_wins, total_ties, total_loses
        

    
def get_total_times(data_dict):
    """
    Calculate total times for both players.
    
    Args:
        data_dict (list of dicts): Match data
    
    Returns:
        tuple: (player1_totals, player2_totals) as lists
    """
    player1_total = []
    player2_total = []
    for row in data_dict:
        player1_total.append(row[c.P1ST] + row[c.P1UT] + row[c.P1PT])
        player2_total.append(row[c.P2ST] + row[c.P2UT] + row[c.P2PT])
    return player1_total,player2_total
    

def display_multiple_distributions(data_lists, ylabel, names_lists=None, bins=10, plot_type=HIST, title=None, save_path=None, log=False):
    """
    Display multiple distributions using various plot types.
    
    Args:
        data_lists (list of lists): Data to plot
        ylabel (str): Y-axis label
        names_lists (list, optional): Names for each distribution
        bins (int, optional): Number of bins for histograms
        plot_type (str): Type of plot (HIST, DEN, VIO, BOX)
        title (str, optional): Plot title
        save_path (str, optional): Path to save figure
        log (bool): Whether to use log scale
    """
    sns.set_style(SET_STYLE)
    plt.figure(figsize=(FIGSIZE_X, FIGSIZE_Y))
    plt.yticks(fontsize=YTICK_FONTSIZE)
    if title:
        plt.title(title, fontsize=TITLE_FONTSIZE, fontweight="bold")
    
    if names_lists is None:
        names_lists = [f"Distribution {i+1}" for i in range(len(data_lists))]


    if plot_type == VIO:
        sns.violinplot(data=data_lists, inner=INNER, palette=PALETTE, linewidth=LINEWIDTH)
        plt.xticks(range(len(names_lists)), names_lists, fontsize=XTICK_FONTSIZE,rotation=XTICK_ROTATION)

    elif plot_type == BOX:
        sns.boxplot(data=data_lists, palette=PALETTE, linewidth=LINEWIDTH, saturation=SATURATION)
        plt.xticks(range(len(names_lists)), names_lists, fontsize=XTICK_FONTSIZE,rotation=XTICK_ROTATION)

    else:
        for values, name in zip(data_lists, names_lists):
            if plot_type == HIST:
                sns.histplot(values, bins=bins, kde=False, label=name, alpha=ALPHA)
                plt.xticks(fontsize=XTICK_FONTSIZE,rotation=XTICK_ROTATION)
                plt.legend(fontsize=LEGEND_FONTSIZE)
            elif plot_type == DEN:
                sns.kdeplot(values, label=name, fill=True, alpha=ALPHA, linewidth=LINEWIDTH)
                plt.xticks( fontsize=XTICK_FONTSIZE,rotation=XTICK_ROTATION)
                plt.legend(fontsize=LEGEND_FONTSIZE)
            else:
                raise ValueError("Unsupported plot_type.")
        plt.ylabel(Y_LABEL_DIS, fontsize=X_LABEL_FONTSIZE)
        plt.xlabel(ylabel, fontsize=Y_LABEL_FONTSIZE)
        if log:
            plt.xscale('log')
        if save_path:
            plt.savefig(save_path, dpi=DPI, bbox_inches=BBOX_INCHES)
        else:
            plt.show()
        return

    plt.xlabel(X_LABEL_DIS, fontsize=X_LABEL_FONTSIZE)
    plt.yticks(fontsize=YTICK_FONTSIZE)
    plt.ylabel(ylabel, fontsize=Y_LABEL_FONTSIZE)
    if log:
        plt.yscale('log')

    if save_path:
        plt.savefig(save_path, dpi=DPI, bbox_inches=BBOX_INCHES)
    else:
        plt.show()

def get_csv_files(folder_path, substring_filter=None):
    """
    Get CSV files from a folder, optionally filtered by substring.
    
    Args:
        folder_path (str): Path to folder to search
        substring_filter (str, optional): Substring to filter filenames
    
    Returns:
        list: Matching CSV filenames
    """
    try:
        if not os.path.isdir(folder_path):
            raise FileNotFoundError(f"The folder '{folder_path}' does not exist.")
        
        csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
        
        if substring_filter:
            csv_files = [file for file in csv_files if substring_filter in file]
        
        return csv_files
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
