import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Process Performance Graphs - Page 2
def ip_graphs_1(dfs, col_names):
    process = dfs['In Process Data Summary']
    fold_expansion = (process.loc[process['Batch #'] == 'Pre Harvest Fold Expansion']).values[0].tolist()[1:]
    
    cell_growth_7 = (process.loc[process['Batch #'] == 'Day 7 Viability (%)'].values[0].tolist())[1:] # Day 7 viability 
    cell_growth_7 = cell_growth_7
    cell_growth_0_r = process.loc[process['Batch #'] == 'Actual Cell Number for Culture'].values[0].tolist()[1:]
    cell_growth_6_r = process.loc[process['Batch #'] == 'Day 6 Total viable cells'].values[0].tolist()[1:]
    cell_growth_7_r = process.loc[process['Batch #'] == 'Day 7 Total Viable cells'].values[0].tolist()[1:] #if NA skip
    cell_growth_8_r = process.loc[process['Batch #'] == 'Harvest -1Day Total Viable Cells'].values[0].tolist()[1:] # cell growth harvest -1
    cell_growth_9_r = process.loc[process['Batch #'] == 'Pre Harvest Total Viable Cells'].values[0].tolist()[1:] # cell growth harvest 


    fig_sub_process_2 = make_subplots(rows=1, cols=2, subplot_titles=("Fold Expansion Over Process", "Cell Growth Over Process"))
    fig_sub_process_2.add_trace(go.Bar(name='', x=col_names, y=fold_expansion, showlegend=False), row=1, col=1)
    x_axis = ["0", "6", "7", "8", "9"]
    for i in range(len(col_names)):
        list_ = [cell_growth_0_r[i], cell_growth_6_r[i]] 
        if pd.isna(cell_growth_7[i]):
            list_.extend([cell_growth_8_r[i], cell_growth_9_r[i]])
        else:
            list_.extend([cell_growth_7_r[i], cell_growth_8_r[i], cell_growth_9_r[i]])
        fig_sub_process_2.add_trace(go.Scatter(x=x_axis, y=list_, name=col_names[i]), row = 1, col = 2)

    fig_sub_process_2.update_layout(title={'text': "Process Performance", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
    return fig_sub_process_2

# Process Performance Graphs - Page 3
def ip_graphs_2(dfs, col_names):
    data_frame = dfs["QC Release Results Summary"]
    process = dfs['In Process Data Summary']
    viability_aph = (process.loc[process['Batch #'] == 'Diluted Apheresis Viability (%)']).values[0].tolist()[1:]
    cell_via_0_aph = viability_aph
    cell_via_0_post = (process.loc[process['Batch #'] == 'Post Enrichment Average Viability (%)'].values[0].tolist())[1:] # viability % 
    cell_via_0_post = cell_via_0_post
    cell_growth_6 = (process.loc[process['Batch #'] == 'Day 6 Viability (%)'].values[0].tolist())[1:] # Day 6 viability
    cell_growth_6 = cell_growth_6
    cell_growth_7 = (process.loc[process['Batch #'] == 'Day 7 Viability (%)'].values[0].tolist())[1:] # Day 7 viability 
    cell_growth_7 = cell_growth_7
    cell_growth_8 = (process.loc[process['Batch #'] == 'Harvest -1Day Viability (%)'].values[0].tolist())[1:] # Day 8 viability 
    cell_growth_8 = cell_growth_8
    cell_growth_9_pre = (process.loc[process['Batch #'] == 'Pre Harvest Viability (%)'].values[0].tolist())[1:] # Day 9 Pre-harvest viability
    cell_growth_9_pre = cell_growth_9_pre
    cell_growth_9_post = (process.loc[process['Batch #'] == 'Post Harvest Average Viability (%)'].values[0].tolist())[1:]  # Day 9 Post-harvest viability
    cell_growth_9_post = cell_growth_9_post
    cell_growth_fdp = (data_frame.loc[data_frame['Unnamed: 1'] == 'Viability'].values[0].tolist())[4:] # % Viability 
    cell_growth_fdp = cell_growth_fdp

    #In Process Cell Viability% Graphs - Page 3
    fig_sub_process_3 = make_subplots(rows=2, cols=2, subplot_titles=("Cell Viability over Process", "Cell Viability (Aph. - d6)", "Cell Viability (Pre- and Post-Harvest, FDP)"))
    x_axis = ["0 (Aph)", "0 (Post)", "6", "7", "8", "9 (Pre)", "9 (Post)", "FDP"]
    colors2 = ["yellow", "orange", "red", "green", "blue", "goldenrod", "magenta", "blue", "purple", "pink", "grey", ]
    for i in range(len(col_names)):
        list_ = [cell_via_0_aph[i], cell_via_0_post[i], cell_growth_6[i]]
        if pd.isna(cell_growth_7[i]):
            list_.extend([cell_growth_8[i], cell_growth_9_pre[i], cell_growth_9_post[i], cell_growth_fdp[i]])
        else:
            list_.extend([cell_growth_7[i], cell_growth_8[i], cell_growth_9_pre[i], cell_growth_9_post[i], cell_growth_fdp[i]])
        fig_sub_process_3.add_trace(go.Scatter(x=x_axis, y=list_, name=col_names[i], marker_color=colors2[i]), row = 1, col = 1)
    x_axis = ["0 (Aph)", "0 (Post)", "6"]
    for i in range(len(col_names)):
        list_ = [cell_via_0_aph[i], cell_via_0_post[i], cell_growth_6[i]]
        fig_sub_process_3.add_trace(go.Scatter(x=x_axis, y=list_, name=col_names[i], marker_color=colors2[i], showlegend=False), row = 1, col = 2)
    x_axis = [ "9 (Pre)", "9 (Post)", "FDP"]
    for i in range(len(col_names)):
        list_ = [cell_growth_9_pre[i], cell_growth_9_post[i], cell_growth_fdp[i]]
        fig_sub_process_3.add_trace(go.Scatter(x=x_axis, y=list_, name=col_names[i], marker_color=colors2[i], showlegend=False), row = 2, col = 1)
    fig_sub_process_3.update_layout(title={'text': "Process Performance", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})

    fig_sub_process_3.update_yaxes(range=[50, 100] , row=1, col=1)
    fig_sub_process_3.update_yaxes(range=[50, 100] , row=1, col=2)
    fig_sub_process_3.update_yaxes(range=[85, 100] , row=2, col=1)

    return fig_sub_process_3
