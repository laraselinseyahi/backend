import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pathlib, webbrowser
from itertools import chain
import pathlib



    # def
    #   file1 = request.files['globalfile']
def visualization(filename):
    xls = pd.ExcelFile(filename)

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
    for i in range(len(col_names)):
        list_ = [cell_via_0_aph[i], cell_via_0_post[i], cell_growth_6[i], cell_growth_7[i], cell_growth_8[i], cell_growth_9_pre[i], cell_growth_9_post[i], cell_growth_fdp[i]]
        fig_sub_process_3.add_trace(go.Scatter(x=x_axis, y=list_, name=col_names[i]), row = 1, col = 1)
    x_axis = ["0 (Aph)", "0 (Post)", "6"]
    for i in range(len(col_names)):
        list_ = [cell_via_0_aph[i], cell_via_0_post[i], cell_growth_6[i]]
        fig_sub_process_3.add_trace(go.Scatter(x=x_axis, y=list_, name=col_names[i]), row = 1, col = 2)
    x_axis = [ "9 (Pre)", "9 (Post)", "FDP"]
    for i in range(len(col_names)):
        list_ = [cell_growth_9_pre[i], cell_growth_9_post[i], cell_growth_fdp[i]]
        fig_sub_process_3.add_trace(go.Scatter(x=x_axis, y=list_, name=col_names[i]), row = 2, col = 1)
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
    CD8_FDP_Tem = (MemDiff.loc[17, :].values.tolist())[3:]
    CD8_FDP_Temra = (MemDiff.loc[18, :].values.tolist())[3:]
    CD8_FDP_Tcm = (MemDiff.loc[19, :].values.tolist())[3:]
    CD8_FDP_Tscm = (MemDiff.loc[20, :].values.tolist())[3:]
    CD8_FDP_Tn = (MemDiff.loc[21, :].values.tolist())[3:]

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
    CD4_FDP_Tem = (MemDiff.loc[23, :].values.tolist())[3:]
    CD4_FDP_Temra = (MemDiff.loc[24, :].values.tolist())[3:]
    CD4_FDP_Tcm = (MemDiff.loc[25, :].values.tolist())[3:]
    CD4_FDP_Tscm = (MemDiff.loc[26, :].values.tolist())[3:]
    CD4_FDP_Tn = (MemDiff.loc[27, :].values.tolist())[3:]

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
    CD4_Post_Tem = (MemDiff.loc[9, :].values.tolist())[3:]
    CD4_Post_Temra = (MemDiff.loc[10, :].values.tolist())[3:]
    CD4_Post_Tcm = (MemDiff.loc[11, :].values.tolist())[3:]
    CD4_Post_Tscm = (MemDiff.loc[12, :].values.tolist())[3:]
    CD4_Post_Tn = (MemDiff.loc[13, :].values.tolist())[3:]

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
    CD8_Post_Tem = (MemDiff.loc[3, :].values.tolist())[3:]
    CD8_Post_Temra = (MemDiff.loc[4, :].values.tolist())[3:]
    CD8_Post_Tcm = (MemDiff.loc[5, :].values.tolist())[3:]
    CD8_Post_Tscm = (MemDiff.loc[6, :].values.tolist())[3:]
    CD8_Post_Tn = (MemDiff.loc[7, :].values.tolist())[3:]

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


    uri = pathlib.Path('p_graph.html').absolute().as_uri()
    webbrowser.open(uri)
   # html_file_path = pathlib.Path('p_graph.html')

# Get the absolute path of the HTML file
  #  absolute_path = html_file_path.absolute()

# Generate the download link for the HTML file
   # download_link = f'<a href="{absolute_path}" download>Download HTML</a>'

# Generate the HTML response containing the download link
 #   html_response = f"""
 #   <html>
 #   <body>
 #   <h1>Download HTML</h1>
 #   {download_link}
 #   </body>
 #   </html>
 #   """

# Print or use the HTML response as needed
#   print(html_response)












