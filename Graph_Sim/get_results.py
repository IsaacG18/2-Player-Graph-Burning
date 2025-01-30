import results as res

def get_time_vs_value_scatter(folder, is_player1=True, filter_name=None, title=None, data_filters=[[]]):
    data = res.combine_csv(res.get_csv_files(folder, filter_name), folder)
    dicts = [res.get_filtered_rows(data, data_filter) for data_filter in data_filters]
    data = []
    if is_player1:
        for dict in dicts:
            data = data + res.get_column_values(dict, ["Player1","Value"], True)
        
    else:
        for dict in dicts:
            data = data + res.get_column_values(dict, ["Player2","Value"], False, True)
    res.plot_scatter(data, "Value", "Times", title)


def get_multiple_distribution(folder, filter_name=None, column="Value", names_lists=None, bins=10, plot_type="hist", title=None, data_filters=[[]]):
    data = res.combine_csv(res.get_csv_files(folder, filter_name), folder)
    dicts = [res.get_filtered_rows(data, data_filter) for data_filter in data_filters]
    data = []
    xlabel = ""
    for dict in dicts:
        if type(column) == str:
            data.append(res.get_column_values(dict, column))
            xlabel = column
        elif column == True:
            data.append(res.get_column_values(dict, [], True))
            xlabel = "Total Time Taken"
        else:
            data.append(res.get_column_values(dict, [], False, True))
            xlabel = "Total Time Taken"
    res.display_multiple_distributions(data,xlabel,names_lists, bins, plot_type, title)

def get_win_rate(folder, filter_name=None,data_filters=[[]]):
    data = res.combine_csv(res.get_csv_files(folder, filter_name), folder)
    return [res.get_win_rate(dict) for dict in [res.get_filtered_rows(data, data_filter) for data_filter in data_filters]]

def get_stats(folder, filter_name=None, column="Value", data_filters=[[]]):
    data = res.combine_csv(res.get_csv_files(folder, filter_name), folder)
    dicts = [res.get_filtered_rows(data, data_filter) for data_filter in data_filters]
    data = []
    for dict in dicts:
        if type(column) == str:
            data.append(res.get_column_values(dict, column))
        elif column == True:
            data.append(res.get_column_values(dict, [], True))
        else:
            data.append(res.get_column_values(dict, [], False, True))
    return res.stats(data)
    


get_multiple_distribution("data_fdm", filter_name=None, column="Value", names_lists=["FDM_SET", "FDM2", "FDM3"], bins=10, plot_type="bar_beside", title=None,
                          data_filters=[[("Player1", "==", "FDM_SET"), ("Player2", "==", "GNSDF")], [("Player1", "==", "FDM2"), ("Player2", "==", "GNSDF")], [("Player1", "==", "FDM3"), ("Player2", "==", "GNSDF")]])
get_multiple_distribution("data_fdm", filter_name=None, column="Value", names_lists=["FDM_SET", "FDM2", "FDM3"], bins=10, plot_type="bar_beside", title=None,
                          data_filters=[[("Player2", "==", "FDM_SET"), ("Player1", "==", "GNSDF")], [("Player2", "==", "FDM2"), ("Player1", "==", "GNSDF")], [("Player2", "==", "FDM3"), ("Player1", "==", "GNSDF")]])

print(get_win_rate("data_fdm", filter_name="30",
                          data_filters=[[("Player1", "==", "FDM_SET"), ("Player2", "==", "GNSDF")], [("Player1", "==", "FDM2"), ("Player2", "==", "GNSDF")], [("Player1", "==", "FDM3"), ("Player2", "==", "GNSDF")], [("Player1", "==", "FDM4"), ("Player2", "==", "GNSDF")]]))

print(get_stats("data_fdm", filter_name="30", column="Value",
                          data_filters=[[("Player1", "==", "FDM_SET"), ("Player2", "==", "GNSDF")], [("Player1", "==", "FDM2"), ("Player2", "==", "GNSDF")], [("Player1", "==", "FDM3"), ("Player2", "==", "GNSDF")], [("Player1", "==", "FDM4"), ("Player2", "==", "GNSDF")]]))



