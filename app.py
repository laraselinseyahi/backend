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
import carrying_data as cd
import global_graphs_1 as gg
import global_graphs_2 as ip
import tbnk_graphs as tbnk
import memdiff_graphs as mdiff
import cytotox_cytokine_graphs as cc
import tables as t



app = Flask(__name__, static_url_path='/static')
CORS(app)



@app.route('/')
def index():
    return jsonify({'message': 'Hello from the backend!'})

@app.route('/process-datavis', methods=['POST'])
def process_datavis():
    global_sheet = request.files['fileInput']
    xls = pd.ExcelFile(global_sheet)

    # Read the Excel file into a dictionary of DataFrames
    dfs = {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names}
    data_frame = dfs["QC Release Results Summary"]
    col_names = list(data_frame.columns.values.tolist())
    col_names = col_names[4:]

    names_1 = data_frame[data_frame['Batch #'] == 'Study (e.g. KYV-IH, KYV-001, KYV-003)'].values[0].tolist()[4:]
    names_2 = data_frame[data_frame['Batch #'] == 'Patient No. w/in Study'].values[0].tolist()[4:]

    names = []
    for i in range(len(names_1)):
        name_info = str(names_1[i]) + '-' + str(names_2[i])
        names.append(name_info)

    col_names = names

    fig_sub_1 = gg.release_graphs(dfs, col_names)
    fig_2 = gg.day8_day9_graph(dfs, col_names)

    colors_bub = ['black', 'black']
    colors_add = ['red'] * (len(col_names) - 2)
    colors_bub += colors_add
    colors_bub = ['red'] * (len(col_names))

    fig_sub_process_2 = ip.ip_graphs_1(dfs, col_names)
    fig_sub_process_3 = ip.ip_graphs_2(dfs, col_names)

    tbnk_graphs_all = tbnk.tbnk_graphs_4(dfs, col_names)
    fig_tbnk = tbnk_graphs_all[0]
    fig_tbnk_2 = tbnk_graphs_all[1]
    tbnk_swarm1 = tbnk_graphs_all[2]
    tbnk_swarm2 = tbnk_graphs_all[3]


    memdiff_graphs = mdiff.memdiff(dfs, col_names)
    fig_memdiff = memdiff_graphs[0]
    fig_memdiff_swarm1 = memdiff_graphs[1]
    fig_memdiff_swarm2 = memdiff_graphs[2]
    fig_memdiff_swarm3 = memdiff_graphs[3]


    fig_cyto = cc.cytotox_cytokine(dfs, col_names)[0]
    fig_cytokine_swarm1 = cc.cytotox_cytokine(dfs, col_names)[1]

    fig = t.table(dfs, col_names, xls)[0]
    fig_tbnk_table = t.table(dfs, col_names, xls)[1]
    fig_table3 = t.table(dfs, col_names, xls)[2]
    fig_tbnk_table2 = t.table(dfs, col_names, xls)[3]
    fig_rel = t.table(dfs, col_names, xls)[4]
    

    with open('p_graph.html', 'w') as f:
        f.write(fig_sub_1.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_sub_process_2.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_sub_process_3.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_2.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_tbnk.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_tbnk_2.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(tbnk_swarm1.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(tbnk_swarm2.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_memdiff.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_memdiff_swarm1.to_html(full_html=False, include_plotlyjs='cdn')) 
        f.write(fig_memdiff_swarm2.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_memdiff_swarm3.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_cyto.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_cytokine_swarm1.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_tbnk_table.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_table3.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_tbnk_table2.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_rel.to_html(full_html=False, include_plotlyjs='cdn'))
        
        
    uri = pathlib.Path('p_graph.html').absolute().as_uri()
    webbrowser.open(uri)
    return send_file('p_graph.html', as_attachment=True)



@app.route('/process-files', methods=['POST'])
def process_files():
    file1 = request.files['globalfile']
    file2 = request.files['patientfile']
    name = request.form['username']
    xls_patient = pd.ExcelFile(file2)
    df_infosheet = pd.read_excel(xls_patient, "General Information") 
    excel_file = pd.ExcelFile(file1)
    dfs = {sheet_name: excel_file.parse(sheet_name) for sheet_name in excel_file.sheet_names}
    cd.carry_data(df_infosheet, xls_patient, dfs, name)
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

    fig_sub_2 = make_subplots(rows=1, cols=2, subplot_titles=("%CD4+ and %CD8+ Cells (Post Enrichment)", "%CD4+ and %CD8+ Cells (FDP)"))
    colors = ['blue', 'red', 'green', 'orange', 'purple']

    fig_sub_2.add_trace(go.Bar(name='CD4+', x=col_names, y=CD4_, marker_color=colors[0]), row=1, col=1)
    fig_sub_2.add_trace(go.Bar(name='CD8+', x=col_names, y=CD8_, marker_color=colors[1]), row=1, col=1)
    fig_sub_2.add_trace(go.Bar(name='', x=col_names, y=CD4_FDP_, marker_color=colors[0], showlegend=False), row=1, col=2)
    fig_sub_2.add_trace(go.Bar(name='', x=col_names, y=CD8_FDP_, marker_color=colors[1], showlegend=False), row=1, col=2)

    fig_sub_2.update_layout(barmode='stack', title={'text': "%CD4+ and %CD8+ Cells", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})





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
