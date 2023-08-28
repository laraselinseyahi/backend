import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from itertools import chain



def memdiff(dfs, col_names):
    
    MemDiff = dfs["Mem-Diff"]

    CD8_FDP_Tem = (MemDiff.loc[MemDiff['Batch #'] == 'Final Product - CD3+\CAR+\CD8+\Tem'].values[0][1:]) # 17
    CD8_FDP_Temra = (MemDiff.loc[MemDiff['Batch #'] == 'Final Product - CD3+\CAR+\CD8+\Temra'].values[0][1:]) # 18
    CD8_FDP_Tcm = (MemDiff.loc[MemDiff['Batch #'] == 'Final Product - CD3+\CAR+\CD8+\Tcm'].values[0][1:]) # 19
    CD8_FDP_Tscm = (MemDiff.loc[MemDiff['Batch #'] == 'Final Product - CD3+\CAR+\CD8+\Tscm'].values[0][1:]) # 20
    CD8_FDP_Tn = (MemDiff.loc[MemDiff['Batch #'] == 'Final Product - CD3+\CAR+\CD8+\Tn'].values[0][1:]) # 21

    CD4_FDP_Tem = (MemDiff.loc[MemDiff['Batch #'] == 'Final Product - CD3+\CAR+\CD4+\Tem'].values[0][1:])
    CD4_FDP_Temra = (MemDiff.loc[MemDiff['Batch #'] == 'Final Product - CD3+\CAR+\CD4+\Temra'].values[0][1:])
    CD4_FDP_Tcm = (MemDiff.loc[MemDiff['Batch #'] == 'Final Product - CD3+\CAR+\CD4+\Tcm'].values[0][1:])
    CD4_FDP_Tscm = (MemDiff.loc[MemDiff['Batch #'] == 'Final Product - CD3+\CAR+\CD4+\Tscm'].values[0][1:])
    CD4_FDP_Tn = (MemDiff.loc[MemDiff['Batch #'] == 'Final Product - CD3+\CAR+\CD4+\Tn'].values[0][1:])

    CD4_Post_Tem = (MemDiff.loc[MemDiff['Batch #'] == 'Day 0 Post-Enrichment - CD3+\CD4+\Tem'].values[0][1:])
    CD4_Post_Temra = (MemDiff.loc[MemDiff['Batch #'] == 'Day 0 Post-Enrichment - CD3+\CD4+\Temra'].values[0][1:])
    CD4_Post_Tcm = (MemDiff.loc[MemDiff['Batch #'] == 'Day 0 Post-Enrichment - CD3+\CD4+\Tcm'].values[0][1:])
    CD4_Post_Tscm = (MemDiff.loc[MemDiff['Batch #'] == 'Day 0 Post-Enrichment - CD3+\CD4+\Tscm'].values[0][1:])
    CD4_Post_Tn = (MemDiff.loc[MemDiff['Batch #'] == 'Day 0 Post-Enrichment - CD3+\CD4+\Tn'].values[0][1:])

    CD8_Post_Tem = (MemDiff.loc[MemDiff['Batch #'] == 'Day 0 Post-Enrichment - CD3+\CD8+\Tem'].values[0][1:])
    CD8_Post_Temra = (MemDiff.loc[MemDiff['Batch #'] == 'Day 0 Post-Enrichment - CD3+\CD8+\Temra'].values[0][1:])
    CD8_Post_Tcm = (MemDiff.loc[MemDiff['Batch #'] == 'Day 0 Post-Enrichment - CD3+\CD8+\Tcm'].values[0][1:])
    CD8_Post_Tscm = (MemDiff.loc[MemDiff['Batch #'] == 'Day 0 Post-Enrichment - CD3+\CD8+\Tscm'].values[0][1:])
    CD8_Post_Tn = (MemDiff.loc[MemDiff['Batch #'] == 'Day 0 Post-Enrichment - CD3+\CD8+\Tn'].values[0][1:])

    #memdiff swarm plots - Page 10
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

    #memdiff swarm plots - Page 11, 12
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

    #MemDiff bar graphs - Page 9     
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

    fig_memdiff.update_layout(barmode="relative", title={'text': "Memory Differentiation (Post-Enrichment & FDP)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
    
    return fig_memdiff, fig_memdiff_swarm1, fig_memdiff_swarm2, fig_memdiff_swarm3

""" fig5, fig6, fig8, fig9 are unused in the current dashboard 

    fig_5 = go.Figure(data=[
        go.Bar(name='Tem', x=col_names, y=CD8_FDP_Tem),
        go.Bar(name='Temra', x=col_names, y=CD8_FDP_Temra),
        go.Bar(name='Tcm', x=col_names, y=CD8_FDP_Tcm),
        go.Bar(name='Tscm', x=col_names, y=CD8_FDP_Tscm),
        go.Bar(name='Tn', x=col_names, y=CD8_FDP_Tn)
    ])
    fig_5.update_layout(barmode='stack', title={'text': "Memory Differentiation %CD8+ Cells (FDP)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})

    fig_6 = go.Figure(data=[
        go.Bar(name='Tem', x=col_names, y=CD4_FDP_Tem),
        go.Bar(name='Temra', x=col_names, y=CD4_FDP_Temra),
        go.Bar(name='Tcm', x=col_names, y=CD4_FDP_Tcm),
        go.Bar(name='Tscm', x=col_names, y=CD4_FDP_Tscm),
        go.Bar(name='Tn', x=col_names, y=CD4_FDP_Tn)
    ])
    fig_6.update_layout(barmode='stack', title={'text': "Memory Differentiation %CD4+ Cells (FDP)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})

    fig_7 = go.Figure(data=[
        go.Bar(name='Tem', x=col_names, y=CD4_Post_Tem),
        go.Bar(name='Temra', x=col_names, y=CD4_Post_Temra),
        go.Bar(name='Tcm', x=col_names, y=CD4_Post_Tcm),
        go.Bar(name='Tscm', x=col_names, y=CD4_Post_Tscm),
        go.Bar(name='Tn', x=col_names, y=CD4_Post_Tn)
    ])
    fig_7.update_layout(barmode='stack', title={'text': "Memory Differentiation %CD4+ Cells (Post Enrichment)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})

    fig_8 = go.Figure(data=[
        go.Bar(name='Tem', x=col_names, y=CD8_Post_Tem),
        go.Bar(name='Temra', x=col_names, y=CD8_Post_Temra),
        go.Bar(name='Tcm', x=col_names, y=CD8_Post_Tcm),
        go.Bar(name='Tscm', x=col_names, y=CD8_Post_Tscm),
        go.Bar(name='Tn', x=col_names, y=CD8_Post_Tn)
    ])
    fig_8.update_layout(barmode='stack', title={'text': "Memory Differentiation %CD8+ Cells (Post Enrichment)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})

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
"""