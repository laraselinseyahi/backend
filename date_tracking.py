

def date_data(dfs, col_names):
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
    