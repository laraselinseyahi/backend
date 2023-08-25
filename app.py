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

    data_frame = dfs["QC Release Results Summary"] 

    #GRAPH FOR %CAR+ FDP
    col_names = list(data_frame.columns.values.tolist())
    col_names = col_names[4:]

    names_1 = data_frame[data_frame['Batch #'] == 'Study (e.g. KYV-IH, KYV-001, KYV-003)'].values[0].tolist()[4:]
    names_2 = data_frame[data_frame['Batch #'] == 'Patient No. w/in Study'].values[0].tolist()[4:]

    names = []
    for i in range(len(names_1)):
        name_info = str(names_1[i]) + '-' + str(names_2[i])
        names.append(name_info)

    col_names = names
    
    # print(data_frame)
    #row 10 is %CAR of final DP = CAR Transduction 
    # print(data_frame['Measurement'])
    row_list = data_frame[data_frame['Unnamed: 1'] == 'CAR Transduction'].values[0].tolist()
    row_list = row_list[4:]

    #purity
    purity = data_frame.loc[data_frame['Unnamed: 1'] == 'CD3 Expression'].values[0].tolist()
    purity = purity[4:]

    #vcn
    vcn = data_frame.loc[data_frame['Unnamed: 1'] == 'VCN'].values[0].tolist()
    vcn = vcn[4:]

    #viability % viable cells
    via = (data_frame.loc[data_frame['Unnamed: 1'] == 'Viability'].values[0].tolist())[4:]

    #actual dose 
    dose = (data_frame.loc[data_frame['Unnamed: 1'] == 'Dose'].values[0].tolist())[4:]

    pt_dose = (data_frame.loc[data_frame['Unnamed: 1'] == '%Target Dose'].values[0].tolist())[4:]
    

    multiplied_list = row_list
    print(multiplied_list)
    y_mean = np.nanmean(multiplied_list)
    print(y_mean)
    std = np.nanstd(multiplied_list)
    print(std)
    two_plussd = y_mean + 2*std
    two_minussd = y_mean - 2*std

    fig = px.scatter(y=multiplied_list, x=col_names, range_y = [0,100], labels={'y':'%CAR+ Cells'}, title="Identity and Potency (%CAR+ Cells)")
    fig.add_trace(go.Scatter(x=col_names, y=[y_mean] * len(col_names), mode='lines', name='Mean'))
    fig.add_trace(go.Scatter(x=col_names, y=[two_plussd] * len(col_names), mode='lines', name='+2SD'))
    fig.add_trace(go.Scatter(x=col_names, y=[two_minussd] * len(col_names), mode='lines', name='-2SD'))
    fig.update_traces(marker_size=10)
    #fig.show()

    purity_ = purity
    y_mean_purity = np.nanmean(purity_)
    std_p = np.nanstd(purity_)
    two_plussd_p = y_mean_purity + 2*std_p
    two_minussd_p = y_mean_purity - 2*std_p

    vcn_ = vcn
    y_mean_vcn = np.nanmean(vcn_ )
    std_vcn = np.nanstd(vcn_ )
    two_plussd_vcn = y_mean_vcn + 2*std_vcn
    two_minussd_vcn = y_mean_vcn - 2*std_vcn


    via_ = via
    y_mean_via = np.nanmean(via_)
    std_via = np.nanstd(via_)
    two_plussd_via = y_mean_via + 2*std_via
    two_minussd_via = y_mean_via - 2*std_via

    y_mean_dose = np.nanmean(dose)
    std_dose = np.nanstd(dose)
    two_plussd_dose = y_mean_dose + 2*std_dose
    two_minussd_dose = y_mean_dose - 2*std_dose 

    y_mean_dosept = np.nanmean(pt_dose)
    std_dosept = np.nanstd(pt_dose)
    two_plussd_dosept = y_mean_dose + 2*std_dose
    two_minussd_dosept = y_mean_dose - 2*std_dose 


    #Graph for %CAR+ D8 and D9
    #row 5 is D8 CAR
    #day 8 car will now pull from the in process data page
    process = dfs['In Process Data Summary']

    row_list_2 = process.loc[process['Batch #'] == 'Harvest -1Day CAR%'].values[0].tolist()[1:]

    multiplied_list_2 = row_list_2

    fig_2 = go.Figure()
    x_axis = ["Day 8", "Day 9"]
    for i in range(len(col_names)):
        list_ = [multiplied_list_2[i], multiplied_list[i]]
        fig_2.add_trace(go.Scatter(x=x_axis, y=list_, name=col_names[i]))
    fig_2.update_layout(title={'text': "%CAR+ Cells (Day 8 and Day 9)",'font': {'size': 24,'color': 'blue'}, 'x': 0.5 })  # Set the title's x position to the center
    #fig_2.show()


    #mode = markers removes the connecting lines 
    fig_sub_1 = make_subplots(rows=2, cols=3, subplot_titles=("Identity and Potency (%CAR+ Cells)", "Purity (%CD3+ Cells)", "Safety (VCN)", "Strength (%Viable Cells)", "Strength (Dose)", "%Target Dose"))
    colors = ['blue', 'red', 'green', 'orange', 'purple']
    colors_bub = ['black', 'black']
    colors_add = ['red'] * (len(col_names) - 2)
    colors_bub += colors_add
    colors_bub = ['red'] * (len(col_names))
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

    fig_sub_1.append_trace(go.Bar(x=col_names, y=pt_dose, marker_color=colors_bub, showlegend=False), row=2, col=3)
    # fig_sub_1.append_trace(go.Bar(x=col_names, y=[y_mean_dosept] * len(col_names), mode='lines', name='Mean', marker_color=colors[0], showlegend=False), row=2, col=3)
    # fig_sub_1.append_trace(go.Bar(x=col_names, y=[two_plussd_dosept] * len(col_names), mode='lines', name='+2SD', marker_color=colors[1], showlegend=False), row=2, col=3)
    # fig_sub_1.append_trace(go.Bar(x=col_names, y=[two_minussd_dosept] * len(col_names), mode='lines', name='-2SD', marker_color=colors[2], showlegend=False), row=2, col=3)

    #for i in range(len(col_names)):
    #    list_ = [multiplied_list_2[i], multiplied_list[i]]
    #    fig_sub_1.append_trace(go.Scatter(x=x_axis, y=list_, name=col_names[i]), row=2, col=3)

    fig_sub_1.update_yaxes(title_text="%CAR+ Cells", range=[0, 100], row=1, col=1)
    fig_sub_1.update_yaxes(title_text="%CD3+ Cells", range=[75, 100] , row=1, col=2)
    fig_sub_1.update_yaxes(title_text="VCN", range=[0, 5], row=1, col=3)
    fig_sub_1.update_yaxes(title_text="Viable Cells (%)", range=[70, 100], row=2, col=1)
    fig_sub_1.update_yaxes(title_text="Actual Dose", range=[0, 1.5 * 10**8] , row=2, col=2)
    fig_sub_1.update_yaxes(title_text="Target Dose(%)", row=2, col=3)



    # fig_sub_1.update_traces(marker_size=10)
    fig_sub_1.update_layout(title={'text': "Release Data", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
    #fig_sub_1.show()


    viability_aph = (process.loc[process['Batch #'] == 'Diluted Apheresis Viability (%)']).values[0].tolist()[1:]
    viability_aph = viability_aph
    fold_expansion = (process.loc[process['Batch #'] == 'Pre Harvest Fold Expansion']).values[0].tolist()[1:]
    fig_sub_process_1 = make_subplots(rows=2, cols=2, subplot_titles=("Cell Growth Over Process", "Cell Viability Over Process", "Apheresis %Viable Cells", "Fold Expansion Over Process"))
    fig_sub_process_1.add_trace(go.Bar(name='', x=col_names, y=viability_aph, marker_color=colors_bub, showlegend=False), row=2, col=1)
    fig_sub_process_1.add_trace(go.Bar(name='', x=col_names, y=fold_expansion,  marker_color=colors_bub, showlegend=False), row=2, col=2)
    fig_sub_process_1.update_layout(title={'text': "IP Data", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})

    cell_growth_0_r = process.loc[process['Batch #'] == 'Actual Cell Number for Culture'].values[0].tolist()[1:]
    print(cell_growth_0_r)
    cell_growth_6_r = process.loc[process['Batch #'] == 'Day 6 Total viable cells'].values[0].tolist()[1:]
    print(cell_growth_6_r)
    cell_growth_7_r = process.loc[process['Batch #'] == 'Day 7 Total Viable cells'].values[0].tolist()[1:] #if NA skip
    print(cell_growth_7_r)
    cell_growth_8_r = process.loc[process['Batch #'] == 'Harvest -1Day Total Viable Cells'].values[0].tolist()[1:] # cell growth harvest -1
    cell_growth_9_r = process.loc[process['Batch #'] == 'Pre Harvest Total Viable Cells'].values[0].tolist()[1:] # cell growth harvest 
    print(cell_growth_8_r)
    print(cell_growth_9_r)
    x_axis = ["0", "6", "7", "H - 1", "H"]
    for i in range(len(col_names)):
        list_ = [cell_growth_0_r[i], cell_growth_6_r[i], cell_growth_7_r[i], cell_growth_8_r[i], cell_growth_9_r[i]]
        fig_sub_process_1.add_trace(go.Scatter(x=x_axis, y=list_, name=col_names[i]), row = 1, col = 1)



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
    print(cell_via_0_post)
    print(cell_growth_6)
    print(cell_growth_7)
    print(cell_growth_8)
    print(cell_growth_9_pre)
    print(cell_growth_9_post)

    x_axis = ["0 (Aph)", "0 (Post)", "6", "7", "8", "9 (Pre)", "9 (Post)", "FDP"]
    for i in range(len(col_names)):
        list_ = [cell_via_0_aph[i], cell_via_0_post[i], cell_growth_6[i]]
        if pd.isna(cell_growth_7[i]):
            list_.extend([cell_growth_8[i], cell_growth_9_pre[i], cell_growth_9_post[i], cell_growth_fdp[i]])
        else:
            list_.extend([cell_growth_7[i], cell_growth_8[i], cell_growth_9_pre[i], cell_growth_9_post[i], cell_growth_fdp[i]])

        fig_sub_process_1.add_trace(go.Scatter(x=x_axis, y=list_, name=col_names[i]), row = 1, col = 2)

    #fig_sub_process_1.show()



    fig_sub_process_2 = make_subplots(rows=1, cols=2, subplot_titles=("Fold Expansion Over Process", "Cell Growth Over Process"))
    fig_sub_process_2.add_trace(go.Bar(name='', x=col_names, y=fold_expansion, showlegend=False), row=1, col=1)
    x_axis = ["0", "6", "7", "8", "9"]
    for i in range(len(col_names)):
        print(cell_growth_7_r[i])
        list_ = [cell_growth_0_r[i], cell_growth_6_r[i]] 
        print('1')
        print(list_)
        if pd.isna(cell_growth_7[i]):
            list_.extend([cell_growth_8_r[i], cell_growth_9_r[i]])
        else:
            list_.extend([cell_growth_7_r[i], cell_growth_8_r[i], cell_growth_9_r[i]])
        print('lara test')
        print(list_)
        fig_sub_process_2.add_trace(go.Scatter(x=x_axis, y=list_, name=col_names[i]), row = 1, col = 2)

    fig_sub_process_2.update_layout(title={'text': "Process Performance", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})


    #process performance y rnge 50-100



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

    #Graph for %CD4+ and %CD8+ Post Enrichment Stacked Bar Plot
    TBNK = dfs["TBNK"] 
    CD4 = (TBNK.loc[TBNK['Batch #'] == 'Day 0 Post-Enrichment - CD4+ T cells'].values[0].tolist())[1:]
    CD8 = (TBNK.loc[TBNK['Batch #'] == 'Day 0 Post-Enrichment - CD8+ T cells'].values[0].tolist())[1:]
    CD4_ = CD4
    CD8_ = CD8

    fig_3 = go.Figure(data=[
        go.Bar(name='CD4+', x=col_names, y=CD4_),
        go.Bar(name='CD8+', x=col_names, y=CD8_)
    ])
    # change bar mode
    fig_3.update_layout(barmode='stack', title={'text': "%CD4+ and %CD8+ Cells (Post Enrichment)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
    #fig_3.show()

    #Graph for %CD4+ and %CD8+ FDP Stacked Bar Plot
    CD4_FDP = (TBNK.loc[TBNK['Batch #'] == 'Final Product - CD4+ T cells'].values[0].tolist())[1:] 
    CD8_FDP = (TBNK.loc[TBNK['Batch #'] == 'Final Product - CD8+ T cells'].values[0].tolist())[1:] 
    CD4_FDP_ = CD4_FDP
    CD8_FDP_  = CD8_FDP


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
    Bcells_Pre = (TBNK.loc[TBNK['Batch #'] == 'Day 0 Pre-Enrichment - B cells']).values[0][1:] # 0
    CD4_Pre = (TBNK.loc[TBNK['Batch #'] == 'Day 0 Pre-Enrichment - CD4+ T cells']).values[0][1:] # 2
    CD4CD8_Pre = (TBNK.loc[TBNK['Batch #'] == 'Day 0 Pre-Enrichment - CD4+ CD8+ T cells']).values[0][1:] # 3
    CD56CD16_Pre = (TBNK.loc[TBNK['Batch #'] == 'Day 0 Pre-Enrichment - CD56+ CD16+ T cells']).values[0][1:] # 4 
    CD8_Pre = (TBNK.loc[TBNK['Batch #'] == 'Day 0 Pre-Enrichment - CD8+ T cells']).values[0][1:] # 5
    Eosinophil_Pre = (TBNK.loc[TBNK['Batch #'] == 'Day 0 Pre-Enrichment - Eosinophils']).values[0][1:] # 6
    Monocyte_Pre = (TBNK.loc[TBNK['Batch #'] == 'Day 0 Pre-Enrichment - Monocytes']).values[0][1:] # 7
    Neutrophil_Pre = (TBNK.loc[TBNK['Batch #'] == 'Day 0 Pre-Enrichment - Neutrophils']).values[0][1:] # 8
    NKT_Pre = (TBNK.loc[TBNK['Batch #'] == 'Day 0 Pre-Enrichment - NKT cells']).values[0][1:] # 9
    T_Pre = (TBNK.loc[TBNK['Batch #'] == 'Day 0 Pre-Enrichment - T cells']).values[0][1:] # 31
    Bcells_fdp = (TBNK.loc[TBNK['Batch #'] == 'Final Product - B cells']).values[0][1:] # 22
    CD4_fdp = (TBNK.loc[TBNK['Batch #'] == 'Final Product - CD4+ T cells']).values[0][1:] # 24
    CD4CD8_fdp = (TBNK.loc[TBNK['Batch #'] == 'Final Product - CD4+ CD8+ T cells']).values[0][1:] # 25
    CD56CD16_fdp = (TBNK.loc[TBNK['Batch #'] == 'Final Product - CD56+ CD16+ T cells']).values[0][1:] # 26
    CD8_fdp = (TBNK.loc[TBNK['Batch #'] == 'Final Product - CD8+ T cells']).values[0][1:] # 27
    Eosinophil_fdp = (TBNK.loc[TBNK['Batch #'] == 'Final Product - Eosinophils']).values[0][1:] # 28
    Monocyte_fdp = (TBNK.loc[TBNK['Batch #'] == 'Final Product - Monocytes']).values[0][1:] # 29
    Neutrophil_fdp = (TBNK.loc[TBNK['Batch #'] == 'Final Product - Neutrophils']).values[0][1:] # 30
    NKT_fdp = (TBNK.loc[TBNK['Batch #'] == 'Final Product - NKT cells']).values[0][1:] # 31
    T_fdp = (TBNK.loc[TBNK['Batch #'] == 'Final Product - T cells']).values[0][1:] # 31

    CD4_Post = (TBNK.loc[TBNK['Batch #'] == 'Day 0 Post-Enrichment - CD4+ T cells']).values[0][1:] # 13
    CD8_Post = (TBNK.loc[TBNK['Batch #'] == 'Day 0 Post-Enrichment - CD8+ T cells']).values[0][1:] # 16

    Bcells_Post = (TBNK.loc[TBNK['Batch #'] == 'Day 0 Post-Enrichment - B cells']).values[0][1:] # 0
    CD4_Post = (TBNK.loc[TBNK['Batch #'] == 'Day 0 Post-Enrichment - CD4+ T cells']).values[0][1:] # 2
    CD4CD8_Post = (TBNK.loc[TBNK['Batch #'] == 'Day 0 Post-Enrichment - CD4+ CD8+ T cells']).values[0][1:] # 3
    CD56CD16_Post = (TBNK.loc[TBNK['Batch #'] == 'Day 0 Post-Enrichment - CD56+ CD16+ T cells']).values[0][1:] # 4 
    CD8_Post = (TBNK.loc[TBNK['Batch #'] == 'Day 0 Post-Enrichment - CD8+ T cells']).values[0][1:] # 5
    Eosinophil_Post = (TBNK.loc[TBNK['Batch #'] == 'Day 0 Post-Enrichment - Eosinophils']).values[0][1:] # 6
    Monocyte_Post = (TBNK.loc[TBNK['Batch #'] == 'Day 0 Post-Enrichment - Monocytes']).values[0][1:] # 7
    Neutrophil_Post = (TBNK.loc[TBNK['Batch #'] == 'Day 0 Post-Enrichment - Neutrophils']).values[0][1:] # 8
    NKT_Post = (TBNK.loc[TBNK['Batch #'] == 'Day 0 Post-Enrichment - NKT cells']).values[0][1:] # 9
    T_Post = (TBNK.loc[TBNK['Batch #'] == 'Day 0 Post-Enrichment - T cells']).values[0][1:] # 9



    tbnk_swarm1 = make_subplots(rows=1, cols=3, subplot_titles=("Pre", "Post", "FDP" ))

    tbnk_swarm1.add_trace(go.Box(y=Bcells_Pre, name="B cells", showlegend=False), row=1, col=1)
    tbnk_swarm1.add_trace(go.Box(y=CD56CD16_Pre, name="CD56CD16", showlegend=False), row=1, col=1)
    tbnk_swarm1.add_trace(go.Box(y=Eosinophil_Pre, name="Eosinophil", showlegend=False), row=1, col=1)
    tbnk_swarm1.add_trace(go.Box(y=Monocyte_Pre, name="Monocyte", showlegend=False), row=1, col=1)
    tbnk_swarm1.add_trace(go.Box(y=Neutrophil_Pre, name="Neutrophil", showlegend=False), row=1, col=1)
    tbnk_swarm1.add_trace(go.Box(y=NKT_Pre, name="NKT", showlegend=False), row=1, col=1)
    tbnk_swarm1.add_trace(go.Box(y=T_Pre, name="T cells", showlegend=False), row=1, col=1)

    tbnk_swarm1.add_trace(go.Box(y=Bcells_Post, name="B cells", showlegend=False), row=1, col=2)
    tbnk_swarm1.add_trace(go.Box(y=CD56CD16_Post, name="CD56CD16", showlegend=False), row=1, col=2)
    tbnk_swarm1.add_trace(go.Box(y=Eosinophil_Post, name="Eosinophil", showlegend=False), row=1, col=2)
    tbnk_swarm1.add_trace(go.Box(y=Monocyte_Post, name="Monocyte", showlegend=False), row=1, col=2)
    tbnk_swarm1.add_trace(go.Box(y=Neutrophil_Post, name="Neutrophil", showlegend=False), row=1, col=2)
    tbnk_swarm1.add_trace(go.Box(y=NKT_Post, name="NKT", showlegend=False), row=1, col=2)
    tbnk_swarm1.add_trace(go.Box(y=T_Post, name="T cells", showlegend=False), row=1, col=2)

    tbnk_swarm1.add_trace(go.Box(y=Bcells_fdp, name="B cells", showlegend=False), row=1, col=3)
    tbnk_swarm1.add_trace(go.Box(y=CD56CD16_fdp, name="CD56CD16", showlegend=False), row=1, col=3)
    tbnk_swarm1.add_trace(go.Box(y=Eosinophil_fdp, name="Eosinophil", showlegend=False), row=1, col=3)
    tbnk_swarm1.add_trace(go.Box(y=Monocyte_fdp, name="Monocyte", showlegend=False), row=1, col=3)
    tbnk_swarm1.add_trace(go.Box(y=Neutrophil_fdp, name="Neutrophil", showlegend=False), row=1, col=3)
    tbnk_swarm1.add_trace(go.Box(y=NKT_fdp, name="NKT", showlegend=False), row=1, col=3)
    tbnk_swarm1.add_trace(go.Box(y=T_fdp, name="T cells", showlegend=False), row=1, col=3)



    tbnk_swarm1.update_yaxes(range=[-5, 100] , row=1, col=1)
    tbnk_swarm1.update_yaxes(range=[-5, 100] , row=1, col=2)
    tbnk_swarm1.update_yaxes(range=[-5, 100] , row=1, col=3)

    tbnk_swarm1.update_traces(boxpoints='all', jitter=0.5)
    tbnk_swarm1.show()


    tbnk_swarm2 = make_subplots(rows=3, cols=2, subplot_titles=("B Cells", "CD56CD16", "Monocyte", "NKT", "T cells"))

    tbnk_swarm2.add_trace(go.Box(y=Bcells_Pre, name="Pre", showlegend=False), row=1, col=1)
    tbnk_swarm2.add_trace(go.Box(y=Bcells_Post, name="Post", showlegend=False), row=1, col=1)
    tbnk_swarm2.add_trace(go.Box(y=Bcells_fdp, name="FDP", showlegend=False), row=1, col=1)

    tbnk_swarm2.add_trace(go.Box(y=CD56CD16_Pre, name="Pre", showlegend=False), row=1, col=2)
    tbnk_swarm2.add_trace(go.Box(y=CD56CD16_Post, name="Post", showlegend=False), row=1, col=2)
    tbnk_swarm2.add_trace(go.Box(y=CD56CD16_fdp, name="FDP", showlegend=False), row=1, col=2)

    tbnk_swarm2.add_trace(go.Box(y=Monocyte_Pre, name="Pre", showlegend=False), row=2, col=1)
    tbnk_swarm2.add_trace(go.Box(y=Monocyte_Post, name="Post", showlegend=False), row=2, col=1)
    tbnk_swarm2.add_trace(go.Box(y=Monocyte_fdp, name="FDP", showlegend=False), row=2, col=1)

    tbnk_swarm2.add_trace(go.Box(y=NKT_Pre, name="Pre", showlegend=False), row=2, col=2)
    tbnk_swarm2.add_trace(go.Box(y=NKT_Post, name="Post", showlegend=False), row=2, col=2)
    tbnk_swarm2.add_trace(go.Box(y=NKT_fdp, name="FDP", showlegend=False), row=2, col=2)

    tbnk_swarm2.add_trace(go.Box(y=T_Pre, name="Pre", showlegend=False), row=3, col=1)
    tbnk_swarm2.add_trace(go.Box(y=T_Post, name="Post", showlegend=False), row=3, col=1)
    tbnk_swarm2.add_trace(go.Box(y=T_fdp, name="FDP", showlegend=False), row=3, col=1)



    tbnk_swarm2.update_yaxes(range=[-5, 100] , row=1, col=1)
    tbnk_swarm2.update_yaxes(range=[-5, 100] , row=1, col=2)
    tbnk_swarm2.update_yaxes(range=[-5, 100] , row=2, col=1)
    tbnk_swarm2.update_yaxes(range=[-5, 100] , row=2, col=2)
    tbnk_swarm2.update_yaxes(range=[-5, 100] , row=3, col=1)

    tbnk_swarm2.update_traces(boxpoints='all', jitter=0.5)
    tbnk_swarm2.show()



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
    # BURDA KALDI
    MemDiff = dfs["Mem-Diff"]
    CD8_FDP_Tem = (MemDiff.loc[MemDiff['Batch #'] == 'Final Product - CD3+\CAR+\CD8+\Tem'].values[0][1:]) # 17
    CD8_FDP_Temra = (MemDiff.loc[MemDiff['Batch #'] == 'Final Product - CD3+\CAR+\CD8+\Temra'].values[0][1:]) # 18
    CD8_FDP_Tcm = (MemDiff.loc[MemDiff['Batch #'] == 'Final Product - CD3+\CAR+\CD8+\Tcm'].values[0][1:]) # 19
    CD8_FDP_Tscm = (MemDiff.loc[MemDiff['Batch #'] == 'Final Product - CD3+\CAR+\CD8+\Tscm'].values[0][1:]) # 20
    CD8_FDP_Tn = (MemDiff.loc[MemDiff['Batch #'] == 'Final Product - CD3+\CAR+\CD8+\Tn'].values[0][1:]) # 21


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
    CD4_FDP_Tem = (MemDiff.loc[MemDiff['Batch #'] == 'Final Product - CD3+\CAR+\CD4+\Tem'].values[0][1:])
    CD4_FDP_Temra = (MemDiff.loc[MemDiff['Batch #'] == 'Final Product - CD3+\CAR+\CD4+\Temra'].values[0][1:])
    CD4_FDP_Tcm = (MemDiff.loc[MemDiff['Batch #'] == 'Final Product - CD3+\CAR+\CD4+\Tcm'].values[0][1:])
    CD4_FDP_Tscm = (MemDiff.loc[MemDiff['Batch #'] == 'Final Product - CD3+\CAR+\CD4+\Tscm'].values[0][1:])
    CD4_FDP_Tn = (MemDiff.loc[MemDiff['Batch #'] == 'Final Product - CD3+\CAR+\CD4+\Tn'].values[0][1:])


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
    CD4_Post_Tem = (MemDiff.loc[MemDiff['Batch #'] == 'Day 0 Post-Enrichment - CD3+\CD4+\Tem'].values[0][1:])
    CD4_Post_Temra = (MemDiff.loc[MemDiff['Batch #'] == 'Day 0 Post-Enrichment - CD3+\CD4+\Temra'].values[0][1:])
    CD4_Post_Tcm = (MemDiff.loc[MemDiff['Batch #'] == 'Day 0 Post-Enrichment - CD3+\CD4+\Tcm'].values[0][1:])
    CD4_Post_Tscm = (MemDiff.loc[MemDiff['Batch #'] == 'Day 0 Post-Enrichment - CD3+\CD4+\Tscm'].values[0][1:])
    CD4_Post_Tn = (MemDiff.loc[MemDiff['Batch #'] == 'Day 0 Post-Enrichment - CD3+\CD4+\Tn'].values[0][1:])


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
    CD8_Post_Tem = (MemDiff.loc[MemDiff['Batch #'] == 'Day 0 Post-Enrichment - CD3+\CD8+\Tem'].values[0][1:])
    CD8_Post_Temra = (MemDiff.loc[MemDiff['Batch #'] == 'Day 0 Post-Enrichment - CD3+\CD8+\Temra'].values[0][1:])
    CD8_Post_Tcm = (MemDiff.loc[MemDiff['Batch #'] == 'Day 0 Post-Enrichment - CD3+\CD8+\Tcm'].values[0][1:])
    CD8_Post_Tscm = (MemDiff.loc[MemDiff['Batch #'] == 'Day 0 Post-Enrichment - CD3+\CD8+\Tscm'].values[0][1:])
    CD8_Post_Tn = (MemDiff.loc[MemDiff['Batch #'] == 'Day 0 Post-Enrichment - CD3+\CD8+\Tn'].values[0][1:])


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


    fig_memdiff_swarm1 = make_subplots(rows=2, cols=2, subplot_titles=("%CD4+ Post", "%CD4+ FDP", "%CD8+ Post", "%CD8+ FDP" ))


    fig_memdiff_swarm1.add_trace(go.Box(y=CD4_Post_Tn, name="Tn", showlegend=False), row=1, col=1)
    fig_memdiff_swarm1.add_trace(go.Box(y=CD4_Post_Tscm, name="Tscm", showlegend=False), row=1, col=1)
    fig_memdiff_swarm1.add_trace(go.Box(y=CD4_Post_Tcm, name="Tcm", showlegend=False), row=1, col=1)
    fig_memdiff_swarm1.add_trace(go.Box(y=CD4_Post_Tem, name="Tem", showlegend=False), row=1, col=1)
    fig_memdiff_swarm1.add_trace(go.Box(y=CD4_Post_Temra, name="Temra", showlegend=False), row=1, col=1)

    fig_memdiff_swarm1.add_trace(go.Box(y=CD4_FDP_Tn, name="Tn", showlegend=False), row=1, col=2)
    fig_memdiff_swarm1.add_trace(go.Box(y=CD4_FDP_Tscm, name="Tscm", showlegend=False), row=1, col=2)
    fig_memdiff_swarm1.add_trace(go.Box(y=CD4_FDP_Tcm, name="Tcm", showlegend=False), row=1, col=2)
    fig_memdiff_swarm1.add_trace(go.Box(y=CD4_FDP_Tem, name="Tem", showlegend=False), row=1, col=2)
    fig_memdiff_swarm1.add_trace(go.Box(y=CD4_FDP_Temra, name="Temra", showlegend=False), row=1, col=2)

    fig_memdiff_swarm1.add_trace(go.Box(y=CD8_Post_Tn, name="Tn", showlegend=False), row=2, col=1)
    fig_memdiff_swarm1.add_trace(go.Box(y=CD8_Post_Tscm, name="Tscm", showlegend=False), row=2, col=1)
    fig_memdiff_swarm1.add_trace(go.Box(y=CD8_Post_Tcm, name="Tcm", showlegend=False), row=2, col=1)
    fig_memdiff_swarm1.add_trace(go.Box(y=CD8_Post_Tem, name="Tem", showlegend=False), row=2, col=1)
    fig_memdiff_swarm1.add_trace(go.Box(y=CD8_Post_Temra, name="Temra", showlegend=False), row=2, col=1)

    fig_memdiff_swarm1.add_trace(go.Box(y=CD8_FDP_Tn, name="Tn", showlegend=False), row=2, col=2)
    fig_memdiff_swarm1.add_trace(go.Box(y=CD8_FDP_Tscm, name="Tscm", showlegend=False), row=2, col=2)
    fig_memdiff_swarm1.add_trace(go.Box(y=CD8_FDP_Tcm, name="Tcm", showlegend=False), row=2, col=2)
    fig_memdiff_swarm1.add_trace(go.Box(y=CD8_FDP_Tem, name="Tem", showlegend=False), row=2, col=2)
    fig_memdiff_swarm1.add_trace(go.Box(y=CD8_FDP_Temra, name="Temra", showlegend=False), row=2, col=2)

    fig_memdiff_swarm1.update_yaxes(range=[-5, 100] , row=1, col=1)
    fig_memdiff_swarm1.update_yaxes(range=[-5, 100] , row=1, col=2)
    fig_memdiff_swarm1.update_yaxes(range=[-5, 100] , row=2, col=1)
    fig_memdiff_swarm1.update_yaxes(range=[-5, 100] , row=2, col=2)

    fig_memdiff_swarm1.update_traces(boxpoints='all', jitter=0.5)
    fig_memdiff_swarm1.show()


    fig_memdiff_swarm2 = make_subplots(rows=3, cols=2, subplot_titles=("%CD4+ Tn", "%CD4+ Tscm", "%CD4+ Tcm", "%CD4+ Tem", "%CD4+ Temra"))
    fig_memdiff_swarm3 = make_subplots(rows=3, cols=2, subplot_titles=("%CD8+ Tn", "%CD8+ Tscm", "%CD8+ Tcm", "%CD8+ Tem", "%CD8+ Temra"))


    fig_memdiff_swarm2.add_trace(go.Box(y=CD4_Post_Tn, name="Post", showlegend=False), row=1, col=1)
    fig_memdiff_swarm2.add_trace(go.Box(y=CD4_FDP_Tn, name="FDP", showlegend=False), row=1, col=1)
    
    fig_memdiff_swarm3.add_trace(go.Box(y=CD8_Post_Tn, name="Post", showlegend=False), row=1, col=1)
    fig_memdiff_swarm3.add_trace(go.Box(y=CD8_FDP_Tn, name="FDP", showlegend=False), row=1, col=1)

    fig_memdiff_swarm2.add_trace(go.Box(y=CD4_Post_Tscm, name="Post", showlegend=False), row=1, col=2)
    fig_memdiff_swarm2.add_trace(go.Box(y=CD4_FDP_Tscm, name="FDP", showlegend=False), row=1, col=2)
    
    fig_memdiff_swarm3.add_trace(go.Box(y=CD8_Post_Tscm, name="Post", showlegend=False), row=1, col=2)
    fig_memdiff_swarm3.add_trace(go.Box(y=CD8_FDP_Tscm, name="FDP", showlegend=False), row=1, col=2)

    fig_memdiff_swarm2.add_trace(go.Box(y=CD4_Post_Tcm, name="Post", showlegend=False), row=2, col=1)
    fig_memdiff_swarm2.add_trace(go.Box(y=CD4_FDP_Tcm, name="FDP", showlegend=False), row=2, col=1)
    
    fig_memdiff_swarm3.add_trace(go.Box(y=CD8_Post_Tcm, name="Post", showlegend=False), row=2, col=1)
    fig_memdiff_swarm3.add_trace(go.Box(y=CD8_FDP_Tcm, name="FDP", showlegend=False), row=2, col=1)

    fig_memdiff_swarm2.add_trace(go.Box(y=CD4_Post_Tem, name="Post", showlegend=False), row=2, col=2)
    fig_memdiff_swarm2.add_trace(go.Box(y=CD4_FDP_Tem, name="FDP", showlegend=False), row=2, col=2)
    
    fig_memdiff_swarm3.add_trace(go.Box(y=CD8_Post_Tem, name="Post", showlegend=False), row=2, col=2)
    fig_memdiff_swarm3.add_trace(go.Box(y=CD8_FDP_Tem, name="FDP", showlegend=False), row=2, col=2)

    fig_memdiff_swarm2.add_trace(go.Box(y=CD4_Post_Temra, name="Post", showlegend=False), row=3, col=1)
    fig_memdiff_swarm2.add_trace(go.Box(y=CD4_FDP_Temra, name="FDP", showlegend=False), row=3, col=1)
    
    fig_memdiff_swarm3.add_trace(go.Box(y=CD8_Post_Temra, name="Post", showlegend=False), row=3, col=1)
    fig_memdiff_swarm3.add_trace(go.Box(y=CD8_FDP_Temra, name="FDP", showlegend=False), row=3, col=1)


    fig_memdiff_swarm2.update_yaxes(range=[-5, 100] , row=1, col=1)
    fig_memdiff_swarm2.update_yaxes(range=[-5, 100] , row=1, col=2)
    fig_memdiff_swarm2.update_yaxes(range=[-5, 100] , row=2, col=1)
    fig_memdiff_swarm2.update_yaxes(range=[-5, 100] , row=2, col=2)
    fig_memdiff_swarm2.update_yaxes(range=[-5, 100] , row=3, col=1)
    fig_memdiff_swarm3.update_yaxes(range=[-5, 100] , row=1, col=1)
    fig_memdiff_swarm3.update_yaxes(range=[-5, 100] , row=1, col=2)
    fig_memdiff_swarm3.update_yaxes(range=[-5, 100] , row=2, col=1)
    fig_memdiff_swarm3.update_yaxes(range=[-5, 100] , row=2, col=2)
    fig_memdiff_swarm3.update_yaxes(range=[-5, 100] , row=3, col=1)

    fig_memdiff_swarm2.update_traces(boxpoints='all', jitter=0.5)
    fig_memdiff_swarm2.show()

    fig_memdiff_swarm3.update_traces(boxpoints='all', jitter=0.5)
    fig_memdiff_swarm3.show()

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

# don't pass
    data_CD4 = [Tem_CD4, Temra_CD4, Tcm_CD4, Tscm_CD4, Tn_CD4]
    print(data_CD4)
    data_CD8 = [Tem_CD8, Temra_CD8, Tcm_CD8, Tscm_CD8, Tn_CD8]
    print(data_CD8)

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
    CD19P_5_1 = (cytokine.loc[cytokine['Batch #'] == 'IFNg 5:1 (CD19+) (pg/mL) E:T Ratio']).values[0].tolist()[1:] 
    CD19P_10_1 = (cytokine.loc[cytokine['Batch #'] == 'IFNg 10:1 (CD19+) (pg/mL) E:T Ratio']).values[0].tolist()[1:]
    CD19M_5_1 = (cytokine.loc[cytokine['Batch #'] == 'IFNg 5:1 (CD19-) (pg/mL) E:T Ratio']).values[0].tolist()[1:]
    CD19M_10_1 = (cytokine.loc[cytokine['Batch #'] == 'IFNg 10:1 (CD19-) (pg/mL) E:T Ratio']).values[0].tolist()[1:]

    cytotox = dfs["Cytotox"]
    one_to_one = (cytotox.loc[cytotox['Batch #'] == '1:1 (CD19+) E:T'].values[0][1:])
    five_to_one = (cytotox.loc[cytotox['Batch #'] == '5:1 (CD19+) E:T'].values[0][1:])
    ten_to_one = (cytotox.loc[cytotox['Batch #'] == '10:1 (CD19+) E:T'].values[0][1:])


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
    #fig_cyto.show()

    df_1 = dfs["Data Date Tracking"]
    patient_names = df_1.columns[1:].tolist()
    release_assays = []
    char_assays = []
    for name in patient_names:
        new_1 = name + ' Release'
        release_assays.append(new_1)
        new_2 = name + ' Char'
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
    
    l = ["Attribute", "Measurement", "Method", "Acceptance Criteria"]
    l.extend(col_names)
    df = data_frame
    # row_means = df.mean(axis=1)
    # Select only the numeric columns
    df_removed = df.iloc[:, 4:]
   # print(df_removed)
    # numeric_columns = df_removed.select_dtypes(include=['number', 'int', 'float'])

    # Calculate the mean of each row for numeric columns
    #row_means = numeric_columns.mean(axis=1)
    #print(row_means)
    # Add the row means as a new column to the DataFrame
    # df['RowMean'] = row_means
    # Select only the numeric columns
    #numeric_columns = df.select_dtypes(include=['number'])

    # Calculate the range of each row for numeric columns
    #row_ranges = np.ptp(numeric_columns.values, axis=1)

    # Add the row ranges as a new column to the DataFrame
    # df['RowRange'] = row_ranges

    #l_new = ["Mean", "Range"]
    #l.extend(l_new)
    fig = go.Figure()
    fig.add_trace(
    go.Table(
        header=dict(
            values=l,
            font=dict(size=10),
            align="left"
        ),
        cells=dict(
            values=[df[k].tolist()[4:] for k in df.columns],
            align = "left")
    )
    )
    

    with open('p_graph.html', 'w') as f:
        f.write(fig_sub_1.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_sub_process_2.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_sub_process_3.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_2.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_tbnk.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_tbnk_2.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(tbnk_swarm1.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(tbnk_swarm2.to_html(full_html=False, include_plotlyjs='cdn'))
       # f.write(fig_sub_2.to_html(full_html=False, include_plotlyjs='cdn'))
       # f.write(fig_9.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_memdiff.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_memdiff_swarm1.to_html(full_html=False, include_plotlyjs='cdn')) 
        f.write(fig_memdiff_swarm2.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_memdiff_swarm3.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_cyto.to_html(full_html=False, include_plotlyjs='cdn'))
       # f.write(fig_date.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))

    uri = pathlib.Path('p_graph.html').absolute().as_uri()
    webbrowser.open(uri)
    return send_file('p_graph.html', as_attachment=True)


# MemDIff 2nd row 
@app.route('/process-files', methods=['POST'])
def process_files():
    file1 = request.files['globalfile']
    file2 = request.files['patientfile']
    name = request.form['username']
    xls_patient = pd.ExcelFile(file2)
    df_infosheet = pd.read_excel(xls_patient, "General Information") 
    general_info = df_infosheet['Value:'].tolist()[1:]
    df = pd.read_excel(xls_patient, "Characterization Data", header=[0,1]) 
    #combines the first 2 rows into column titles
    df.columns = ['.'.join(col).strip() for col in df.columns.values]
    
    TBNK_Day0_Pre = df.iloc[0:11, 1]
    TBNK_Day0_Post = df.iloc[0:11, 2]
    TBNK_Day9_Final = df.iloc[0:11, 3]
    TBNK_Day0_Pre = TBNK_Day0_Pre.to_list()
    TBNK_Day0_Post = TBNK_Day0_Post.to_list()
    TBNK_Day9_Final = TBNK_Day9_Final.to_list()
    TBNK_ratios = df.iloc[11, 1:4].to_list()
    TBNK_col = general_info + TBNK_Day0_Pre + TBNK_Day0_Post + TBNK_Day9_Final + TBNK_ratios

    MemDiff_Day0Post = (df.iloc[0:14, 5]).to_list()
    MemDiff_Day9Final = (df.iloc[0:14, 7]).to_list()
    MemDiff_col = general_info + MemDiff_Day0Post + MemDiff_Day9Final 

    exhaustion_day9 = general_info + (df.iloc[0:9, 9]).to_list()

    cytotox = general_info + (df.iloc[0:6, 11]).to_list() 

    cytokine = general_info + (df.iloc[0:4, 13]).to_list()
 


    # cell_count = general_info + (df.iloc[0:1, 14]).to_list() + (df.iloc[0:1, 15]).to_list() + (df.iloc[0:1, 16]).to_list() + (df.iloc[0:1, 17]).to_list() + (df.iloc[0:1, 18]).to_list() 

    excel_file = pd.ExcelFile(file1)
    dfs = {sheet_name: excel_file.parse(sheet_name) for sheet_name in excel_file.sheet_names}


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

    # df_TBNK = dfs["Cell Growth plot"] 
    # df_TBNK[name] = cell_count 

    # data date tracking carry 
    df_1 = pd.read_excel(xls_patient, "Date Tracking") 
    date_data_df = dfs['Data Date Tracking']

    start = df_1["TAT to Start Method"].tolist()
    complete = df_1["TAT to Complete Method"].tolist()
    qa = (df_1["TAT For QA review"].tolist())[0:11]
    results = df_1["TAT to Receive Results"].tolist()
    list = start + complete + qa + results
    date_data_df[name] = list

    #release data
    df_1 = pd.read_excel(xls_patient, "QC Release Data") 
    release = df_1['Result'].tolist()
    release_data = general_info + [None] + release
    date_data_df = dfs['QC Release Results Summary']
    date_data_df[name] = release_data

    #in_process data
    input = []
    process = pd.read_excel(xls_patient, "In Process Data") 
    ip = process['In Process Features'].tolist()
    sub_id = ip.index('Subject ID')
    don_id = ip.index('Donation ID')
    cell_num = ip.index('# of cells collected during apheresis')
    d0_title = ip.index('D0 Incoming Apheresis')
    aph_vol = ip.index('Thawed Apheresis Volume (mL)')
    aph_inc_vol = ip.index('Diluted Incoming Apheresis Volume (mL)')
    aph_vcc = ip.index('Diluted Apheresis VCC')
    aph_via = ip.index('Diluted Apheresis Viability (%)')
    aph_tvc = ip.index('Total Viable Cells Thawed Apheresis')
    aph_rec = ip.index('% Recovery of Cells Post Thaw Leukopak')
    aph_remv = ip.index('Remaining Apheresis Volume')

    column = process['Values'].tolist()
    input = general_info + [column[sub_id], column[don_id], column[cell_num], column[d0_title], column[aph_vol], column[aph_inc_vol], column[aph_vcc], column[aph_via], column[aph_tvc], column[aph_rec], column[aph_remv]]
    d0_post_title = ip.index('D0 Post Enrichment of T cells')
    post_vol = ip.index('Post Enrichment Total Volume')
    aph_inc_vol = ip.index('Diluted Incoming Apheresis Volume (mL)')
    post_vcc = ip.index('Post Enrichment Average VCC (actual)')
    post_via = ip.index('Post Enrichment Average Viability (%)')
    post_tvc = ip.index('Post Enrichment Total Viable Cells (actual)')
    post_csv = ip.index('Cell Seeding Volume (mL)')
    actnum_cell = ip.index('Actual Cell Number for Culture')
    post_reccells = ip.index('% Recovery of Cells Post Enrichment')
    post_cell_prodigy = ip.index('% Post Enriched Cells Used to Seed Prodigy')

    input2 = [column[d0_post_title], column[post_vcc], column[post_via], column[post_vol], column[post_tvc], column[post_reccells], column[post_cell_prodigy], column[post_csv], column[actnum_cell]]
    d1_lvv = ip.index('D1 LVV Transduction')
    lvv_vol = ip.index('LVV Volume Calculated (mL)')
    d6_title = ip.index('D6 CCV')
    d6_vcc = ip.index('Day 6 VCC')
    d6_via = ip.index('Day 6 Viability (%)')
    d6_tv = ip.index('Day 6 Total Volume (mL)')
    d6_tvc = ip.index('Day 6 Total Viable Cells')
    d6_fold = ip.index('Day 6 Fold Expansion')
    d7_title = ip.index('D7 CCV')
    d7_vcc = ip.index('Day 7 VCC')
    d7_via = ip.index('Day 7 Viability (%)')
    d7_tv = ip.index('Day 7 Total Volume (mL)')
    d7_tvc = ip.index('Day 7 Total Viable Cells')
    d7_fold = ip.index('Day 7 Fold Expansion')
    dm1h_title = ip.index('Harvest -1D CCV and CAR')
    dm1h_vcc = ip.index('Harvest -1Day VCC')
    dm1h_via = ip.index('Harvest -1Day Viability (%)')
    dm1h_tv = ip.index('Harvest -1Day Total Volume (mL)')
    dm1h_tvc = ip.index('Harvest -1Day Total Viable Cells')
    dm1h_fold = ip.index('Harvest -1Day Fold Expansion')
    dm1h_car = ip.index('Harvest -1Day CAR (%)')
    preharv_title = ip.index('Pre Harvest')
    preharv_vcc = ip.index('Pre Harvest VCC')
    preharv_via = ip.index('Pre Harvest Viability (%)')
    preharv_tv = ip.index('Pre Harvest Total Volume (mL)')
    preharv_tvc = ip.index('Pre Harvest Total Viable Cells')
    preharv_fold = ip.index('Pre Harvest Fold Expansion')

    input3 = [column[d1_lvv], column[lvv_vol], column[d6_title], column[d6_vcc], column[d6_via], column[d6_tv], column[d6_tvc], column[d6_fold], column[d7_title], column[d7_vcc], column[d7_via], column[d7_tv], column[d7_tvc], column[d7_fold]]
    input4 = [column[dm1h_title], column[dm1h_vcc], column[dm1h_via], column[dm1h_tv], column[dm1h_tvc], column[dm1h_fold], column[dm1h_car], column[preharv_title], column[preharv_vcc], column[preharv_via], column[preharv_tv], column[preharv_tvc], column[preharv_fold]]

    postharv_title = ip.index('Post Harvest, Formulation')
    postharv_vcc = ip.index('Post Harvest Average VCC (actual)')
    postharv_via = ip.index('Post Harveset Average Viability (%)')
    postharv_chv = ip.index('Cell Harvest Volume (mL)')
    postharv_tvc = ip.index('Total Viable Cells Harvested (actual)')
    postharv_cardose = ip.index('Total Viable CAR+ per Dose')
    postharv_vccdose = ip.index('VCC Required for Dose')
    postharv_doserecorded = ip.index('Total Viable Cells per Dose (recorded)')
    postharv_fpv = ip.index('Final Product Volume (mL)')
    postharv_fold = ip.index('Post Harvest Fold Expansion')
    postharv_reccells = ip.index('% Recovery of Cells Harvested')
    cyro_bag1 = ip.index('Final Product Bag 1 Volume (mL)')
    cyro_bag2 = ip.index('Final Product Bag 2 Volume (mL)')
    cyro_vials = ip.index('Number of 1 mL Vials Retain Filled')
    cyro_bags = ip.index('Number of Dose Bags Transferred to CRF')
    cyro_vials_crf = ip.index('Number of 1 Vials Transferred to CRF')

    input5 = [column[postharv_title], column[postharv_vcc], column[postharv_via], column[postharv_chv], column[postharv_tvc], column[postharv_fold], column[postharv_reccells], column[postharv_cardose], column[postharv_doserecorded], column[postharv_vccdose], column[postharv_fpv], column[cyro_bag1], column[cyro_bag2], None, column[cyro_vials], column[cyro_bags], column[cyro_vials_crf]]
    input.extend(input2)
    input.extend(input3)
    input.extend(input4)
    input.extend(input5)


    df_ip = dfs["In Process Data Summary"]
    df_ip[name] = input 

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
    process = dfs["In Process Data Summary"]
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
    ip_values = process['Batch #'].tolist()
    via_aph_index = ip_values.index('Diluted Apheresis Viability (%)')
    fold_index = ip_values.index('Pre Harvest Fold Expansion')
    cg_0 = ip_values.index('Actual Cell Number for Culture')
    cg_6 = ip_values.index('Day 6 Total viable cells')
    cg_7 = ip_values.index('Day 7 Total Viable cells')
    cg_hm1 = ip_values.index('Harvest -1Day Total Viable Cells')
    cg_tvc = ip_values.index('Pre Harvest Total Viable Cells')
    percent_0 = ip_values.index('Post Enrichment Average Viability (%)')
    percent_6 = ip_values.index('Day 6 Viability (%)')
    percent_7 = ip_values.index('Day 7 Viability (%)')
    percent_8 = ip_values.index('Harvest -1Day Viability (%)')
    percent_9pre = ip_values.index('Pre Harvest Viability (%)')
    percent_9post = ip_values.index('Post Harvest Average Viability (%)')
    

    release = dfs["QC Release Results Summary"]
    release_values = release['Unnamed: 1'].tolist()
    cg_fdp = release_values.index('Viability')

    for patient in col_names:
        column = process[patient]
        viability_aph.append(column[via_aph_index])
        fold_expansion.append(column[fold_index])
        cell_growth_0_r.append(column[cg_0])
        cell_growth_6_r.append(column[cg_6])
        cell_growth_7_r.append(column[cg_7])
        cell_growth_8_r.append(column[cg_hm1])
        cell_growth_9_r.append(column[cg_tvc])
        cell_via_0_post.append(column[percent_0]) #15
        cell_growth_6.append(column[percent_6]) #27
        cell_growth_7.append(column[percent_7]) #32
        cell_growth_8.append(column[percent_8])
        cell_growth_9_pre.append(column[percent_9pre])
        cell_growth_9_post.append(column[percent_9post])
        r_1 = release[patient]
        cell_growth_fdp.append(r_1[cg_fdp])
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
        if pd.isna(cell_growth_7_r[i]):
            list_ = [cell_growth_0_r[i], cell_growth_6_r[i], cell_growth_8_r[i], cell_growth_9_r[i]]
        else :
            list_ = [cell_growth_0_r[i], cell_growth_6_r[i], cell_growth_7_r[i], cell_growth_8_r[i], cell_growth_9_r[i]]
        fig_sub_process_2.add_trace(go.Scatter(x=x_axis, y=list_, name=col_names[i]), row = 1, col = 2)

    fig_sub_process_2.update_layout(title={'text': "Process Performance", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
    # fig_sub_process_2.show()

    colors2 = ["yellow", "orange", "red", "green", "blue", "goldenrod", "magenta", "blue", "purple", "pink", "grey" ]
    fig_sub_process_3 = make_subplots(rows=2, cols=2, subplot_titles=("Cell Viability over Process", "Cell Viability (Aph. - d6)", "Cell Viability (Pre- and Post-Harvest, FDP)"))
    x_axis = ["0 (Aph)", "0 (Post)", "6", "7", "8", "9 (Pre)", "9 (Post)", "FDP"]
    for i in range(len(col_names)):
        if pd.isna(cell_growth_7_r[i]):
            list_ = [cell_via_0_aph[i], cell_via_0_post[i], cell_growth_6[i], cell_growth_8[i], cell_growth_9_pre[i], cell_growth_9_post[i], cell_growth_fdp[i]]
        else:
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

    tbnk_values = TBNK['Batch #'].tolist()
    CD4_i = tbnk_values.index('Day 0 Post-Enrichment - CD4+ T cells')
    CD8_i = tbnk_values.index('Day 0 Post-Enrichment - CD8+ T cells')
    CD4_fdp_i = tbnk_values.index('Final Product - CD4+ T cells')
    CD8_fdp_i = tbnk_values.index('Final Product - CD8+ T cells')
    bcellspre_i = tbnk_values.index('Day 0 Pre-Enrichment - B cells')
    cd4pre_i = tbnk_values.index('Day 0 Pre-Enrichment - CD4+ T cells')
    cd4cd8pre_i = tbnk_values.index('Day 0 Pre-Enrichment - CD4+ CD8+ T cells')
    cd56cd16pre_i = tbnk_values.index('Day 0 Pre-Enrichment - CD56+ CD16+ T cells')
    cd8pre_i = tbnk_values.index('Day 0 Pre-Enrichment - CD8+ T cells')
    eosino_pre_i = tbnk_values.index('Day 0 Pre-Enrichment - Eosinophils')
    mono_pre_i = tbnk_values.index('Day 0 Pre-Enrichment - Monocytes')
    neutro_pre_i = tbnk_values.index('Day 0 Pre-Enrichment - Neutrophils')
    nkt_pre_i = tbnk_values.index('Day 0 Pre-Enrichment - NKT cells')
    b_fdp_i = tbnk_values.index('Final Product - B cells')
    cd4_fdp_i = tbnk_values.index('Final Product - CD4+ T cells')
    cd4cd8_fdp_i = tbnk_values.index('Final Product - CD4+ CD8+ T cells')
    cd56cd16_fdp_i = tbnk_values.index('Final Product - CD56+ CD16+ T cells')
    cd8_fdp_i = tbnk_values.index('Final Product - CD8+ T cells')
    eosino_fdp_i = tbnk_values.index('Final Product - Eosinophils')
    mono_fdp_i = tbnk_values.index('Final Product - Monocytes')
    neutro_fdp_i = tbnk_values.index('Final Product - Neutrophils')
    nkt_fdp_i = tbnk_values.index('Final Product - NKT cells')
    cd4_post_i = tbnk_values.index('Day 0 Post-Enrichment - CD4+ T cells')
    cd8_post_i = tbnk_values.index('Day 0 Post-Enrichment - CD8+ T cells')


    for patient in col_names:
        column = TBNK[patient]
        CD4.append(column[CD4_i])
        CD8.append(column[CD8_i])
        CD4_FDP.append(column[CD4_fdp_i])
        CD8_FDP.append(column[CD8_fdp_i])
        Bcells_Pre.append(column[bcellspre_i])
        CD4_Pre.append(column[cd4pre_i])
        CD4CD8_Pre.append(column[cd4cd8pre_i])
        CD56CD16_Pre.append(column[cd56cd16pre_i])
        CD8_Pre.append(column[cd8pre_i])
        Eosinophil_Pre.append(column[eosino_pre_i])
        Monocyte_Pre.append(column[mono_pre_i])
        Neutrophil_Pre.append(column[neutro_pre_i])
        NKT_Pre.append(column[nkt_pre_i])
        Bcells_fdp.append(column[b_fdp_i])
        CD4_fdp.append(column[cd4_fdp_i])
        CD4CD8_fdp.append(column[cd4cd8_fdp_i])
        CD56CD16_fdp.append(column[cd56cd16_fdp_i])
        CD8_fdp.append(column[cd8_fdp_i])
        Eosinophil_fdp.append(column[eosino_fdp_i])
        Monocyte_fdp.append(column[mono_fdp_i])
        Neutrophil_fdp.append(column[neutro_fdp_i])
        NKT_fdp.append(column[nkt_fdp_i])
        CD4_Post.append(column[cd4_post_i])
        CD8_Post.append(column[cd8_post_i])


    CD4_ = CD4
    CD8_ = CD8

    fig_3 = go.Figure(data=[
        go.Bar(name='CD4+', x=col_names, y=CD4_),
        go.Bar(name='CD8+', x=col_names, y=CD8_)
    ])
    # change bar mode
    fig_3.update_layout(barmode='stack', title={'text': "%CD4+ and %CD8+ Cells (Post Enrichment)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
  #  fig_3.show()

    #Graph for %CD4+ and %CD8+ FDP Stacked Bar Plot
    CD4_FDP_ = CD4_FDP
    CD8_FDP_  = CD8_FDP


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

    MemDiff = dfs["Mem-Diff"]
    memdiff_values = MemDiff['Batch #'].tolist()

    CD8_fdp_tem_i = memdiff_values.index('Final Product - CD3+\CAR+\CD8+\Tem')
    CD8_fdp_temra_i = memdiff_values.index('Final Product - CD3+\CAR+\CD8+\Temra')
    CD8_fdp_tcm_i = memdiff_values.index('Final Product - CD3+\CAR+\CD8+\Tcm')
    CD8_fdp_tscm_i = memdiff_values.index('Final Product - CD3+\CAR+\CD8+\Tscm')
    CD8_fdp_tn_i = memdiff_values.index('Final Product - CD3+\CAR+\CD8+\Tn')

    CD4_fdp_tem_i = memdiff_values.index('Final Product - CD3+\CAR+\CD4+\Tem')
    CD4_fdp_temra_i = memdiff_values.index('Final Product - CD3+\CAR+\CD4+\Temra')
    CD4_fdp_tcm_i = memdiff_values.index('Final Product - CD3+\CAR+\CD4+\Tcm')
    CD4_fdp_tscm_i = memdiff_values.index('Final Product - CD3+\CAR+\CD4+\Tscm')
    CD4_fdp_tn_i = memdiff_values.index('Final Product - CD3+\CAR+\CD4+\Tn')

    CD8_post_tem_i = memdiff_values.index('Day 0 Post-Enrichment - CD3+\CD8+\Tem')
    CD8_post_temra_i = memdiff_values.index('Day 0 Post-Enrichment - CD3+\CD8+\Temra')
    CD8_post_tcm_i = memdiff_values.index('Day 0 Post-Enrichment - CD3+\CD8+\Tcm')
    CD8_post_tscm_i = memdiff_values.index('Day 0 Post-Enrichment - CD3+\CD8+\Tscm')
    CD8_post_tn_i = memdiff_values.index('Day 0 Post-Enrichment - CD3+\CD8+\Tn')

    CD4_post_tem_i = memdiff_values.index('Day 0 Post-Enrichment - CD3+\CD4+\Tem')
    CD4_post_temra_i = memdiff_values.index('Day 0 Post-Enrichment - CD3+\CD4+\Temra')
    CD4_post_tcm_i = memdiff_values.index('Day 0 Post-Enrichment - CD3+\CD4+\Tcm')
    CD4_post_tscm_i = memdiff_values.index('Day 0 Post-Enrichment - CD3+\CD4+\Tscm')
    CD4_post_tn_i = memdiff_values.index('Day 0 Post-Enrichment - CD3+\CD4+\Tn')


    for patient in col_names:
        column = MemDiff[patient]
        CD8_FDP_Tem.append(column[CD8_fdp_tem_i])
        CD8_FDP_Temra.append(column[CD8_fdp_temra_i])
        CD8_FDP_Tcm.append(column[CD8_fdp_tcm_i])
        CD8_FDP_Tscm.append(column[CD8_fdp_tscm_i])
        CD8_FDP_Tn.append(column[CD8_fdp_tn_i])
        CD4_FDP_Tem.append(column[CD4_fdp_tem_i])
        CD4_FDP_Temra.append(column[CD4_fdp_temra_i])
        CD4_FDP_Tcm.append(column[CD4_fdp_tcm_i])
        CD4_FDP_Tscm.append(column[CD4_fdp_tscm_i])
        CD4_FDP_Tn.append(column[CD4_fdp_tn_i])

        CD4_Post_Tem.append(column[CD4_post_tem_i])
        CD4_Post_Temra.append(column[CD4_post_temra_i])
        CD4_Post_Tcm.append(column[CD4_post_tcm_i])
        CD4_Post_Tscm.append(column[CD4_post_tscm_i])
        CD4_Post_Tn.append(column[CD4_post_tn_i])
        CD8_Post_Tem.append(column[CD8_post_tem_i])
        CD8_Post_Temra.append(column[CD8_post_temra_i])
        CD8_Post_Tcm.append(column[CD8_post_tcm_i])
        CD8_Post_Tscm.append(column[CD8_post_tscm_i])
        CD8_Post_Tn.append(column[CD8_post_tn_i])


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
    cytokine_values = cytokine['Batch #'].tolist()
    p51 = cytokine_values.index('IFNg 5:1 (CD19+) (pg/mL) E:T Ratio')
    p101 = cytokine_values.index('IFNg 10:1 (CD19+) (pg/mL) E:T Ratio')
    m51 = cytokine_values.index('IFNg 5:1 (CD19-) (pg/mL) E:T Ratio')
    m101 = cytokine_values.index('IFNg 10:1 (CD19-) (pg/mL) E:T Ratio')


    CD19P_5_1 = []
    CD19P_10_1 = []
    CD19M_5_1 = []
    CD19M_10_1 = []
    
    for patient in col_names:
        column =  cytokine[patient]
        CD19P_5_1.append(column[p51])
        CD19P_10_1.append(column[p101])
        CD19M_5_1.append(column[m51])
        CD19M_10_1.append(column[m101])

    cytotox = dfs["Cytotox"]
    cytotox_values = cytotox['Batch #'].tolist()
    p11 = cytotox_values.index('1:1 (CD19+) E:T')
    p51 = cytotox_values.index('5:1 (CD19+) E:T')
    p101 = cytotox_values.index('10:1 (CD19+) E:T')
    m11 = cytotox_values.index('1:1 (CD19-) E:T')
    m51 = cytotox_values.index('5:1 (CD19-) E:T')
    m101 = cytotox_values.index('10:1 (CD19-) E:T')

    one_to_one = []
    five_to_one = []
    ten_to_one = []

    for patient in col_names:
        column =  cytotox[patient]
        one_to_one.append(column[p11])
        five_to_one.append(column[p51])
        ten_to_one.append(column[p101])

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
        new_1 = name + ' Release'
        release_assays.append(new_1)
        new_2 = name + ' Char'
        char_assays.append(new_2)
    titles = release_assays + char_assays
    print(titles)
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
