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
    
    return fig_tbnk, fig_tbnk_2, tbnk_swarm1, tbnk_swarm2


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


