import pandas as pd
from flask import Flask, render_template, request, send_file, jsonify
# import data_vis
from flask_cors import CORS
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pathlib, webbrowser
from itertools import chain
import pathlib
import webbrowser, os
import random
import colour


app = Flask(__name__, static_url_path='/static')
CORS(app)

@app.route('/')
def index():
    return jsonify({'message': 'Hello from the backend!'})

@app.route('/process-datavis', methods=['POST'])
def process_datavis():
    global_sheet = request.files['fileInput']
    # data_vis.visualization(global_sheet)
   # return jsonify({'message': 'Data visualization processed successfully'})
    xls = pd.ExcelFile(global_sheet)

    # Read the Excel file into a dictionary of DataFrames
    dfs = {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names}

    data_frame = dfs["Analytical Result trend"] 

    #GRAPH FOR %CAR+ FDP
    col_names = list(data_frame.columns.values.tolist())
    col_names = col_names[4:]

    #row 10 is %CAR of final DP
    row_list = (data_frame.loc[10, :].values.tolist())[4:]

    #purity
    purity = (data_frame.loc[9, :].values.tolist())[4:]

    #vcn
    vcn = (data_frame.loc[11, :].values.tolist())[4:]

    #viability % viable cells
    via = (data_frame.loc[2, :].values.tolist())[4:]

    #actual dose 
    dose = (data_frame.loc[7, :].values.tolist())[4:]

    multiplied_list = list(map(lambda x: x * 100, row_list))
    y_mean = np.mean(multiplied_list)
    std = np.std(multiplied_list)
    two_plussd = y_mean + 2*std
    two_minussd = y_mean - 2*std

    fig = px.scatter(y=multiplied_list, x=col_names, range_y = [0,100], labels={'y':'%CAR+ Cells'}, title="Identity and Potency (%CAR+ Cells)")
    fig.add_trace(go.Scatter(x=col_names, y=[y_mean] * len(col_names), mode='lines', name='Mean'))
    fig.add_trace(go.Scatter(x=col_names, y=[two_plussd] * len(col_names), mode='lines', name='+2SD'))
    fig.add_trace(go.Scatter(x=col_names, y=[two_minussd] * len(col_names), mode='lines', name='-2SD'))
    fig.update_traces(marker_size=10)
    #fig.show()

    purity_ = list(map(lambda x: x * 100, purity))
    y_mean_purity = np.mean(purity_)
    std_p = np.std(purity_)
    two_plussd_p = y_mean_purity + 2*std_p
    two_minussd_p = y_mean_purity - 2*std_p

    vcn_ = vcn
    y_mean_vcn = np.mean(vcn_ )
    std_vcn = np.std(vcn_ )
    two_plussd_vcn = y_mean_vcn + 2*std_vcn
    two_minussd_vcn = y_mean_vcn - 2*std_vcn


    via_ = list(map(lambda x: x * 100, via))
    y_mean_via = np.mean(via_)
    std_via = np.std(via_)
    two_plussd_via = y_mean_via + 2*std_via
    two_minussd_via = y_mean_via - 2*std_via

    y_mean_dose = np.mean(dose)
    std_dose = np.std(dose)
    two_plussd_dose = y_mean_dose + 2*std_dose
    two_minussd_dose = y_mean_dose - 2*std_dose 


    #Graph for %CAR+ D8 and D9
    #row 5 is D8 CAR
    row_list_2 = (data_frame.loc[5, :].values.tolist())[4:]
    multiplied_list_2 = list(map(lambda x: x * 100, row_list_2))

    fig_2 = go.Figure()
    x_axis = ["Day 8", "Day 9"]
    for i in range(len(col_names)):
        list_ = [multiplied_list_2[i], multiplied_list[i]]
        fig_2.add_trace(go.Scatter(x=x_axis, y=list_, name=col_names[i]))
    fig_2.update_layout(title={'text': "%CAR+ Cells (Day 8 and Day 9)",'font': {'size': 24,'color': 'blue'}, 'x': 0.5 })  # Set the title's x position to the center
    #fig_2.show()


    #mode = markers removes the connecting lines 
    fig_sub_1 = make_subplots(rows=2, cols=3, subplot_titles=("Identity and Potency (%CAR+ Cells)", "Purity (%CD3+ Cells)", "Safety (VCN)", "Strength (%Viable Cells)", "Strength (Dose)"))
    colors = ['blue', 'red', 'green', 'orange', 'purple']
    colors_bub = ['black', 'black']
    colors_add = ['red'] * (len(col_names) - 2)
    colors_bub += colors_add
    fig_sub_1.append_trace(go.Scatter(x=col_names, y=multiplied_list, mode="markers", marker_color=colors_bub, showlegend=False), row=1, col=1)
    fig_sub_1.append_trace(go.Scatter(x=col_names, y=[y_mean] * len(col_names), mode='lines', name='Mean', marker_color=colors[0]), row=1, col=1)
    fig_sub_1.append_trace(go.Scatter(x=col_names, y=[two_plussd] * len(col_names), mode='lines', name='+2SD', marker_color=colors[1]), row=1, col=1)
    fig_sub_1.append_trace(go.Scatter(x=col_names, y=[two_minussd] * len(col_names), mode='lines', name='-2SD', marker_color=colors[2]), row=1, col=1)

    fig_sub_1.append_trace(go.Scatter(x=col_names, y=purity_, mode="markers", marker_color=colors_bub, showlegend=False), row=1, col=2)
    fig_sub_1.append_trace(go.Scatter(x=col_names, y=[y_mean_purity] * len(col_names), mode='lines', name='Mean', marker_color=colors[0], showlegend=False), row=1, col=2)
    fig_sub_1.append_trace(go.Scatter(x=col_names, y=[two_plussd_p] * len(col_names), mode='lines', name='+2SD', marker_color=colors[1], showlegend=False), row=1, col=2)
    fig_sub_1.append_trace(go.Scatter(x=col_names, y=[two_minussd_p] * len(col_names), mode='lines', name='-2SD', marker_color=colors[2], showlegend=False), row=1, col=2)

    fig_sub_1.append_trace(go.Scatter(x=col_names, y=vcn_, mode="markers", marker_color=colors_bub, showlegend=False), row=1, col=3)
    fig_sub_1.append_trace(go.Scatter(x=col_names, y=[y_mean_vcn] * len(col_names), mode='lines', name='Mean', marker_color=colors[0], showlegend=False), row=1, col=3)
    fig_sub_1.append_trace(go.Scatter(x=col_names, y=[two_plussd_vcn] * len(col_names), mode='lines', name='+2SD', marker_color=colors[1], showlegend=False), row=1, col=3)
    fig_sub_1.append_trace(go.Scatter(x=col_names, y=[two_minussd_vcn] * len(col_names), mode='lines', name='-2SD', marker_color=colors[2], showlegend=False), row=1, col=3)

    fig_sub_1.append_trace(go.Scatter(x=col_names, y=via_, mode="markers", marker_color=colors_bub, showlegend=False), row=2, col=1)
    fig_sub_1.append_trace(go.Scatter(x=col_names, y=[y_mean_via] * len(col_names), mode='lines', name='Mean', marker_color=colors[0], showlegend=False), row=2, col=1)
    fig_sub_1.append_trace(go.Scatter(x=col_names, y=[two_plussd_via] * len(col_names), mode='lines', name='+2SD', marker_color=colors[1], showlegend=False), row=2, col=1)
    fig_sub_1.append_trace(go.Scatter(x=col_names, y=[two_minussd_via] * len(col_names), mode='lines', name='-2SD', marker_color=colors[2], showlegend=False), row=2, col=1)

    fig_sub_1.append_trace(go.Scatter(x=col_names, y=dose, mode="markers", marker_color=colors_bub, showlegend=False), row=2, col=2)
    #fig_sub_1.append_trace(go.Scatter(x=col_names, y=[y_mean_dose] * len(col_names), mode='lines', name='Mean', marker_color=colors[0], showlegend=False), row=2, col=2)
    #fig_sub_1.append_trace(go.Scatter(x=col_names, y=[two_plussd_dose] * len(col_names), mode='lines', name='+2SD', marker_color=colors[1], showlegend=False), row=2, col=2)
    #fig_sub_1.append_trace(go.Scatter(x=col_names, y=[two_minussd_dose] * len(col_names), mode='lines', name='-2SD', marker_color=colors[2], showlegend=False), row=2, col=2)

    #for i in range(len(col_names)):
    #    list_ = [multiplied_list_2[i], multiplied_list[i]]
    #    fig_sub_1.append_trace(go.Scatter(x=x_axis, y=list_, name=col_names[i]), row=2, col=3)

    fig_sub_1.update_yaxes(title_text="%CAR+ Cells", range=[0, 100], row=1, col=1)
    fig_sub_1.update_yaxes(title_text="%CD3+ Cells", range=[75, 100] , row=1, col=2)
    fig_sub_1.update_yaxes(title_text="VCN", range=[0, 5], row=1, col=3)
    fig_sub_1.update_yaxes(title_text="Viable Cells (%)", range=[70, 100], row=2, col=1)
    fig_sub_1.update_yaxes(title_text="Actual Dose", range=[0, 1.5 * 10**8] , row=2, col=2)



    fig_sub_1.update_traces(marker_size=10)
    fig_sub_1.update_layout(title={'text': "Release Data", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
    #fig_sub_1.show()


    process = dfs["Run trend summary"]
    viability_aph = (process.loc[6, :].values.tolist())[3:]
    viability_aph = list(map(lambda x: x * 100, viability_aph))
    fold_expansion = (process.loc[51, :].values.tolist())[3:]
    fig_sub_process_1 = make_subplots(rows=2, cols=2, subplot_titles=("Cell Growth Over Process", "Cell Viability Over Process", "Apheresis %Viable Cells", "Fold Expansion Over Process"))
    fig_sub_process_1.add_trace(go.Bar(name='', x=col_names, y=viability_aph, marker_color=colors_bub, showlegend=False), row=2, col=1)
    fig_sub_process_1.add_trace(go.Bar(name='', x=col_names, y=fold_expansion,  marker_color=colors_bub, showlegend=False), row=2, col=2)
    fig_sub_process_1.update_layout(title={'text': "IP Data", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})

    cell_growth_0_r = (process.loc[24, :].values.tolist())[3:]
    cell_growth_6_r = (process.loc[29, :].values.tolist())[3:]
    cell_growth_7_r = (process.loc[34, :].values.tolist())[3:]
    cell_growth_8_r = (process.loc[39, :].values.tolist())[3:]
    cell_growth_9_r = (process.loc[45, :].values.tolist())[3:]

    x_axis = ["0", "6", "7", "8", "9"]
    for i in range(len(col_names)):
        list_ = [cell_growth_0_r[i], cell_growth_6_r[i], cell_growth_7_r[i], cell_growth_8_r[i], cell_growth_9_r[i]]
        fig_sub_process_1.add_trace(go.Scatter(x=x_axis, y=list_, name=col_names[i]), row = 1, col = 1)



    cell_via_0_aph = viability_aph
    cell_via_0_post = (process.loc[15, :].values.tolist())[3:]
    cell_via_0_post = list(map(lambda x: x * 100, cell_via_0_post))
    cell_growth_6 = (process.loc[27, :].values.tolist())[3:]
    cell_growth_6 = list(map(lambda x: x * 100, cell_growth_6))
    cell_growth_7 = (process.loc[32, :].values.tolist())[3:]
    cell_growth_7 = list(map(lambda x: x * 100, cell_growth_7))
    cell_growth_8 = (process.loc[37, :].values.tolist())[3:]
    cell_growth_8 = list(map(lambda x: x * 100, cell_growth_8))
    cell_growth_9_pre = (process.loc[43, :].values.tolist())[3:]
    cell_growth_9_pre = list(map(lambda x: x * 100, cell_growth_9_pre))
    cell_growth_9_post = (process.loc[48, :].values.tolist())[3:]
    cell_growth_9_post = list(map(lambda x: x * 100, cell_growth_9_post))
    cell_growth_fdp = (process.loc[70, :].values.tolist())[3:]
    cell_growth_fdp = list(map(lambda x: x * 100, cell_growth_fdp))

    x_axis = ["0 (Aph)", "0 (Post)", "6", "7", "8", "9 (Pre)", "9 (Post)", "FDP"]
    for i in range(len(col_names)):
        list_ = [cell_via_0_aph[i], cell_via_0_post[i], cell_growth_6[i], cell_growth_7[i], cell_growth_8[i], cell_growth_9_pre[i], cell_growth_9_post[i], cell_growth_fdp[i]]
        fig_sub_process_1.add_trace(go.Scatter(x=x_axis, y=list_, name=col_names[i]), row = 1, col = 2)

    #fig_sub_process_1.show()



    fig_sub_process_2 = make_subplots(rows=1, cols=2, subplot_titles=("Fold Expansion Over Process", "Cell Growth Over Process"))
    fig_sub_process_2.add_trace(go.Bar(name='', x=col_names, y=fold_expansion,  marker_color=colors_bub, showlegend=False), row=1, col=1)
    x_axis = ["0", "6", "7", "8", "9"]
    for i in range(len(col_names)):
        list_ = [cell_growth_0_r[i], cell_growth_6_r[i], cell_growth_7_r[i], cell_growth_8_r[i], cell_growth_9_r[i]]
        fig_sub_process_2.add_trace(go.Scatter(x=x_axis, y=list_, name=col_names[i]), row = 1, col = 2)

    fig_sub_process_2.update_layout(title={'text': "Process Performance", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})



    fig_sub_process_3 = make_subplots(rows=2, cols=2, subplot_titles=("Cell Viability over Process", "Cell Viability (Aph. - d6)", "Cell Viability (Pre- and Post-Harvest, FDP)"))
    x_axis = ["0 (Aph)", "0 (Post)", "6", "7", "8", "9 (Pre)", "9 (Post)", "FDP"]
    colors2 = ["yellow", "orange", "red", "green", "blue", "goldenrod", "magenta", "blue", "purple", "pink", "grey", ]
    for i in range(len(col_names)):
        list_ = [cell_via_0_aph[i], cell_via_0_post[i], cell_growth_6[i], cell_growth_7[i], cell_growth_8[i], cell_growth_9_pre[i], cell_growth_9_post[i], cell_growth_fdp[i]]
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

    #Graph for %CD4+ and %CD8+ Post Enrichment Stacked Bar Plot
    TBNK = dfs["TBNK"] 
    CD4 = (TBNK.loc[13, :].values.tolist())[3:]
    CD8 = (TBNK.loc[16, :].values.tolist())[3:]
    CD4_ = list(map(lambda x: x * 100 if not np.isnan(x) else x, CD4))
    CD8_ = list(map(lambda x: x * 100 if not np.isnan(x) else x, CD8))

    fig_3 = go.Figure(data=[
        go.Bar(name='CD4+', x=col_names, y=CD4_),
        go.Bar(name='CD8+', x=col_names, y=CD8_)
    ])
    # change bar mode
    fig_3.update_layout(barmode='stack', title={'text': "%CD4+ and %CD8+ Cells (Post Enrichment)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
    #fig_3.show()

    #Graph for %CD4+ and %CD8+ FDP Stacked Bar Plot
    CD4_FDP = (TBNK.loc[24, :].values.tolist())[3:]
    CD8_FDP = (TBNK.loc[27, :].values.tolist())[3:]
    CD4_FDP_ = list(map(lambda x: x * 100 if not np.isnan(x) else x, CD4_FDP))
    CD8_FDP_  = list(map(lambda x: x * 100 if not np.isnan(x) else x, CD8_FDP))


    fig_4 = go.Figure(data=[
        go.Bar(name='CD4+', x=col_names, y=CD4_FDP_),
        go.Bar(name='CD8+', x=col_names, y=CD8_FDP_)
    ])
    fig_4.update_layout(barmode='stack', title={'text': "%CD4+ and %CD8+ Cells (FDP)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
    #fig_4.show()


    fig_sub_2 = make_subplots(rows=1, cols=2, subplot_titles=("%CD4+ and %CD8+ Cells (Post Enrichment)", "%CD4+ and %CD8+ Cells (FDP)"))
    colors = ['blue', 'red', 'green', 'orange', 'purple']

    fig_sub_2.add_trace(go.Bar(name='CD4+', x=col_names, y=CD4_, marker_color=colors[0]), row=1, col=1)
    fig_sub_2.add_trace(go.Bar(name='CD8+', x=col_names, y=CD8_, marker_color=colors[1]), row=1, col=1)
    fig_sub_2.add_trace(go.Bar(name='', x=col_names, y=CD4_FDP_, marker_color=colors[0], showlegend=False), row=1, col=2)
    fig_sub_2.add_trace(go.Bar(name='', x=col_names, y=CD8_FDP_, marker_color=colors[1], showlegend=False), row=1, col=2)

    fig_sub_2.update_layout(barmode='stack', title={'text': "%CD4+ and %CD8+ Cells", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
    #fig_sub_2.show()








    #Graph for %CD4+ and %CD8+ FDP Stacked Bar Plot
    Bcells_Pre = list(map(lambda x: x * 100 if not np.isnan(x) else x,  (TBNK.loc[0, :].values.tolist())[3:]))
    CD4_Pre = list(map(lambda x: x * 100 if not np.isnan(x) else x, (TBNK.loc[2, :].values.tolist())[3:]))
    CD4CD8_Pre = list(map(lambda x: x * 100 if not np.isnan(x) else x, (TBNK.loc[3, :].values.tolist())[3:]))
    CD56CD16_Pre = list(map(lambda x: x * 100 if not np.isnan(x) else x, (TBNK.loc[4, :].values.tolist())[3:]))
    CD8_Pre = list(map(lambda x: x * 100 if not np.isnan(x) else x, (TBNK.loc[5, :].values.tolist())[3:]))
    Eosinophil_Pre = list(map(lambda x: x * 100 if not np.isnan(x) else x, (TBNK.loc[6, :].values.tolist())[3:]))
    Monocyte_Pre = list(map(lambda x: x * 100 if not np.isnan(x) else x, (TBNK.loc[7, :].values.tolist())[3:]))
    Neutrophil_Pre = list(map(lambda x: x * 100 if not np.isnan(x) else x, (TBNK.loc[8, :].values.tolist())[3:]))
    NKT_Pre = list(map(lambda x: x * 100 if not np.isnan(x) else x, (TBNK.loc[9, :].values.tolist())[3:]))
    Bcells_fdp = list(map(lambda x: x * 100 if not np.isnan(x) else x, (TBNK.loc[22, :].values.tolist())[3:]))
    CD4_fdp = list(map(lambda x: x * 100 if not np.isnan(x) else x, (TBNK.loc[24, :].values.tolist())[3:]))
    CD4CD8_fdp = list(map(lambda x: x * 100 if not np.isnan(x) else x, (TBNK.loc[25, :].values.tolist())[3:]))
    CD56CD16_fdp = list(map(lambda x: x * 100 if not np.isnan(x) else x, (TBNK.loc[26, :].values.tolist())[3:]))
    CD8_fdp = list(map(lambda x: x * 100 if not np.isnan(x) else x, (TBNK.loc[27, :].values.tolist())[3:]))
    Eosinophil_fdp = list(map(lambda x: x * 100 if not np.isnan(x) else x, (TBNK.loc[28, :].values.tolist())[3:]))
    Monocyte_fdp = list(map(lambda x: x * 100 if not np.isnan(x) else x, (TBNK.loc[29, :].values.tolist())[3:]))
    Neutrophil_fdp = list(map(lambda x: x * 100 if not np.isnan(x) else x, (TBNK.loc[30, :].values.tolist())[3:]))
    NKT_fdp = list(map(lambda x: x * 100 if not np.isnan(x) else x, (TBNK.loc[31, :].values.tolist())[3:]))

    CD4_Post = list(map(lambda x: x * 100 if not np.isnan(x) else x, (TBNK.loc[13, :].values.tolist())[3:]))
    CD8_Post = list(map(lambda x: x * 100 if not np.isnan(x) else x, (TBNK.loc[16, :].values.tolist())[3:]))

    B_cells = []
    for i in range(len(Bcells_Pre)):
        B_cells.append(Bcells_Pre[i])
        B_cells.append(Bcells_fdp[i])

    CD4 = []
    for i in range(len(CD4_Pre)):
        CD4.append(CD4_Pre[i])
        CD4.append(CD4_fdp[i])

    CD4CD8 = []
    for i in range(len(CD4CD8_Pre)):
        CD4CD8.append(CD4CD8_Pre[i])
        CD4CD8.append(CD4CD8_fdp[i])

    CD56CD16 = []
    for i in range(len(CD56CD16_Pre)):
        CD56CD16.append(CD56CD16_Pre[i])
        CD56CD16.append(CD56CD16_fdp[i])

    CD8 = []
    for i in range(len(CD8_Pre)):
        CD8.append(CD8_Pre[i])
        CD8.append(CD8_fdp[i])

    Eosinophil = []
    for i in range(len(Eosinophil_Pre)):
        Eosinophil.append(Eosinophil_Pre[i])
        Eosinophil.append(Eosinophil_fdp[i])

    Monocyte = []
    for i in range(len(Monocyte_Pre)):
        Monocyte.append(Monocyte_Pre[i])
        Monocyte.append(Monocyte_fdp[i])

    Neutrophil = []
    for i in range(len(Neutrophil_Pre)):
        Neutrophil.append(Neutrophil_Pre[i])
        Neutrophil.append(Neutrophil_fdp[i])

    NKT = []
    for i in range(len(NKT_Pre)):
        NKT.append(NKT_Pre[i])
        NKT.append(NKT_fdp[i])

    data = [B_cells, CD4, CD4CD8, CD56CD16, CD8, Eosinophil, Monocyte, Neutrophil, NKT]
    fig_tbnk = go.Figure()

    x_axis = list(chain.from_iterable(map(lambda x: [x, x], col_names)))
    my_list = ['Aph', 'FDP']
    result_list = my_list * len(col_names)

    x = [x_axis,result_list]
    names = ['B cells', 'CD4+', 'CD4+CD8+', 'CD56+CD16+', 'CD8+', 'Eosinophil', 'Monocyte', 'Neutrophil', 'NKT']
    for i in range(len(data)):
        fig_tbnk.add_bar(x=x,y=data[i],name=names[i])

    fig_tbnk.update_layout(barmode="relative", title={'text': "Leukocyte Purity (Apheresis and FDP)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
    #fig_tbnk.show()

    CD4_ = []
    for i in range(len(CD4_Pre)):
        CD4_.append(CD4_Pre[i])
        CD4_.append(CD4_Post[i])
        CD4_.append(CD4_fdp[i])

    CD8_ = []
    for i in range(len(CD8_Pre)):
        CD8_.append(CD8_Pre[i])
        CD8_.append(CD8_Post[i])
        CD8_.append(CD8_fdp[i])

    data = [CD4_, CD8_]
    fig_tbnk_2 = go.Figure()

    x_axis = list(chain.from_iterable(map(lambda x: [x, x, x], col_names)))
    my_list = ['Aph', 'Post', 'FDP']
    result_list = my_list * len(col_names)

    x = [x_axis,result_list]
    names = ['CD4+', 'CD8+']
    for i in range(len(data)):
        fig_tbnk_2.add_bar(x=x,y=data[i],name=names[i])

    fig_tbnk_2.update_layout(barmode="relative", title={'text': "%CD4+ and %CD8+ Cells (Aph., Post Enrichment, FDP)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
    #fig_tbnk_2.show()









































    #MemDiff CD8+ FDP
    MemDiff = dfs["Mem-Diff"]
    CD8_FDP_Tem = list(map(lambda x: x * 100 if not np.isnan(x) else x, (MemDiff.loc[17, :].values.tolist())[3:]))
    CD8_FDP_Temra = list(map(lambda x: x * 100 if not np.isnan(x) else x, (MemDiff.loc[18, :].values.tolist())[3:]))
    CD8_FDP_Tcm = list(map(lambda x: x * 100 if not np.isnan(x) else x,(MemDiff.loc[19, :].values.tolist())[3:]))
    CD8_FDP_Tscm = list(map(lambda x: x * 100 if not np.isnan(x) else x,(MemDiff.loc[20, :].values.tolist())[3:]))
    CD8_FDP_Tn = list(map(lambda x: x * 100 if not np.isnan(x) else x,(MemDiff.loc[21, :].values.tolist())[3:]))

    fig_5 = go.Figure(data=[
        go.Bar(name='Tem', x=col_names, y=CD8_FDP_Tem),
        go.Bar(name='Temra', x=col_names, y=CD8_FDP_Temra),
        go.Bar(name='Tcm', x=col_names, y=CD8_FDP_Tcm),
        go.Bar(name='Tscm', x=col_names, y=CD8_FDP_Tscm),
        go.Bar(name='Tn', x=col_names, y=CD8_FDP_Tn)
    ])
    fig_5.update_layout(barmode='stack', title={'text': "Memory Differentiation %CD8+ Cells (FDP)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
    #fig_5.show()

    #MemDiff CD4+ FDP
    CD4_FDP_Tem = list(map(lambda x: x * 100 if not np.isnan(x) else x,(MemDiff.loc[23, :].values.tolist())[3:]))
    CD4_FDP_Temra = list(map(lambda x: x * 100 if not np.isnan(x) else x,(MemDiff.loc[24, :].values.tolist())[3:]))
    CD4_FDP_Tcm = list(map(lambda x: x * 100 if not np.isnan(x) else x,(MemDiff.loc[25, :].values.tolist())[3:]))
    CD4_FDP_Tscm = list(map(lambda x: x * 100 if not np.isnan(x) else x,(MemDiff.loc[26, :].values.tolist())[3:]))
    CD4_FDP_Tn = list(map(lambda x: x * 100 if not np.isnan(x) else x,(MemDiff.loc[27, :].values.tolist())[3:]))

    fig_6 = go.Figure(data=[
        go.Bar(name='Tem', x=col_names, y=CD4_FDP_Tem),
        go.Bar(name='Temra', x=col_names, y=CD4_FDP_Temra),
        go.Bar(name='Tcm', x=col_names, y=CD4_FDP_Tcm),
        go.Bar(name='Tscm', x=col_names, y=CD4_FDP_Tscm),
        go.Bar(name='Tn', x=col_names, y=CD4_FDP_Tn)
    ])
    fig_6.update_layout(barmode='stack', title={'text': "Memory Differentiation %CD4+ Cells (FDP)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
    #fig_6.show()

    #MemDiff CD4+ Post Enrichment
    CD4_Post_Tem = list(map(lambda x: x * 100 if not np.isnan(x) else x,(MemDiff.loc[9, :].values.tolist())[3:]))
    CD4_Post_Temra = list(map(lambda x: x * 100 if not np.isnan(x) else x,(MemDiff.loc[10, :].values.tolist())[3:]))
    CD4_Post_Tcm = list(map(lambda x: x * 100 if not np.isnan(x) else x,(MemDiff.loc[11, :].values.tolist())[3:]))
    CD4_Post_Tscm = list(map(lambda x: x * 100 if not np.isnan(x) else x,(MemDiff.loc[12, :].values.tolist())[3:]))
    CD4_Post_Tn = list(map(lambda x: x * 100 if not np.isnan(x) else x,(MemDiff.loc[13, :].values.tolist())[3:]))

    fig_7 = go.Figure(data=[
        go.Bar(name='Tem', x=col_names, y=CD4_Post_Tem),
        go.Bar(name='Temra', x=col_names, y=CD4_Post_Temra),
        go.Bar(name='Tcm', x=col_names, y=CD4_Post_Tcm),
        go.Bar(name='Tscm', x=col_names, y=CD4_Post_Tscm),
        go.Bar(name='Tn', x=col_names, y=CD4_Post_Tn)
    ])
    fig_7.update_layout(barmode='stack', title={'text': "Memory Differentiation %CD4+ Cells (Post Enrichment)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
    #fig_7.show()

    #MemDiff CD8+ Post Enrichment
    CD8_Post_Tem = list(map(lambda x: x * 100 if not np.isnan(x) else x,(MemDiff.loc[3, :].values.tolist())[3:]))
    CD8_Post_Temra = list(map(lambda x: x * 100 if not np.isnan(x) else x,(MemDiff.loc[4, :].values.tolist())[3:]))
    CD8_Post_Tcm = list(map(lambda x: x * 100 if not np.isnan(x) else x,(MemDiff.loc[5, :].values.tolist())[3:]))
    CD8_Post_Tscm = list(map(lambda x: x * 100 if not np.isnan(x) else x,(MemDiff.loc[6, :].values.tolist())[3:]))
    CD8_Post_Tn = list(map(lambda x: x * 100 if not np.isnan(x) else x,(MemDiff.loc[7, :].values.tolist())[3:]))

    fig_8 = go.Figure(data=[
        go.Bar(name='Tem', x=col_names, y=CD8_Post_Tem),
        go.Bar(name='Temra', x=col_names, y=CD8_Post_Temra),
        go.Bar(name='Tcm', x=col_names, y=CD8_Post_Tcm),
        go.Bar(name='Tscm', x=col_names, y=CD8_Post_Tscm),
        go.Bar(name='Tn', x=col_names, y=CD8_Post_Tn)
    ])
    fig_8.update_layout(barmode='stack', title={'text': "Memory Differentiation %CD8+ Cells (Post Enrichment)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
    #fig_8.show()

    fig_9 = make_subplots(rows=2, cols=2, subplot_titles=("Memory Differentiation %CD8+ Cells (FDP)", "Memory Differentiation %CD4+ Cells (FDP)", "Memory Differentiation %CD8+ Cells (Post Enrichment)", "Memory Differentiation %CD4+ Cells (Post Enrichment)"))
    colors = ['blue', 'red', 'green', 'orange', 'purple']


    fig_9.add_trace(go.Bar(name='Tem', x=col_names, y=CD8_FDP_Tem, marker_color=colors[0]), row=1, col=1)
    fig_9.add_trace(go.Bar(name='Temra', x=col_names, y=CD8_FDP_Temra, marker_color=colors[1]), row=1, col=1)
    fig_9.add_trace(go.Bar(name='Tcm', x=col_names, y=CD8_FDP_Tcm, marker_color=colors[2]), row=1, col=1)
    fig_9.add_trace(go.Bar(name='Tcm', x=col_names, y=CD8_FDP_Tscm, marker_color=colors[3]), row=1, col=1)
    fig_9.add_trace(go.Bar(name='Tn', x=col_names, y=CD8_FDP_Tn, marker_color=colors[4]), row=1, col=1)


    fig_9.add_trace(go.Bar(name='', x=col_names, y=CD4_FDP_Tem, marker_color=colors[0], showlegend=False), row=1, col=2)
    fig_9.add_trace(go.Bar(name='', x=col_names, y=CD4_FDP_Temra, marker_color=colors[1], showlegend=False), row=1, col=2)
    fig_9.add_trace( go.Bar(name='', x=col_names, y=CD4_FDP_Tcm, marker_color=colors[2], showlegend=False), row=1, col=2)
    fig_9.add_trace(go.Bar(name='', x=col_names, y=CD4_FDP_Tscm, marker_color=colors[3], showlegend=False), row=1, col=2)
    fig_9.add_trace(go.Bar(name='', x=col_names, y=CD4_FDP_Tn, marker_color=colors[4], showlegend=False), row=1, col=2)

    fig_9.add_trace(go.Bar(name='', x=col_names, y=CD8_Post_Tem, marker_color=colors[0], showlegend=False), row=2, col=1)
    fig_9.add_trace(go.Bar(name='', x=col_names, y=CD8_Post_Temra, marker_color=colors[1], showlegend=False), row=2, col=1)
    fig_9.add_trace(go.Bar(name='', x=col_names, y=CD8_Post_Tcm, marker_color=colors[2], showlegend=False), row=2, col=1)
    fig_9.add_trace(go.Bar(name='', x=col_names, y=CD8_Post_Tscm, marker_color=colors[3], showlegend=False), row=2, col=1)
    fig_9.add_trace(go.Bar(name='', x=col_names, y=CD8_Post_Tn, marker_color=colors[4], showlegend=False), row=2, col=1)

    fig_9.add_trace(go.Bar(name='', x=col_names, y=CD4_Post_Tem, marker_color=colors[0], showlegend=False), row=2, col=2)
    fig_9.add_trace(go.Bar(name='', x=col_names, y=CD4_Post_Temra, marker_color=colors[1], showlegend=False), row=2, col=2)
    fig_9.add_trace(go.Bar(name='', x=col_names, y=CD4_Post_Tcm, marker_color=colors[2], showlegend=False), row=2, col=2)
    fig_9.add_trace(go.Bar(name='', x=col_names, y=CD4_Post_Tscm, marker_color=colors[3], showlegend=False), row=2, col=2)
    fig_9.add_trace(go.Bar(name='', x=col_names, y=CD4_Post_Tn, marker_color=colors[4], showlegend=False), row=2, col=2)



    # Update layout properties
    fig_9.update_layout(barmode='stack', title={'text': "Memory Differentiation", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
    #fig_9.show()




    fig_memdiff = make_subplots(rows=1, cols=2, subplot_titles=("%CD4+ Cells (Post-Enrichment & FDP)", "%CD8+ Cells (Post-Enrichment & FDP)"))

    x_axis = list(chain.from_iterable(map(lambda x: [x, x], col_names[2:])))
    my_list = ['Post', 'FDP']
    result_list = my_list * len(col_names[2:])

    Tem_CD4 = []
    for i in range(len(CD4_Post_Tem)):
        Tem_CD4.append(CD4_Post_Tem[i])
        Tem_CD4.append(CD4_FDP_Tem[i])

    Temra_CD4 = []
    for i in range(len(CD4_Post_Temra)):
        Temra_CD4.append(CD4_Post_Temra[i])
        Temra_CD4.append(CD4_FDP_Temra[i])

    Tcm_CD4 = []
    for i in range(len(CD4_Post_Tcm)):
        Tcm_CD4.append(CD4_Post_Tcm[i])
        Tcm_CD4.append(CD4_FDP_Tcm[i])

    Tscm_CD4 = []
    for i in range(len(CD4_Post_Tscm)):
        Tscm_CD4.append(CD4_Post_Tscm[i])
        Tscm_CD4.append(CD4_FDP_Tscm[i])

    Tn_CD4 = []
    for i in range(len(CD4_Post_Tn)):
        Tn_CD4.append(CD4_Post_Tn[i])
        Tn_CD4.append(CD4_FDP_Tn[i])

    Tem_CD8 = []
    for i in range(len(CD8_Post_Tem)):
        Tem_CD8.append(CD8_Post_Tem[i])
        Tem_CD8.append(CD8_FDP_Tem[i])

    Temra_CD8 = []
    for i in range(len(CD8_Post_Temra)):
        Temra_CD8.append(CD8_Post_Temra[i])
        Temra_CD8.append(CD8_FDP_Temra[i])

    Tcm_CD8 = []
    for i in range(len(CD8_Post_Tcm)):
        Tcm_CD8.append(CD8_Post_Tcm[i])
        Tcm_CD8.append(CD8_FDP_Tcm[i])

    Tscm_CD8 = []
    for i in range(len(CD8_Post_Tscm)):
        Tscm_CD8.append(CD8_Post_Tscm[i])
        Tscm_CD8.append(CD8_FDP_Tscm[i])

    Tn_CD8 = []
    for i in range(len(CD8_Post_Tn)):
        Tn_CD8.append(CD8_Post_Tn[i])
        Tn_CD8.append(CD8_FDP_Tn[i])

    x = [x_axis,result_list]
    names = ['Tem', 'Temra', 'Tcm', 'Tscm', 'Tn']

    data_CD4 = [Tem_CD4[4:], Temra_CD4[4:], Tcm_CD4[4:], Tscm_CD4[4:], Tn_CD4[4:]]
    data_CD8 = [Tem_CD8[4:], Temra_CD8[4:], Tcm_CD8[4:], Tscm_CD8[4:], Tn_CD8[4:]]

    colors = ['pink', 'purple', 'blue', 'violet', 'orange']
    for i in range(len(data_CD4)):
        fig_memdiff.add_trace(go.Bar(name=names[i], x=x, y=data_CD4[i], marker_color=colors[i]), row=1, col=1)
        fig_memdiff.add_trace(go.Bar(name='', x=x, y=data_CD8[i], marker_color=colors[i], showlegend=False), row=1, col=2)
    # fig_memdiff.add_bar(x=x,y=data_CD4[i],name=names[i], color=colors[2]), row=1, col=1)
    # fig_memdiff.add_bar(x=x,y=data_CD8[i],name="", showlegend=False, colors[i], row=1, col=2)

    fig_memdiff.update_layout(barmode="relative", title={'text': "Memory Differentiation (Post-Enrichment & FDP)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
    
    #, xaxis_tickangle=-45
    
    #fig_memdiff.show()



    cytokine = dfs["Cytokine"]
    CD19P_5_1 = (cytokine.loc[0, :].values.tolist())[1:]
    CD19P_10_1 = (cytokine.loc[1, :].values.tolist())[1:]
    CD19M_5_1 = (cytokine.loc[2, :].values.tolist())[1:]
    CD19M_10_1 = (cytokine.loc[3, :].values.tolist())[1:]

    cytotox = dfs["Cytotox"]
    one_to_one = list(map(lambda x: x * 100 if not np.isnan(x) else x, (cytotox.loc[0, :].values.tolist())[1:]))
    five_to_one = list(map(lambda x: x * 100 if not np.isnan(x) else x, (cytotox.loc[1, :].values.tolist())[1:]))
    ten_to_one = list(map(lambda x: x * 100 if not np.isnan(x) else x, (cytotox.loc[2, :].values.tolist())[1:]))

    cytotoxicity_data = [one_to_one, five_to_one, ten_to_one]
    cytokine_data = [CD19P_5_1, CD19P_10_1, CD19M_5_1, CD19M_10_1]

    cytotoxicity_names = ["1:1 (CD19+)", "5:1 (CD19+)", "10:1 (CD19+)"]
    cytokine_names = ["5:1 (CD19+)", "10:1 (CD19+)", "5:1 (CD19-)", "10:1 (CD19-)"]

    fig_cyto = make_subplots(rows=1, cols=2, subplot_titles=("IFNg Secretion (E:T Ratio)", "Cytotoxicity(E:T Ratio)"))

    for i in range(len(cytokine_data)):
        fig_cyto.add_trace(go.Bar(name=cytokine_names[i], x=col_names[1:], y=cytokine_data[i]), row=1, col=1)

    for i in range(len(cytotoxicity_data)):
        fig_cyto.add_trace(go.Bar(name=cytotoxicity_names[i], x=col_names[1:], y=cytotoxicity_data[i]), row=1, col=2)

    # Change the bar mode
    fig_cyto.update_layout(barmode='group', title={'text': "Characterization: Potency(IFNg and Cytotox)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
    #fig_cyto.show()

    df_1 = dfs["Data Date Tracking"]
    patient_names = df_1.columns[1:].tolist()
    release_assays = []
    char_assays = []
    for name in patient_names:
        new_1 = name + ' Release Assay'
        release_assays.append(new_1)
        new_2 = name + ' Characterization Assay'
        char_assays.append(new_2)
    titles = release_assays + char_assays
    col_count = len(df_1.columns) - 1
    y_1 = ['Mycoplasma', 'CAR Expression', 'Identity', 'Cell Count', 'Viability', 'Endotoxin', 'VCN', 'Appearance/Color', 'BacT', 'RCL', 'Sanger Sequence']
    y_2 = ['TBNK (DO Pre)', 'VCN', 'TBNK (D0 Post)', 'Mem/Diff (D0)', 'TBNK (D9)', 'Mem/Diff (D9)', 'Exhaustion', 'Cytotox', 'Cytokine']
    colors = ['blue', 'red', 'pink', 'purple']
    fig_date = make_subplots(rows=2, cols=col_count, subplot_titles=(titles))
    for i in range(len(patient_names)):
        col = df_1[patient_names[i]]
        start_method_1 = col[0:11]
        complete_method_1 = col[20:31]
        qa_review = col[40:51]
        receive_res_1 = col[51:62]
        start_method_2 = col[11:20]
        complete_method_2 = col[31:40]
        receive_res_2 = col[62:]
        if i == 0:
            fig_date.add_trace(go.Bar(y=y_1, x=start_method_1, name='TAT to Start Method', orientation='h', marker_color=colors[0]), row=1, col=(i+1))
            fig_date.add_trace(go.Bar(y=y_1, x=complete_method_1, name='TAT to Complete Method', orientation='h', marker_color=colors[1]), row=1, col=(i+1))
            fig_date.add_trace(go.Bar(y=y_1, x=qa_review, name='TAT For QA review', orientation='h', marker_color=colors[3]), row=1, col=(i+1))
            fig_date.add_trace(go.Bar(y=y_1, x=receive_res_1, name='TAT to Receive Results', orientation='h', marker_color=colors[2]), row=1, col=(i+1))
        else:
            fig_date.add_trace(go.Bar(y=y_1, x=start_method_1, name='TAT to Start Method', orientation='h', marker_color=colors[0], showlegend=False), row=1, col=(i+1))
            fig_date.add_trace(go.Bar(y=y_1, x=complete_method_1, name='TAT to Complete Method', orientation='h', marker_color=colors[1], showlegend=False), row=1, col=(i+1))
            fig_date.add_trace(go.Bar(y=y_1, x=qa_review, name='TAT For QA review', orientation='h', marker_color=colors[3], showlegend=False), row=1, col=(i+1))
            fig_date.add_trace(go.Bar(y=y_1, x=receive_res_1, name='TAT to Receive Results', orientation='h', marker_color=colors[2], showlegend=False), row=1, col=(i+1))
        fig_date.add_trace(go.Bar(y=y_2, x=start_method_2, name='TAT to Start Method', orientation='h', marker_color=colors[0], showlegend=False), row=2, col=(i+1))
        fig_date.add_trace(go.Bar(y=y_2, x=complete_method_2, name='TAT to Complete Method', orientation='h', marker_color=colors[1], showlegend=False), row=2, col=(i+1))
        fig_date.add_trace(go.Bar(y=y_2, x=receive_res_2, name='TAT to Receive Results', orientation='h', marker_color=colors[2], showlegend=False), row=2, col=(i+1))
    fig_date.update_layout(barmode='stack', title={'text': "Data Date Tracking", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
    
    

    with open('p_graph.html', 'w') as f:
        f.write(fig_sub_1.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_sub_process_2.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_sub_process_3.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_2.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_tbnk.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_tbnk_2.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_sub_2.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_9.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_memdiff.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_cyto.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_date.to_html(full_html=False, include_plotlyjs='cdn'))

    uri = pathlib.Path('p_graph.html').absolute().as_uri()
    webbrowser.open(uri)
    return send_file('p_graph.html', as_attachment=True)



@app.route('/process-files', methods=['POST'])
def process_files():
    file1 = request.files['globalfile']
    file2 = request.files['patientfile']
    name = request.form['username']
    xls_patient = pd.ExcelFile(file2)
    df = pd.read_excel(xls_patient, "Characterization Data 2", header=[0,1]) 
    df.columns = ['.'.join(col).strip() for col in df.columns.values]
        
    TBNK_Day0_Pre = df.iloc[0:11, 1]
    TBNK_Day0_Post = df.iloc[0:11, 2]
    TBNK_Day9_Final = df.iloc[0:11, 3]
    TBNK_Day0_Pre = TBNK_Day0_Pre.to_list()
    TBNK_Day0_Post = TBNK_Day0_Post.to_list()
    TBNK_Day9_Final = TBNK_Day9_Final.to_list()
    TBNK_col = TBNK_Day0_Pre + TBNK_Day0_Post + TBNK_Day9_Final 

    MemDiff_Day0Post = (df.iloc[0:14, 5]).to_list()
    MemDiff_Day9Final = (df.iloc[0:14, 6]).to_list()
    MemDiff_col = MemDiff_Day0Post + MemDiff_Day9Final 

    exhaustion_day9 = (df.iloc[0:27, 8]).to_list()

    cytotox = (df.iloc[0:3, 10]).to_list()

    cytokine = (df.iloc[0:4, 12]).to_list()

    cell_count = (df.iloc[0:1, 14]).to_list() + (df.iloc[0:1, 15]).to_list() + (df.iloc[0:1, 16]).to_list() + (df.iloc[0:1, 17]).to_list() + (df.iloc[0:1, 18]).to_list() 

    excel_file = pd.ExcelFile(file1)
    dfs = {sheet_name: excel_file.parse(sheet_name) for sheet_name in excel_file.sheet_names}
        
    print(dfs)
    df_TBNK = dfs["TBNK"]
    df_TBNK[name] = TBNK_col 

    df_TBNK = dfs["Mem-Diff"]
    df_TBNK[name] = MemDiff_col 

    df_TBNK = dfs["Exhaustion"]
    df_TBNK[name] = exhaustion_day9 

    df_TBNK = dfs["Cytotox"]
    df_TBNK[name] = cytotox

    df_TBNK = dfs["Cytokine"]
    df_TBNK[name] = cytokine

    df_TBNK = dfs["Cell Growth plot"] 
    df_TBNK[name] = cell_count 

   # df_2 = pd.read_excel(xls_patient, "Date Tracking", header=[0,1]) 
  #  df_2.columns = ['.'.join(col).strip() for col in df_2.columns.values]
  #  print(df_2.columns)

    #df_1 = pd.read_excel(xls_patient, "Date Tracking", header=[0]) 
    # df.columns = ['.'.join(col).strip() for col in df.columns.values]
    #start = df_1["TAT to Start Method"].tolist()
   # complete = df_1["TAT to Complete Method"].tolist()
  #  qa = (df_1["TAT For QA review"].tolist())[0:11]
  #  results = df_1["TAT to Receive Results"].tolist()
  #  list = start + complete + qa + results
  #  df_2 = pd.read_excel(excel_file, "Data Date Tracking", header=[0]) 
   # df_2[name] = list
    
    output_file = "modified_global.xlsx"
    with pd.ExcelWriter(output_file) as writer:
        for sheet_name, df in dfs.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    return send_file(output_file, as_attachment=True)


@app.route('/datavis-subset', methods=['POST'])
def visualization_subset():
    input = request.files['fileInputsubset']
    patient_names = request.form['patientnames']
    xls = pd.ExcelFile(input)
    col_names = patient_names.split(',')
    # Read the Excel file into a dictionary of DataFrames
    dfs = {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names}
    # print(dfs)
    process = dfs["Run trend summary"]
    viability_aph = []
    fold_expansion = []
    cell_growth_0_r = []
    cell_growth_6_r = []
    cell_growth_7_r = []
    cell_growth_8_r = []
    cell_growth_9_r = []
    cell_via_0_post = []
    cell_growth_6 = []
    cell_growth_7 = []
    cell_growth_8 = []
    cell_growth_9_pre = []
    cell_growth_9_post = []
    cell_growth_fdp = []
    print(process.keys())
    for patient in col_names:
        column = process[patient]
        viability_aph.append(column[6])
        fold_expansion.append(column[51])
        cell_growth_0_r.append(column[24])
        cell_growth_6_r.append(column[29])
        cell_growth_7_r.append(column[34])
        cell_growth_8_r.append(column[39])
        cell_growth_9_r.append(column[45])
        cell_via_0_post.append(column[15])
        cell_growth_6.append(column[27])
        cell_growth_7.append(column[32])
        cell_growth_8.append(column[37])
        cell_growth_9_pre.append(column[43])
        cell_growth_9_post.append(column[48])
        cell_growth_fdp.append(column[70])
      #  print(column)
    
   # viability_aph = (process.loc[6, :].values.tolist())[3:]
    viability_aph = list(map(lambda x: x * 100, viability_aph))
  #  fold_expansion = (process.loc[51, :].values.tolist())[3:]
    fig_sub_process_1 = make_subplots(rows=2, cols=2, subplot_titles=("Cell Growth Over Process", "Cell Viability Over Process", "Apheresis %Viable Cells", "Fold Expansion Over Process"))
    fig_sub_process_1.add_trace(go.Bar(name='', x=col_names, y=viability_aph, showlegend=False), row=2, col=1)
    fig_sub_process_1.add_trace(go.Bar(name='', x=col_names, y=fold_expansion, showlegend=False), row=2, col=2)
    fig_sub_process_1.update_layout(title={'text': "IP Data", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})

    x_axis = ["0", "6", "7", "8", "9"]
    for i in range(len(col_names)):
        list_ = [cell_growth_0_r[i], cell_growth_6_r[i], cell_growth_7_r[i], cell_growth_8_r[i], cell_growth_9_r[i]]
        fig_sub_process_1.add_trace(go.Scatter(x=x_axis, y=list_, name=col_names[i]), row = 1, col = 1)



    cell_via_0_aph = viability_aph
    cell_via_0_post = list(map(lambda x: x * 100, cell_via_0_post))
    cell_growth_6 = list(map(lambda x: x * 100, cell_growth_6))
    cell_growth_7 = list(map(lambda x: x * 100, cell_growth_7))
    cell_growth_8 = list(map(lambda x: x * 100, cell_growth_8))
    cell_growth_9_pre = list(map(lambda x: x * 100, cell_growth_9_pre))
    cell_growth_9_post = list(map(lambda x: x * 100, cell_growth_9_post))
    cell_growth_fdp = list(map(lambda x: x * 100, cell_growth_fdp))

    x_axis = ["0 (Aph)", "0 (Post)", "6", "7", "8", "9 (Pre)", "9 (Post)", "FDP"]
    for i in range(len(col_names)):
        list_ = [cell_via_0_aph[i], cell_via_0_post[i], cell_growth_6[i], cell_growth_7[i], cell_growth_8[i], cell_growth_9_pre[i], cell_growth_9_post[i], cell_growth_fdp[i]]
        fig_sub_process_1.add_trace(go.Scatter(x=x_axis, y=list_, name=col_names[i]), row = 1, col = 2)

   # fig_sub_process_1.show()



    fig_sub_process_2 = make_subplots(rows=1, cols=2, subplot_titles=("Fold Expansion Over Process", "Cell Growth Over Process"))
    fig_sub_process_2.add_trace(go.Bar(name='', x=col_names, y=fold_expansion, showlegend=False), row=1, col=1)
    x_axis = ["0", "6", "7", "8", "9"]
    for i in range(len(col_names)):
        list_ = [cell_growth_0_r[i], cell_growth_6_r[i], cell_growth_7_r[i], cell_growth_8_r[i], cell_growth_9_r[i]]
        fig_sub_process_2.add_trace(go.Scatter(x=x_axis, y=list_, name=col_names[i]), row = 1, col = 2)

    fig_sub_process_2.update_layout(title={'text': "Process Performance", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
    # fig_sub_process_2.show()

    colors2 = ["yellow", "orange", "red", "green", "blue", "goldenrod", "magenta", "blue", "purple", "pink", "grey" ]
    fig_sub_process_3 = make_subplots(rows=2, cols=2, subplot_titles=("Cell Viability over Process", "Cell Viability (Aph. - d6)", "Cell Viability (Pre- and Post-Harvest, FDP)"))
    x_axis = ["0 (Aph)", "0 (Post)", "6", "7", "8", "9 (Pre)", "9 (Post)", "FDP"]
    for i in range(len(col_names)):
        list_ = [cell_via_0_aph[i], cell_via_0_post[i], cell_growth_6[i], cell_growth_7[i], cell_growth_8[i], cell_growth_9_pre[i], cell_growth_9_post[i], cell_growth_fdp[i]]
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


    # fig_sub_process_3.show()







    #Graph for %CD4+ and %CD8+ Post Enrichment Stacked Bar Plot
    TBNK = dfs["TBNK"] 
    CD4 = []
    CD8 = []
    CD4_FDP = []
    CD8_FDP = []
    Bcells_Pre = []
    CD4_Pre = []
    CD4CD8_Pre = []
    CD56CD16_Pre = []
    CD8_Pre = []
    Eosinophil_Pre = []
    Monocyte_Pre = []
    Neutrophil_Pre = []
    NKT_Pre = []
    Bcells_fdp = []
    CD4_fdp = []
    CD4CD8_fdp = []
    CD56CD16_fdp = []
    CD8_fdp = []
    Eosinophil_fdp = []
    Monocyte_fdp = []
    Neutrophil_fdp = []
    NKT_fdp = []
    CD4_Post = []
    CD8_Post = []


    for patient in col_names:
        column = TBNK[patient]
        CD4.append(column[13])
        CD8.append(column[16])
        CD4_FDP.append(column[24])
        CD8_FDP.append(column[27])
        Bcells_Pre.append(column[0] * 100)
        CD4_Pre.append(column[2] * 100)
        CD4CD8_Pre.append(column[3] * 100)
        CD56CD16_Pre.append(column[4] * 100)
        CD8_Pre.append(column[5] * 100)
        Eosinophil_Pre.append(column[6] * 100)
        Monocyte_Pre.append(column[7] * 100)
        Neutrophil_Pre.append(column[8] * 100)
        NKT_Pre.append(column[9] * 100)
        Bcells_fdp.append(column[22] * 100)
        CD4_fdp.append(column[24] * 100)
        CD4CD8_fdp.append(column[25] * 100)
        CD56CD16_fdp.append(column[26] * 100)
        CD8_fdp.append(column[27] * 100)
        Eosinophil_fdp.append(column[28] * 100)
        Monocyte_fdp.append(column[29] * 100)
        Neutrophil_fdp.append(column[30] * 100)
        NKT_fdp.append(column[31] * 100)
        CD4_Post.append(column[13] * 100)
        CD8_Post.append(column[16] * 100)


    CD4_ = list(map(lambda x: x * 100 if not np.isnan(x) else x, CD4))
    CD8_ = list(map(lambda x: x * 100 if not np.isnan(x) else x, CD8))

    fig_3 = go.Figure(data=[
        go.Bar(name='CD4+', x=col_names, y=CD4_),
        go.Bar(name='CD8+', x=col_names, y=CD8_)
    ])
    # change bar mode
    fig_3.update_layout(barmode='stack', title={'text': "%CD4+ and %CD8+ Cells (Post Enrichment)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
  #  fig_3.show()

    #Graph for %CD4+ and %CD8+ FDP Stacked Bar Plot
    CD4_FDP_ = list(map(lambda x: x * 100 if not np.isnan(x) else x, CD4_FDP))
    CD8_FDP_  = list(map(lambda x: x * 100 if not np.isnan(x) else x, CD8_FDP))


    fig_4 = go.Figure(data=[
        go.Bar(name='CD4+', x=col_names, y=CD4_FDP_),
        go.Bar(name='CD8+', x=col_names, y=CD8_FDP_)
    ])
    fig_4.update_layout(barmode='stack', title={'text': "%CD4+ and %CD8+ Cells (FDP)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
   # fig_4.show()


    fig_sub_2 = make_subplots(rows=1, cols=2, subplot_titles=("%CD4+ and %CD8+ Cells (Post Enrichment)", "%CD4+ and %CD8+ Cells (FDP)"))
    colors = ['blue', 'red', 'green', 'orange', 'purple']

    fig_sub_2.add_trace(go.Bar(name='CD4+', x=col_names, y=CD4_, marker_color=colors[0]), row=1, col=1)
    fig_sub_2.add_trace(go.Bar(name='CD8+', x=col_names, y=CD8_, marker_color=colors[1]), row=1, col=1)
    fig_sub_2.add_trace(go.Bar(name='', x=col_names, y=CD4_FDP_, marker_color=colors[0], showlegend=False), row=1, col=2)
    fig_sub_2.add_trace(go.Bar(name='', x=col_names, y=CD8_FDP_, marker_color=colors[1], showlegend=False), row=1, col=2)

    fig_sub_2.update_layout(barmode='stack', title={'text': "%CD4+ and %CD8+ Cells", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
   # fig_sub_2.show()








    #Graph for %CD4+ and %CD8+ FDP Stacked Bar Plot

    B_cells = []
    for i in range(len(Bcells_Pre)):
        B_cells.append(Bcells_Pre[i])
        B_cells.append(Bcells_fdp[i])

    CD4 = []
    for i in range(len(CD4_Pre)):
        CD4.append(CD4_Pre[i])
        CD4.append(CD4_fdp[i])

    CD4CD8 = []
    for i in range(len(CD4CD8_Pre)):
        CD4CD8.append(CD4CD8_Pre[i])
        CD4CD8.append(CD4CD8_fdp[i])

    CD56CD16 = []
    for i in range(len(CD56CD16_Pre)):
        CD56CD16.append(CD56CD16_Pre[i])
        CD56CD16.append(CD56CD16_fdp[i])

    CD8 = []
    for i in range(len(CD8_Pre)):
        CD8.append(CD8_Pre[i])
        CD8.append(CD8_fdp[i])

    Eosinophil = []
    for i in range(len(Eosinophil_Pre)):
        Eosinophil.append(Eosinophil_Pre[i])
        Eosinophil.append(Eosinophil_fdp[i])

    Monocyte = []
    for i in range(len(Monocyte_Pre)):
        Monocyte.append(Monocyte_Pre[i])
        Monocyte.append(Monocyte_fdp[i])

    Neutrophil = []
    for i in range(len(Neutrophil_Pre)):
        Neutrophil.append(Neutrophil_Pre[i])
        Neutrophil.append(Neutrophil_fdp[i])

    NKT = []
    for i in range(len(NKT_Pre)):
        NKT.append(NKT_Pre[i])
        NKT.append(NKT_fdp[i])

    data = [B_cells, CD4, CD4CD8, CD56CD16, CD8, Eosinophil, Monocyte, Neutrophil, NKT]
    fig_tbnk = go.Figure()

    x_axis = list(chain.from_iterable(map(lambda x: [x, x], col_names)))
    my_list = ['Aph', 'FDP']
    result_list = my_list * len(col_names)

    x = [x_axis,result_list]
    names = ['B cells', 'CD4+', 'CD4+CD8+', 'CD56+CD16+', 'CD8+', 'Eosinophil', 'Monocyte', 'Neutrophil', 'NKT']
    for i in range(len(data)):
        fig_tbnk.add_bar(x=x,y=data[i],name=names[i])

    fig_tbnk.update_layout(barmode="relative", title={'text': "Leukocyte Purity (Apheresis and FDP)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
  #  fig_tbnk.show()

    CD4_ = []
    for i in range(len(CD4_Pre)):
        CD4_.append(CD4_Pre[i])
        CD4_.append(CD4_Post[i])
        CD4_.append(CD4_fdp[i])

    CD8_ = []
    for i in range(len(CD8_Pre)):
        CD8_.append(CD8_Pre[i])
        CD8_.append(CD8_Post[i])
        CD8_.append(CD8_fdp[i])

    data = [CD4_, CD8_]
    fig_tbnk_2 = go.Figure()

    x_axis = list(chain.from_iterable(map(lambda x: [x, x, x], col_names)))
    my_list = ['Aph', 'Post', 'FDP']
    result_list = my_list * len(col_names)

    x = [x_axis,result_list]
    names = ['CD4+', 'CD8+']
    for i in range(len(data)):
        fig_tbnk_2.add_bar(x=x,y=data[i],name=names[i])

    fig_tbnk_2.update_layout(barmode="relative", title={'text': "%CD4+ and %CD8+ Cells (Aph., Post Enrichment, FDP)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
   # fig_tbnk_2.show()









































    #MemDiff CD8+ FDP
    MemDiff = dfs["Mem-Diff"]
    CD8_FDP_Tem = []
    CD8_FDP_Temra = []
    CD8_FDP_Tcm = []
    CD8_FDP_Tscm = []
    CD8_FDP_Tn = []
    CD4_FDP_Tem = []
    CD4_FDP_Temra = []
    CD4_FDP_Tcm = []
    CD4_FDP_Tscm = []
    CD4_FDP_Tn = []
    CD4_Post_Tem = []
    CD4_Post_Temra = []
    CD4_Post_Tcm = []
    CD4_Post_Tscm = []
    CD4_Post_Tn = []
    CD8_Post_Tem = []
    CD8_Post_Temra = []
    CD8_Post_Tcm = []
    CD8_Post_Tscm = []
    CD8_Post_Tn = []

    for patient in col_names:
        column = MemDiff[patient]
        CD8_FDP_Tem.append(column[17] * 100)
        CD8_FDP_Temra.append(column[18] * 100)
        CD8_FDP_Tcm.append(column[19] * 100)
        CD8_FDP_Tscm.append(column[20] * 100)
        CD8_FDP_Tn.append(column[21] * 100)
        CD4_FDP_Tem.append(column[23]* 100)
        CD4_FDP_Temra.append(column[24] * 100)
        CD4_FDP_Tcm.append(column[25] * 100)
        CD4_FDP_Tscm.append(column[26] * 100)
        CD4_FDP_Tn.append(column[27] * 100)
        CD4_Post_Tem.append(column[9] * 100)
        CD4_Post_Temra.append(column[10] * 100)
        CD4_Post_Tcm.append(column[11] * 100)
        CD4_Post_Tscm.append(column[12] * 100)
        CD4_Post_Tn.append(column[13] * 100)
            #MemDiff CD8+ Post Enrichment
        CD8_Post_Tem.append(column[3] * 100)
        CD8_Post_Temra.append(column[4] * 100)
        CD8_Post_Tcm.append(column[5] * 100)
        CD8_Post_Tscm.append(column[6] * 100)
        CD8_Post_Tn.append(column[7] * 100)


    fig_5 = go.Figure(data=[
        go.Bar(name='Tem', x=col_names, y=CD8_FDP_Tem),
        go.Bar(name='Temra', x=col_names, y=CD8_FDP_Temra),
        go.Bar(name='Tcm', x=col_names, y=CD8_FDP_Tcm),
        go.Bar(name='Tscm', x=col_names, y=CD8_FDP_Tscm),
        go.Bar(name='Tn', x=col_names, y=CD8_FDP_Tn)
    ])
    fig_5.update_layout(barmode='stack', title={'text': "Memory Differentiation %CD8+ Cells (FDP)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
  #  fig_5.show()

    #MemDiff CD4+ FDP


    fig_6 = go.Figure(data=[
        go.Bar(name='Tem', x=col_names, y=CD4_FDP_Tem),
        go.Bar(name='Temra', x=col_names, y=CD4_FDP_Temra),
        go.Bar(name='Tcm', x=col_names, y=CD4_FDP_Tcm),
        go.Bar(name='Tscm', x=col_names, y=CD4_FDP_Tscm),
        go.Bar(name='Tn', x=col_names, y=CD4_FDP_Tn)
    ])
    fig_6.update_layout(barmode='stack', title={'text': "Memory Differentiation %CD4+ Cells (FDP)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
 #   fig_6.show()

    #MemDiff CD4+ Post Enrichment


    fig_7 = go.Figure(data=[
        go.Bar(name='Tem', x=col_names, y=CD4_Post_Tem),
        go.Bar(name='Temra', x=col_names, y=CD4_Post_Temra),
        go.Bar(name='Tcm', x=col_names, y=CD4_Post_Tcm),
        go.Bar(name='Tscm', x=col_names, y=CD4_Post_Tscm),
        go.Bar(name='Tn', x=col_names, y=CD4_Post_Tn)
    ])
    fig_7.update_layout(barmode='stack', title={'text': "Memory Differentiation %CD4+ Cells (Post Enrichment)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
 #   fig_7.show()


    fig_8 = go.Figure(data=[
        go.Bar(name='Tem', x=col_names, y=CD8_Post_Tem),
        go.Bar(name='Temra', x=col_names, y=CD8_Post_Temra),
        go.Bar(name='Tcm', x=col_names, y=CD8_Post_Tcm),
        go.Bar(name='Tscm', x=col_names, y=CD8_Post_Tscm),
        go.Bar(name='Tn', x=col_names, y=CD8_Post_Tn)
    ])
    fig_8.update_layout(barmode='stack', title={'text': "Memory Differentiation %CD8+ Cells (Post Enrichment)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
   # fig_8.show()

    fig_9 = make_subplots(rows=2, cols=2, subplot_titles=("Memory Differentiation %CD8+ Cells (FDP)", "Memory Differentiation %CD4+ Cells (FDP)", "Memory Differentiation %CD8+ Cells (Post Enrichment)", "Memory Differentiation %CD4+ Cells (Post Enrichment)"))
    colors = ['blue', 'red', 'green', 'orange', 'purple']


    fig_9.add_trace(go.Bar(name='Tem', x=col_names, y=CD8_FDP_Tem, marker_color=colors[0]), row=1, col=1)
    fig_9.add_trace(go.Bar(name='Temra', x=col_names, y=CD8_FDP_Temra, marker_color=colors[1]), row=1, col=1)
    fig_9.add_trace(go.Bar(name='Tcm', x=col_names, y=CD8_FDP_Tcm, marker_color=colors[2]), row=1, col=1)
    fig_9.add_trace(go.Bar(name='Tcm', x=col_names, y=CD8_FDP_Tscm, marker_color=colors[3]), row=1, col=1)
    fig_9.add_trace(go.Bar(name='Tn', x=col_names, y=CD8_FDP_Tn, marker_color=colors[4]), row=1, col=1)


    fig_9.add_trace(go.Bar(name='', x=col_names, y=CD4_FDP_Tem, marker_color=colors[0], showlegend=False), row=1, col=2)
    fig_9.add_trace(go.Bar(name='', x=col_names, y=CD4_FDP_Temra, marker_color=colors[1], showlegend=False), row=1, col=2)
    fig_9.add_trace( go.Bar(name='', x=col_names, y=CD4_FDP_Tcm, marker_color=colors[2], showlegend=False), row=1, col=2)
    fig_9.add_trace(go.Bar(name='', x=col_names, y=CD4_FDP_Tscm, marker_color=colors[3], showlegend=False), row=1, col=2)
    fig_9.add_trace(go.Bar(name='', x=col_names, y=CD4_FDP_Tn, marker_color=colors[4], showlegend=False), row=1, col=2)

    fig_9.add_trace(go.Bar(name='', x=col_names, y=CD8_Post_Tem, marker_color=colors[0], showlegend=False), row=2, col=1)
    fig_9.add_trace(go.Bar(name='', x=col_names, y=CD8_Post_Temra, marker_color=colors[1], showlegend=False), row=2, col=1)
    fig_9.add_trace(go.Bar(name='', x=col_names, y=CD8_Post_Tcm, marker_color=colors[2], showlegend=False), row=2, col=1)
    fig_9.add_trace(go.Bar(name='', x=col_names, y=CD8_Post_Tscm, marker_color=colors[3], showlegend=False), row=2, col=1)
    fig_9.add_trace(go.Bar(name='', x=col_names, y=CD8_Post_Tn, marker_color=colors[4], showlegend=False), row=2, col=1)

    fig_9.add_trace(go.Bar(name='', x=col_names, y=CD4_Post_Tem, marker_color=colors[0], showlegend=False), row=2, col=2)
    fig_9.add_trace(go.Bar(name='', x=col_names, y=CD4_Post_Temra, marker_color=colors[1], showlegend=False), row=2, col=2)
    fig_9.add_trace(go.Bar(name='', x=col_names, y=CD4_Post_Tcm, marker_color=colors[2], showlegend=False), row=2, col=2)
    fig_9.add_trace(go.Bar(name='', x=col_names, y=CD4_Post_Tscm, marker_color=colors[3], showlegend=False), row=2, col=2)
    fig_9.add_trace(go.Bar(name='', x=col_names, y=CD4_Post_Tn, marker_color=colors[4], showlegend=False), row=2, col=2)



    # Update layout properties
    fig_9.update_layout(barmode='stack', title={'text': "Memory Differentiation", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
   # fig_9.show()




    fig_memdiff = make_subplots(rows=1, cols=2, subplot_titles=("%CD4+ Cells (Post-Enrichment & FDP)", "%CD8+ Cells (Post-Enrichment & FDP)"))

    x_axis = list(chain.from_iterable(map(lambda x: [x, x], col_names)))
    my_list = ['Post', 'FDP']
    result_list = my_list * len(col_names)

    Tem_CD4 = []
    for i in range(len(CD4_Post_Tem)):
        Tem_CD4.append(CD4_Post_Tem[i])
        Tem_CD4.append(CD4_FDP_Tem[i])

    Temra_CD4 = []
    for i in range(len(CD4_Post_Temra)):
        Temra_CD4.append(CD4_Post_Temra[i])
        Temra_CD4.append(CD4_FDP_Temra[i])

    Tcm_CD4 = []
    for i in range(len(CD4_Post_Tcm)):
        Tcm_CD4.append(CD4_Post_Tcm[i])
        Tcm_CD4.append(CD4_FDP_Tcm[i])

    Tscm_CD4 = []
    for i in range(len(CD4_Post_Tscm)):
        Tscm_CD4.append(CD4_Post_Tscm[i])
        Tscm_CD4.append(CD4_FDP_Tscm[i])

    Tn_CD4 = []
    for i in range(len(CD4_Post_Tn)):
        Tn_CD4.append(CD4_Post_Tn[i])
        Tn_CD4.append(CD4_FDP_Tn[i])

    Tem_CD8 = []
    for i in range(len(CD8_Post_Tem)):
        Tem_CD8.append(CD8_Post_Tem[i])
        Tem_CD8.append(CD8_FDP_Tem[i])

    Temra_CD8 = []
    for i in range(len(CD8_Post_Temra)):
        Temra_CD8.append(CD8_Post_Temra[i])
        Temra_CD8.append(CD8_FDP_Temra[i])

    Tcm_CD8 = []
    for i in range(len(CD8_Post_Tcm)):
        Tcm_CD8.append(CD8_Post_Tcm[i])
        Tcm_CD8.append(CD8_FDP_Tcm[i])

    Tscm_CD8 = []
    for i in range(len(CD8_Post_Tscm)):
        Tscm_CD8.append(CD8_Post_Tscm[i])
        Tscm_CD8.append(CD8_FDP_Tscm[i])

    Tn_CD8 = []
    for i in range(len(CD8_Post_Tn)):
        Tn_CD8.append(CD8_Post_Tn[i])
        Tn_CD8.append(CD8_FDP_Tn[i])

    x = [x_axis,result_list]
    names = ['Tem', 'Temra', 'Tcm', 'Tscm', 'Tn']

    data_CD4 = [Tem_CD4, Temra_CD4, Tcm_CD4, Tscm_CD4, Tn_CD4]
    data_CD8 = [Tem_CD8, Temra_CD8, Tcm_CD8, Tscm_CD8, Tn_CD8]

    colors = ['pink', 'purple', 'blue', 'violet', 'orange']
    for i in range(len(data_CD4)):
        fig_memdiff.add_trace(go.Bar(name=names[i], x=x, y=data_CD4[i], marker_color=colors[i]), row=1, col=1)
        fig_memdiff.add_trace(go.Bar(name='', x=x, y=data_CD8[i], marker_color=colors[i], showlegend=False), row=1, col=2)
    # fig_memdiff.add_bar(x=x,y=data_CD4[i],name=names[i], color=colors[2]), row=1, col=1)
    # fig_memdiff.add_bar(x=x,y=data_CD8[i],name="", showlegend=False, colors[i], row=1, col=2)

    fig_memdiff.update_layout(barmode="relative", title={'text': "Memory Differentiation (Post-Enrichment & FDP)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
    
    #, xaxis_tickangle=-45
    
  #  fig_memdiff.show()



    cytokine = dfs["Cytokine"]
    CD19P_5_1 = []
    CD19P_10_1 = []
    CD19M_5_1 = []
    CD19M_10_1 = []
    
    for patient in col_names:
        column =  cytokine[patient]
        CD19P_5_1.append(column[0])
        CD19P_10_1.append(column[1])
        CD19M_5_1.append(column[2])
        CD19M_10_1.append(column[3])

    cytotox = dfs["Cytotox"]
    one_to_one = []
    five_to_one = []
    ten_to_one = []

    for patient in col_names:
        column =  cytotox[patient]
        one_to_one.append(column[0] * 100)
        five_to_one.append(column[1] * 100)
        ten_to_one.append(column[2] * 100)

    cytotoxicity_data = [one_to_one, five_to_one, ten_to_one]
    cytokine_data = [CD19P_5_1, CD19P_10_1, CD19M_5_1, CD19M_10_1]

    cytotoxicity_names = ["1:1 (CD19+)", "5:1 (CD19+)", "10:1 (CD19+)"]
    cytokine_names = ["5:1 (CD19+)", "10:1 (CD19+)", "5:1 (CD19-)", "10:1 (CD19-)"]

    fig_cyto = make_subplots(rows=1, cols=2, subplot_titles=("IFNg Secretion (E:T Ratio)", "Cytotoxicity(E:T Ratio)"))

    for i in range(len(cytokine_data)):
        fig_cyto.add_trace(go.Bar(name=cytokine_names[i], x=col_names, y=cytokine_data[i]), row=1, col=1)

    for i in range(len(cytotoxicity_data)):
        fig_cyto.add_trace(go.Bar(name=cytotoxicity_names[i], x=col_names, y=cytotoxicity_data[i]), row=1, col=2)

    # Change the bar mode
    fig_cyto.update_layout(barmode='group', title={'text': "Characterization: Potency(IFNg and Cytotox)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
  #  fig_cyto.show()
   
    df_1 = dfs["Data Date Tracking"]
    patient_names = col_names
    release_assays = []
    char_assays = []
    for name in patient_names:
        new_1 = name + ' Release Assay'
        release_assays.append(new_1)
        new_2 = name + ' Characterization Assay'
        char_assays.append(new_2)
    titles = release_assays + char_assays
    col_count = len(patient_names) 
    y_1 = ['Mycoplasma', 'CAR Expression', 'Identity', 'Cell Count', 'Viability', 'Endotoxin', 'VCN', 'Appearance/Color', 'BacT', 'RCL', 'Sanger Sequence']
    y_2 = ['TBNK (DO Pre)', 'VCN', 'TBNK (D0 Post)', 'Mem/Diff (D0)', 'TBNK (D9)', 'Mem/Diff (D9)', 'Exhaustion', 'Cytotox', 'Cytokine']
    colors = ['blue', 'red', 'pink', 'purple']
    fig_date = make_subplots(rows=2, cols=col_count, subplot_titles=(titles))
    for i in range(len(patient_names)):
        col = df_1[patient_names[i]]
        start_method_1 = col[0:11]
        complete_method_1 = col[20:31]
        qa_review = col[40:51]
        receive_res_1 = col[51:62]
        start_method_2 = col[11:20]
        complete_method_2 = col[31:40]
        receive_res_2 = col[62:]
        if i == 0:
            fig_date.add_trace(go.Bar(y=y_1, x=start_method_1, name='TAT to Start Method', orientation='h', marker_color=colors[0]), row=1, col=(i+1))
            fig_date.add_trace(go.Bar(y=y_1, x=complete_method_1, name='TAT to Complete Method', orientation='h', marker_color=colors[1]), row=1, col=(i+1))
            fig_date.add_trace(go.Bar(y=y_1, x=qa_review, name='TAT For QA review', orientation='h', marker_color=colors[3]), row=1, col=(i+1))
            fig_date.add_trace(go.Bar(y=y_1, x=receive_res_1, name='TAT to Receive Results', orientation='h', marker_color=colors[2]), row=1, col=(i+1))
        else:
            fig_date.add_trace(go.Bar(y=y_1, x=start_method_1, name='TAT to Start Method', orientation='h', marker_color=colors[0], showlegend=False), row=1, col=(i+1))
            fig_date.add_trace(go.Bar(y=y_1, x=complete_method_1, name='TAT to Complete Method', orientation='h', marker_color=colors[1], showlegend=False), row=1, col=(i+1))
            fig_date.add_trace(go.Bar(y=y_1, x=qa_review, name='TAT For QA review', orientation='h', marker_color=colors[3], showlegend=False), row=1, col=(i+1))
            fig_date.add_trace(go.Bar(y=y_1, x=receive_res_1, name='TAT to Receive Results', orientation='h', marker_color=colors[2], showlegend=False), row=1, col=(i+1))
        fig_date.add_trace(go.Bar(y=y_2, x=start_method_2, name='TAT to Start Method', orientation='h', marker_color=colors[0], showlegend=False), row=2, col=(i+1))
        fig_date.add_trace(go.Bar(y=y_2, x=complete_method_2, name='TAT to Complete Method', orientation='h', marker_color=colors[1], showlegend=False), row=2, col=(i+1))
        fig_date.add_trace(go.Bar(y=y_2, x=receive_res_2, name='TAT to Receive Results', orientation='h', marker_color=colors[2], showlegend=False), row=2, col=(i+1))
    fig_date.update_layout(barmode='stack', title={'text': "Data Date Tracking", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
    
    





    with open('p_graph.html', 'w') as f:
        f.write(fig_sub_process_2.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_sub_process_3.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_tbnk.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_tbnk_2.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_sub_2.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_9.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_memdiff.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_cyto.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_date.to_html(full_html=False, include_plotlyjs='cdn'))

  # return send_file('p_graph.html', as_attachment=True)

    uri = pathlib.Path('p_graph.html').absolute().as_uri()
    webbrowser.open(uri)
    return send_file('p_graph.html', as_attachment=True)
   # html_file_path = pathlib.Path('p_graph.html')


if __name__ == "__main__":
    app.debug = True
    app.run()
