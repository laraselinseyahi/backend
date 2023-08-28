import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from itertools import chain

def cytotox_cytokine(dfs, col_names):

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
    #Cytotox and Cytokine - Page 14 
    fig_cyto.update_layout(barmode='group', title={'text': "Characterization: Potency(IFNg and Cytotox)", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})
    #fig_cyto.show()

    
    fig_cytokine_swarm1 = make_subplots(rows=1, cols=2, subplot_titles=("Cytokine", "Cytotoxicity" ))

    fig_cytokine_swarm1.add_trace(go.Box(y=CD19P_5_1, name="CD19+ 5:1", showlegend=False), row=1, col=1)
    fig_cytokine_swarm1.add_trace(go.Box(y=CD19P_10_1, name="CD19+ 10:1", showlegend=False), row=1, col=1)
    fig_cytokine_swarm1.add_trace(go.Box(y=CD19M_5_1, name="CD19- 5:1", showlegend=False), row=1, col=1)
    fig_cytokine_swarm1.add_trace(go.Box(y=CD19M_10_1, name="CD19- 10:1", showlegend=False), row=1, col=1)


    fig_cytokine_swarm1.add_trace(go.Box(y=one_to_one, name="1:1", showlegend=False), row=1, col=2)
    fig_cytokine_swarm1.add_trace(go.Box(y=five_to_one, name="5:1", showlegend=False), row=1, col=2)
    fig_cytokine_swarm1.add_trace(go.Box(y=ten_to_one, name="10:1", showlegend=False), row=1, col=2)


    fig_cytokine_swarm1.update_yaxes(range=[0, 20000] , row=1, col=1)
    fig_cytokine_swarm1.update_yaxes(range=[0, 100] , row=1, col=2)


    fig_cytokine_swarm1.update_traces(boxpoints='all', jitter=0.5)
    
    return fig_cyto, fig_cytokine_swarm1