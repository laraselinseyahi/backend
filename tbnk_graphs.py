import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from itertools import chain



def tbnk_graphs_4(dfs, col_names):

    TBNK = dfs["TBNK"] 
    CD4 = (TBNK.loc[TBNK['Batch #'] == 'Day 0 Post-Enrichment - CD4+ T cells'].values[0].tolist())[1:]
    CD8 = (TBNK.loc[TBNK['Batch #'] == 'Day 0 Post-Enrichment - CD8+ T cells'].values[0].tolist())[1:]
    CD4_ = CD4
    CD8_ = CD8

    fig_3 = go.Figure(data=[
        go.Bar(name='CD4+', x=col_names, y=CD4_),
        go.Bar(name='CD8+', x=col_names, y=CD8_)
    ])
    #barmode is important
    fig_3.update_layout(barmode='stack', title={'text': "%CD4+ and %CD8+ Cells (Post Enrichment)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})


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


    fig_sub_2 = make_subplots(rows=1, cols=2, subplot_titles=("%CD4+ and %CD8+ Cells (Post Enrichment)", "%CD4+ and %CD8+ Cells (FDP)"))
    colors = ['blue', 'red', 'green', 'orange', 'purple']

    fig_sub_2.add_trace(go.Bar(name='CD4+', x=col_names, y=CD4_, marker_color=colors[0]), row=1, col=1)
    fig_sub_2.add_trace(go.Bar(name='CD8+', x=col_names, y=CD8_, marker_color=colors[1]), row=1, col=1)
    fig_sub_2.add_trace(go.Bar(name='', x=col_names, y=CD4_FDP_, marker_color=colors[0], showlegend=False), row=1, col=2)
    fig_sub_2.add_trace(go.Bar(name='', x=col_names, y=CD8_FDP_, marker_color=colors[1], showlegend=False), row=1, col=2)

    fig_sub_2.update_layout(barmode='stack', title={'text': "%CD4+ and %CD8+ Cells", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})

    
    #burdan
    
    TBNK = dfs["TBNK"]
 
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

    #TBNK swarm plot 1 - Page 7
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
    #Start test
    # Create a subplot figure


    figsca1 = make_subplots(rows=1, cols=3, subplot_titles=("Pre", "Post", "FDP" ))

    patients_pre = []
    for i in range(len(col_names)):
        new_list = [Bcells_Pre[i], CD56CD16_Pre[i], Eosinophil_Pre[i], Monocyte_Pre[i], Neutrophil_Pre[i], NKT_Pre[i], T_Pre[i]]
        patients_pre.append(new_list)

    patients_post = []
    for i in range(len(col_names)):
        new_list = [Bcells_Post[i], CD56CD16_Post[i], Eosinophil_Post[i], Monocyte_Post[i], Neutrophil_Post[i], NKT_Post[i], T_Post[i]]
        patients_post.append(new_list)

    patients_fdp = []
    for i in range(len(col_names)):
        new_list = [Bcells_fdp[i], CD56CD16_fdp[i], Eosinophil_fdp[i], Monocyte_fdp[i], Neutrophil_fdp[i], NKT_fdp[i], T_fdp[i]]
        patients_fdp.append(new_list)

    text = ['B cells', 'CD56CD16', 'Eosinophil', 'Monocyte', 'Neutrophil', 'NKT cells', 'T cells']
    colors_test = ['blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgrey', 'darkgreen', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'grey', 'green', 'greenyellow', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgrey', 'lightgreen', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'red', 'rosybrown', 'royalblue', 'rebeccapurple', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen', 'aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black', 'blanchedalmond']


    for i in range(len(col_names)):
    # Add strip plots to the subplots with custom names
        figsca1.add_trace(go.Scatter(y=patients_pre[i], mode='markers', name=col_names[i], marker_color=colors_test[i]), row=1, col=1)
        figsca1.add_trace(go.Scatter(y=patients_post[i], mode='markers', name=col_names[i], marker_color=colors_test[i], showlegend=False), row=1, col=2)
        figsca1.add_trace(go.Scatter(y=patients_fdp[i], mode='markers', name=col_names[i], marker_color=colors_test[i], showlegend=False), row=1, col=3)

    custom_tickvals = list(range(0, len(text) + 1))
    custom_ticktext = text

    figsca1.update_xaxes(tickvals=custom_tickvals, ticktext=custom_ticktext, row=1, col=1)
    figsca1.update_xaxes(tickvals=custom_tickvals, ticktext=custom_ticktext, row=1, col=2)
    figsca1.update_xaxes(tickvals=custom_tickvals, ticktext=custom_ticktext, row=1, col=3)

    figsca1.update_yaxes(range=[-5, 100] , row=1, col=1)
    figsca1.update_yaxes(range=[-5, 100] , row=1, col=2)
    figsca1.update_yaxes(range=[-5, 100] , row=1, col=3)


    # Show the plot
    figsca1.show()






    # TBNK Individual Swarm Plots - Page 8 
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

    tbnk_swarm2.update_yaxes(range=[-5, 40] , row=1, col=1)
    tbnk_swarm2.update_yaxes(range=[-5, 40] , row=1, col=2)
    tbnk_swarm2.update_yaxes(range=[-5, 40] , row=2, col=1)
    tbnk_swarm2.update_yaxes(range=[-5, 40] , row=2, col=2)
    tbnk_swarm2.update_yaxes(range=[-5, 100] , row=3, col=1)

    tbnk_swarm2.update_traces(boxpoints='all', jitter=0.5)
    tbnk_swarm2.show()

    figsca2 = make_subplots(rows=3, cols=2, subplot_titles=("B Cells", "CD56CD16", "Monocyte", "NKT", "T Cells" ))

    patients_bcells = []
    for i in range(len(col_names)):
        new_list = [Bcells_Pre[i], Bcells_Post[i], Bcells_fdp[i]]
        patients_bcells.append(new_list)

    patients_cd56cd16 = []
    for i in range(len(col_names)):
        new_list = [CD56CD16_Pre[i], CD56CD16_Post[i], CD56CD16_fdp[i]]
        patients_cd56cd16.append(new_list)

    patients_monocyte = []
    for i in range(len(col_names)):
        new_list = [Monocyte_Pre[i], Monocyte_Post[i], Monocyte_fdp[i]]
        patients_monocyte.append(new_list)

    patients_nkt = []
    for i in range(len(col_names)):
        new_list = [NKT_Pre[i], NKT_Post[i], NKT_fdp[i]]
        patients_nkt.append(new_list)

    patients_t = []
    for i in range(len(col_names)):
        new_list = [T_Pre[i], T_Post[i], T_fdp[i]]
        patients_t.append(new_list)

    text = ['Pre', 'Post', 'FDP']


    for i in range(len(col_names)):
    # Add strip plots to the subplots with custom names
        figsca2.add_trace(go.Scatter(y=patients_bcells[i], mode='markers', name=col_names[i], marker_color=colors_test[i]), row=1, col=1)
        figsca2.add_trace(go.Scatter(y=patients_cd56cd16[i], mode='markers', name=col_names[i], marker_color=colors_test[i], showlegend=False), row=1, col=2)
        figsca2.add_trace(go.Scatter(y=patients_monocyte[i], mode='markers', name=col_names[i], marker_color=colors_test[i], showlegend=False), row=2, col=1)
        figsca2.add_trace(go.Scatter(y=patients_nkt[i], mode='markers', name=col_names[i], marker_color=colors_test[i], showlegend=False), row=2, col=2)
        figsca2.add_trace(go.Scatter(y=patients_t[i], mode='markers', name=col_names[i], marker_color=colors_test[i], showlegend=False), row=3, col=1)

    custom_tickvals = list(range(0, len(text) + 1))
    custom_ticktext = text

    figsca2.update_xaxes(tickvals=custom_tickvals, ticktext=custom_ticktext, row=1, col=1)
    figsca2.update_xaxes(tickvals=custom_tickvals, ticktext=custom_ticktext, row=1, col=2)
    figsca2.update_xaxes(tickvals=custom_tickvals, ticktext=custom_ticktext, row=2, col=1)
    figsca2.update_xaxes(tickvals=custom_tickvals, ticktext=custom_ticktext, row=2, col=2)
    figsca2.update_xaxes(tickvals=custom_tickvals, ticktext=custom_ticktext, row=3, col=1)

    figsca2.update_yaxes(range=[-5, 40] , row=1, col=1)
    figsca2.update_yaxes(range=[-5, 40] , row=1, col=2)
    figsca2.update_yaxes(range=[-5, 40] , row=2, col=1)
    figsca2.update_yaxes(range=[-5, 40] , row=2, col=2)
    figsca2.update_yaxes(range=[-5, 100] , row=3, col=1)
    
    # Show the plot
    figsca2.show()




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
    
    #TBNK Bar Graphs - Page 5 
    fig_tbnk = go.Figure()

    x_axis = list(chain.from_iterable(map(lambda x: [x, x], col_names)))
    my_list = ['Aph', 'FDP']
    result_list = my_list * len(col_names)

    x = [x_axis,result_list]
    names = ['B cells', 'CD4+', 'CD4+CD8+', 'CD56+CD16+', 'CD8+', 'Eosinophil', 'Monocyte', 'Neutrophil', 'NKT']
    for i in range(len(data)):
        fig_tbnk.add_bar(x=x,y=data[i],name=names[i])

    fig_tbnk.update_layout(barmode="relative", title={'text': "Leukocyte Purity (Apheresis and FDP)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})


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

    #TBNK Bar Graphs - Page 6 
    fig_tbnk_2 = go.Figure()

    x_axis = list(chain.from_iterable(map(lambda x: [x, x, x], col_names)))
    my_list = ['Aph', 'Post', 'FDP']
    result_list = my_list * len(col_names)

    x = [x_axis,result_list]
    names = ['CD4+', 'CD8+']
    for i in range(len(data)):
        fig_tbnk_2.add_bar(x=x,y=data[i],name=names[i])

    fig_tbnk_2.update_layout(barmode="relative", title={'text': "%CD4+ and %CD8+ Cells (Aph., Post Enrichment, FDP)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
    
    return fig_tbnk, fig_tbnk_2, tbnk_swarm1, tbnk_swarm2, figsca1, figsca2


#UNUSED GRAPH 
def tbnk_graphs_1(dfs, col_names):   
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
    #barmode is important
    fig_3.update_layout(barmode='stack', title={'text': "%CD4+ and %CD8+ Cells (Post Enrichment)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
    return fig_3

#UNUSED GRAPH
def tbnk_graphs_2(dfs, col_names):
    TBNK = dfs["TBNK"]  
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
    return fig_4

#UNUSED GRAPH
def tbnk_graphs_3(dfs, col_names):
    TBNK = dfs["TBNK"]
    CD4 = (TBNK.loc[TBNK['Batch #'] == 'Day 0 Post-Enrichment - CD4+ T cells'].values[0].tolist())[1:]
    CD8 = (TBNK.loc[TBNK['Batch #'] == 'Day 0 Post-Enrichment - CD8+ T cells'].values[0].tolist())[1:]
    CD4_FDP = (TBNK.loc[TBNK['Batch #'] == 'Final Product - CD4+ T cells'].values[0].tolist())[1:] 
    CD8_FDP = (TBNK.loc[TBNK['Batch #'] == 'Final Product - CD8+ T cells'].values[0].tolist())[1:] 

    fig_sub_2 = make_subplots(rows=1, cols=2, subplot_titles=("%CD4+ and %CD8+ Cells (Post Enrichment)", "%CD4+ and %CD8+ Cells (FDP)"))
    colors = ['blue', 'red', 'green', 'orange', 'purple']

    fig_sub_2.add_trace(go.Bar(name='CD4+', x=col_names, y=CD4, marker_color=colors[0]), row=1, col=1)
    fig_sub_2.add_trace(go.Bar(name='CD8+', x=col_names, y=CD8, marker_color=colors[1]), row=1, col=1)
    fig_sub_2.add_trace(go.Bar(name='', x=col_names, y=CD4_FDP, marker_color=colors[0], showlegend=False), row=1, col=2)
    fig_sub_2.add_trace(go.Bar(name='', x=col_names, y=CD8_FDP, marker_color=colors[1], showlegend=False), row=1, col=2)

    fig_sub_2.update_layout(barmode='stack', title={'text': "%CD4+ and %CD8+ Cells", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
    return fig_sub_2


