import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px


# Page 1 - Release Graphs
def release_graphs(dfs, col_names):
    data_frame = dfs["QC Release Results Summary"]

    #%CAR
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
    
    #std and mean calc
    multiplied_list = row_list
    print(multiplied_list)
    y_mean = np.nanmean(multiplied_list)
    std = np.nanstd(multiplied_list)
    two_plussd = y_mean + 2*std
    two_minussd = y_mean - 2*std

   # fig = px.scatter(y=multiplied_list, x=col_names, range_y = [0,100], labels={'y':'%CAR+ Cells'}, title="Identity and Potency (%CAR+ Cells)")
   # fig.add_trace(go.Scatter(x=col_names, y=[y_mean] * len(col_names), mode='lines', name='Mean'))
   # fig.add_trace(go.Scatter(x=col_names, y=[two_plussd] * len(col_names), mode='lines', name='+2SD'))
   # fig.add_trace(go.Scatter(x=col_names, y=[two_minussd] * len(col_names), mode='lines', name='-2SD'))
   # fig.update_traces(marker_size=10)

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


    # mode = markers removes the connecting lines 

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

    fig_sub_1.append_trace(go.Bar(x=col_names, y=pt_dose, marker_color=colors_bub, showlegend=False), row=2, col=3)

    fig_sub_1.update_yaxes(title_text="%CAR+ Cells", range=[0, 100], row=1, col=1)
    fig_sub_1.update_yaxes(title_text="%CD3+ Cells", range=[75, 100] , row=1, col=2)
    fig_sub_1.update_yaxes(title_text="VCN", range=[0, 5], row=1, col=3)
    fig_sub_1.update_yaxes(title_text="Viable Cells (%)", range=[70, 100], row=2, col=1)
    fig_sub_1.update_yaxes(title_text="Actual Dose", range=[0, 1.5 * 10**8] , row=2, col=2)
    fig_sub_1.update_yaxes(title_text="Target Dose(%)", row=2, col=3)
    fig_sub_1.update_layout(title={'text': "Release Data", 'font': {'size': 24,'color': 'blue'}, 'x': 0.5})

    return fig_sub_1


# Page 4 - Graph for %CAR+ D8 and D9 
def day8_day9_graph(dfs, col_names):
    #%CAR
    data_frame = dfs["QC Release Results Summary"]
    row_list = data_frame[data_frame['Unnamed: 1'] == 'CAR Transduction'].values[0].tolist()
    row_list = row_list[4:]
    multiplied_list = row_list
    process = dfs['In Process Data Summary']
    row_list_2 = process.loc[process['Batch #'] == 'Harvest -1Day CAR%'].values[0].tolist()[1:]
    multiplied_list_2 = row_list_2

    fig_2 = go.Figure()
    x_axis = ["Day 8", "Day 9"]
    for i in range(len(col_names)):
        list_ = [multiplied_list_2[i], multiplied_list[i]]
        fig_2.add_trace(go.Scatter(x=x_axis, y=list_, name=col_names[i]))
    fig_2.update_layout(title={'text': "%CAR+ Cells (Day 8 and Day 9)",'font': {'size': 24,'color': 'blue'}, 'x': 0.5 })  # Set the title's x position to the center
    return fig_2




