import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from itertools import chain


def round_numerical_values(value, digits):
    if isinstance(value, (int, float)):
        return round(value, digits)
    return value

def format_sci_notation(value):
    if abs(value) >= 1e6:
        return f'{value:.1e}'
    else:
        return value


def table(dfs, col_names, xls):
    
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
    
    Bcells_fdp = (TBNK.loc[TBNK['Batch #'] == 'Final Product - B cells']).values[0][1:] # 22
    CD4_fdp = (TBNK.loc[TBNK['Batch #'] == 'Final Product - CD4+ T cells']).values[0][1:] # 24
    CD4CD8_fdp = (TBNK.loc[TBNK['Batch #'] == 'Final Product - CD4+ CD8+ T cells']).values[0][1:] # 25
    CD56CD16_fdp = (TBNK.loc[TBNK['Batch #'] == 'Final Product - CD56+ CD16+ T cells']).values[0][1:] # 26
    CD8_fdp = (TBNK.loc[TBNK['Batch #'] == 'Final Product - CD8+ T cells']).values[0][1:] # 27
    Eosinophil_fdp = (TBNK.loc[TBNK['Batch #'] == 'Final Product - Eosinophils']).values[0][1:] # 28
    Monocyte_fdp = (TBNK.loc[TBNK['Batch #'] == 'Final Product - Monocytes']).values[0][1:] # 29
    Neutrophil_fdp = (TBNK.loc[TBNK['Batch #'] == 'Final Product - Neutrophils']).values[0][1:] # 30
    NKT_fdp = (TBNK.loc[TBNK['Batch #'] == 'Final Product - NKT cells']).values[0][1:] # 31
    
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
   

    CD4CD8Ratio_Pre = (TBNK.loc[TBNK['Batch #'] == 'CD4:CD8 Ratio Pre-Enrichment']).values[0][1:] # 13
    CD4CD8Ratio_Post = (TBNK.loc[TBNK['Batch #'] == 'CD4:CD8 Ratio Post-Enrichment']).values[0][1:] # 16
    CD4CD8Ratio_fdp = (TBNK.loc[TBNK['Batch #'] == 'CD4:CD8 Ratio DP']).values[0][1:] # 16
    

    # Read the Excel file into a dictionary of DataFrames
    dfs = {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names}
    data_frame = dfs["QC Release Results Summary"]

    data_frame = data_frame[6:]
    data_frame.drop(data_frame.loc[data_frame['Unnamed: 1']=='Total Cell Count'].index, inplace=True)
    data_frame.drop(data_frame.loc[data_frame['Unnamed: 1']=='Microbial Growth (BacT ALERT)'].index, inplace=True)
    data_frame.drop(data_frame.loc[data_frame['Unnamed: 1']=='Mycoplasma DNA (MycoSeq)'].index, inplace=True)
    data_frame.drop(data_frame.tail(3).index,inplace = True)
    data_frame.drop(data_frame.loc[data_frame['Unnamed: 1']=='Dose'].index, inplace=True)
    data_frame['Batch #'] = ['Identity', 'Purity', 'Strength', 'Strength', 'DP Volume', 'Target Dose', 'Dose', 'Safety']
    data_frame['Unnamed: 1'] = ['CAR Transduction', 'CD3 Expression', 'Viable Cell Count', 'Viability (%)', 'Volume by Weight', 'Dose', 'Dose', 'VCN']
    data_frame['Unnamed: 2'] = ['≥10% CAR+ Cells', '≥80% CD3+ Cells', 'N/A', '≥70% Viability', 'N/A', '1E8 or 0.5E8 Viable CAR+ Cells', 'KYV-001: 75-125% of Target Dose KYV-003: 70-130% of Target Dose      IH: Report Result', '≤5 Copies/Transduced Cell']
    data_frame.reset_index(inplace=True, drop=True)
    data_frame.drop(['Unnamed: 3'], axis=1, inplace=True)
    l = ["Attribute", "Measurement", "Specification"]
    l.extend(col_names)
    df = data_frame

    names_v2 = list(data_frame.columns.values.tolist())
    names_v2 = names_v2[3:]
    for name in names_v2:
        df[name] = df[name].apply(round_numerical_values, digits=2)
    print(df)
    print(df.iloc[:, 4:])
    print(df.iloc[[2, 5, 6], 3:])
    df.iloc[6,:] = df.iloc[6,:].apply(round_numerical_values, digits=0)
    df["Median"] = df.iloc[:, 3:].median(axis=1)
    list_min = df.iloc[:, 3:].min(axis=1)
    list_max = df.iloc[:, 3:].max(axis=1)
    df.iloc[[2, 5, 6], 3:] = df.iloc[[2, 5, 6], 3:].applymap(format_sci_notation)
    print(list_min)
    list_min = list_min.astype(int)
    list_max = list_max.astype(int)
    list_min = list_min.apply(format_sci_notation).apply(round_numerical_values, digits=0)
    list_max = list_max.apply(format_sci_notation).apply(round_numerical_values, digits=0)
    df["Range"] = list_min.astype(str) + " - " + list_max.astype(str)
    l_new = ["Median", "Range"]



    df["colors"] = ['lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightgreen', 'lightgreen', 'lightgreen', 'lightyellow']
    l.extend(l_new)
    fig = go.Figure()
    fig.add_trace(
    go.Table(
        header=dict(
            values=l,
            font=dict(size=12),
            line_color='darkslategray',
            fill_color='lightgrey',
            align="center"
        ),
        cells=dict(
            values=[df[k].tolist() for k in df.columns[0:-1]],
            font=dict(size=10),
            line_color='darkslategray',
            fill_color=[df.colors],
            align = "center")
    )
    )




    fig.update_layout(
    autosize=True,       # Automatically adjust the table size to fit the content
    width=1450,           # Set the width of the table (adjust as needed)
    height=1000,          # Set the height of the table (adjust as needed)
   # margin=dict(l=10, r=10, t=10, b=10)  # Set margins to provide spacing
    )
    fig.show()

    tbnk_vals = ({
    'Cell Type':["CD4+ Post Temra","CD4+ FDP Temra", "CD4+ Post Tem", "CD4+ FDP Tem", "CD4+ Post Tcm", "CD4+ FDP Tcm", "CD4+ Post Tscm", "CD4+ FDP Tscm", "CD4+ Post Tn", "CD4+ FDP Tn", "CD8+ Post Temra", "CD8+ FDP Temra",
            "CD8+ Post Tem", "CD8+ FDP Tem",
            "CD8+ Post Tcm", "CD8+ FDP Tcm",
            "CD8+ Post Tscm", "CD8+ FDP Tscm",
            "CD8+ Post Tn", "CD8+ FDP Tn"]})
    
    for i in range(len(col_names)):
        tbnk_vals[col_names[i]] = [CD4_Post_Temra[i], CD4_FDP_Temra[i], CD4_Post_Tem[i], CD4_FDP_Tem[i], CD4_Post_Tcm[i], CD4_FDP_Tcm[i], CD4_Post_Tscm[i], CD4_FDP_Tscm[i], CD4_Post_Tn[i], CD4_FDP_Tn[i], CD8_Post_Temra[i], CD8_FDP_Temra[i], CD8_Post_Tem[i], CD8_FDP_Tem[i], CD8_Post_Tcm[i], CD8_FDP_Tcm[i], CD8_Post_Tscm[i], CD8_FDP_Tscm[i], CD8_Post_Tn[i], CD8_FDP_Tn[i]]
        print(tbnk_vals[col_names[i]])
    print(tbnk_vals)
    df = pd.DataFrame(tbnk_vals)
    print(df)
    tbnk_table_titles = ["Cell Types"]
    tbnk_table_titles.extend(col_names)
    last = ["Median", "Range"]
    tbnk_table_titles.extend(last)

    df["Median"] = df.iloc[:, 1:].median(axis=1)
    df["Median"] =  df["Median"].round(2)

    list_min = (df.iloc[:, 1:].min(axis=1)).round(2)
    list_max = (df.iloc[:, 1:].max(axis=1)).round(2)
    df["Range"] = list_min.astype(str) + "-" + list_max.astype(str)

    df["colors"] = ['aliceblue', 'aliceblue', 'antiquewhite', 'antiquewhite', 'aqua', 'aqua', 'aquamarine', 'aquamarine', 'azure', 'azure', 'aliceblue', 'aliceblue', 'antiquewhite', 'antiquewhite', 'aqua', 'aqua', 'aquamarine', 'aquamarine', 'azure', 'azure']
    
    for name in col_names:
        df[name] = df[name].round(2)

    fig_tbnk_table = go.Figure()
    fig_tbnk_table.add_trace(
    go.Table(
        header=dict(
            values=tbnk_table_titles,
            font=dict(size=14),
            align="center"
        ),
        cells=dict(
            values=[df[k].tolist() for k in df.columns[0:-1]],
            line_color='darkslategray', fill_color=[df.colors],
            align = "center")
    )
    )
    fig_tbnk_table.update_layout(
    autosize=True,       # Automatically adjust the table size to fit the content
   #width=1000,           # Set the width of the table (adjust as needed)
  #  height=600,          # Set the height of the table (adjust as needed)
    #margin=dict(l=10, r=10, t=10, b=10)  # Set margins to provide spacing
)
    

    table_vals = ({
    'Cell Type':["CD4+ T Cells Aph","CD4+ T Cells Post", "CD4+ T Cells FP", 
                 "CD4+CD8+ T Cells Aph","CD4+CD8+ T Cells Post", "CD4+CD8+ T Cells FP",
                 "CD8+ T Cells Aph","CD8+ T Cells Post", "CD8+ T Cells FP",
                 "NKT Cells Aph","NKT Cells Post", "NKT Cells FP",
                 "B Cells Aph","B Cells Post", "B Cells FP",
                 "Eosinophils Aph","Eosinophils Post", "Eosinophils FP",
                 "Monocytes Aph","Monocytes Post", "Monocytes FP",
                 "Neutrophils Aph","Neutrophils Post", "Neutrophils FP",
                 "CD56+CD16+ cells Aph","CD56+CD16+ cells Post", "CD56+CD16+ cells FP",
                 "CD4/CD8 Ratio Aph","CD4/CD8 Ratio Post", "CD4/CD8 Ratio FP", 
                 ]})
    
    for i in range(len(col_names)):
        table_vals[col_names[i]] = [CD4_Pre[i], CD4_Post[i], CD4_fdp[i], CD4CD8_Pre[i], CD4CD8_Post[i], CD4CD8_fdp[i], CD8_Pre[i], CD8_Post[i], CD8_fdp[i], NKT_Pre[i], NKT_Post[i], NKT_fdp[i], Bcells_Pre[i], Bcells_Post[i], Bcells_fdp[i], Eosinophil_Pre[i], Eosinophil_Post[i], Eosinophil_fdp[i], Monocyte_Pre[i], Monocyte_Post[i], Monocyte_fdp[i], Neutrophil_Pre[i], Neutrophil_Post[i], Neutrophil_fdp[i], CD56CD16_Pre[i], CD56CD16_Post[i], CD56CD16_fdp[i], CD4CD8Ratio_Pre[i], CD4CD8Ratio_Post[i], CD4CD8Ratio_fdp[i]]


    df = pd.DataFrame(table_vals)
    print(df)
    table_titles = ["Cell Types"]
    table_titles.extend(col_names)
    last = ["Median", "Range"]
    table_titles.extend(last)

    df["Median"] = df.iloc[:, 1:].median(axis=1)
    df["Median"] =  df["Median"].round(2)

    list_min = (df.iloc[:, 1:].min(axis=1)).round(2)
    list_max = (df.iloc[:, 1:].max(axis=1)).round(2)
    df["Range"] = list_min.astype(str) + "-" + list_max.astype(str)

    df["colors"] = ['aliceblue', 'aliceblue', 'aliceblue', 'antiquewhite', 'antiquewhite', 'antiquewhite', 'aqua', 'aqua',  'aqua', 'aquamarine', 'aquamarine', 'aquamarine', 'azure', 'azure', 'azure', 'lightpink', 'lightpink', 'lightpink',  'cornflowerblue', 'cornflowerblue', 'cornflowerblue', 'cyan', 'cyan', 'cyan', 'floralwhite', 'floralwhite', 'floralwhite', 'pink', 'pink', 'pink']
    
    for name in col_names:
        df[name] = df[name].round(2)

    fig_table3 = go.Figure()
    fig_table3.add_trace(
    go.Table(
        header=dict(
            values=table_titles,
            font=dict(size=14),
            align="center"
        ),
        cells=dict(
            values=[df[k].tolist() for k in df.columns[0:-1]],
            line_color='darkslategray', fill_color=[df.colors],
            align = "center")
    )
    )


    fig_table3.update_layout(
    autosize=True,       # Automatically adjust the table size to fit the content
   #width=1000,           # Set the width of the table (adjust as needed)
    height=1000,          # Set the height of the table (adjust as needed)
    #margin=dict(l=10, r=10, t=10, b=10)  # Set margins to provide spacing
    )



    cd4cd8_ratios = ({
    'Material':["Apheresis", "Post Enrichment", "FDP"]})
    
    for i in range(len(col_names)):
        cd4cd8_ratios[col_names[i]] = [CD4CD8Ratio_Pre[i], CD4CD8Ratio_Post[i], CD4CD8Ratio_fdp[i]]
    print(tbnk_vals)
    df = pd.DataFrame(cd4cd8_ratios)
    print(df)
    tbnk_table_titles = ["Material"]
    tbnk_table_titles.extend(col_names)
    last = ["Median", "Range"]
    tbnk_table_titles.extend(last)


    df["Median"] = df.iloc[:, 1:].median(axis=1)
    df["Median"] =  df["Median"].round(1)

    list_min = (df.iloc[:, 1:].min(axis=1)).round(1)
    list_max = (df.iloc[:, 1:].max(axis=1)).round(1)
    df["Range"] = list_min.astype(str) + "-" + list_max.astype(str)

    df["colors"] = ['lightgreen', 'powderblue', 'lightgreen']

    for name in col_names:
        df[name] = df[name].round(1)

    fig_tbnk_table2 = go.Figure()
    fig_tbnk_table2.add_trace(
    go.Table(
        header=dict(
            values=tbnk_table_titles,
            font=dict(size=14),
            align="center"
        ),
        cells=dict(
            values=[df[k].tolist() for k in df.columns[0:-1]],
            line_color='darkslategray', fill_color=[df.colors],
            align = "center")
    )
    )
    fig_tbnk_table2.update_layout(
    autosize=True,       # Automatically adjust the table size to fit the content
   #width=1000,           # Set the width of the table (adjust as needed)
  #  height=600,          # Set the height of the table (adjust as needed)
    #margin=dict(l=10, r=10, t=10, b=10)  # Set margins to provide spacing
)

    fig_tbnk_table2.update_layout(
    title={
        'text': "CD4:CD8 Ratio",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 18,'color': 'blue'}, 'x': 0.5
        })
    
    
    fig_tbnk_table2.show()
    
    cytokine = dfs["Cytokine"]
    CD19P_5_1 = (cytokine.loc[cytokine['Batch #'] == 'IFNg 5:1 (CD19+) (pg/mL) E:T Ratio']).values[0].tolist()[1:] 
    CD19P_10_1 = (cytokine.loc[cytokine['Batch #'] == 'IFNg 10:1 (CD19+) (pg/mL) E:T Ratio']).values[0].tolist()[1:]
  
    cytotox = dfs["Cytotox"]
    one_to_one = (cytotox.loc[cytotox['Batch #'] == '1:1 (CD19+) E:T'].values[0][1:])
    five_to_one = (cytotox.loc[cytotox['Batch #'] == '5:1 (CD19+) E:T'].values[0][1:])
    ten_to_one = (cytotox.loc[cytotox['Batch #'] == '10:1 (CD19+) E:T'].values[0][1:])


    release_table = ({
    'Attribute':["TBNK", "Memory Phenotype (CD4+\CAR+ T cells)", "Memory Phenotype (CD4+\CAR+ T cells)", "Memory Phenotype (CD4+\CAR+ T cells)", "Memory Phenotype (CD4+\CAR+ T cells)", "Memory Phenotype (CD4+\CAR+ T cells)", "Memory Phenotype (CD8+\CAR+ T cells)",  "Memory Phenotype (CD8+\CAR+ T cells)",  "Memory Phenotype (CD8+\CAR+ T cells)", "Memory Phenotype (CD8+\CAR+ T cells)", "Memory Phenotype (CD8+\CAR+ T cells)", "Exhaustion (CAR+\CD4+ T cells)", "Exhaustion (CAR+\CD8+ T cells)", "Potency (IFNγ)", "Potency (IFNγ)", "Potency (Cytotoxicity)", "Potency (Cytotoxicity)", "Potency (Cytotoxicity)", "Leukocyte Content (TBNK)", "Leukocyte Content (TBNK)", "Leukocyte Content (TBNK)", "Leukocyte Content (TBNK)", "Leukocyte Content (TBNK)", "Leukocyte Content (TBNK)", "Leukocyte Content (TBNK)", "Leukocyte Content (TBNK)", "Leukocyte Content (TBNK)"],
    'Measurement': ['CD4:CD8 Ratio', 'Tn (%)', 'Tscm (%)', 'Tcm (%)', 'Tem (%)', 'Temra (%)', 'Tn (%)', 'Tscm (%)', 'Tcm (%)', 'Tem (%)', 'Temra (%)', 'PD1+\Tim3+LAG3+ cells (%)', 'PD1+\Tim3+LAG3+ cells (%)', 'IFNγ (pg/mL) 5:1 E:T (CD19+)', 'IFNγ (pg/mL) 10:1 E:T (CD19+)', 'Cytotoxicity (%) at 1:1 E:T (CD19+)', 'Cytotoxicity (%) at 5:1 E:T (CD19+)', 'Cytotoxicity (%) at 10:1 E:T (CD19+)', 'CD4+ T cells (%)', 'CD4+CD8+ T cells (%)', 'CD8+ T cells (%)', 'NKT cells (%)', 'B cells (%)', 'Eosinophils (%)', 'Monocytes (%)', 'Neutrophils (%)', 'CD56+CD16+ cells (%)'] 
    })

    exhaustion = dfs["Exhaustion"]
    exhaustion_1 = (exhaustion.loc[exhaustion['Batch #'] == '%Exhausted (Viable CD3+\CAR+\CD4+\CD279+\CD223+CD366+)'].values[0][1:])
    exhaustion_2 = (exhaustion.loc[exhaustion['Batch #'] == '%Exhausted (Viable CD3+\CAR+\CD8+\CD279+\CD223+CD366+)'].values[0][1:])



    for i in range(len(col_names)):
        release_table[col_names[i]] = [CD4CD8Ratio_fdp[i], CD4_FDP_Tn[i], CD4_FDP_Tscm[i], CD4_FDP_Tcm[i], CD4_FDP_Tem[i], CD4_FDP_Temra[i], CD8_FDP_Tn[i], CD8_FDP_Tscm[i], CD8_FDP_Tcm[i], CD8_FDP_Tem[i], CD8_FDP_Temra[i], exhaustion_1[i], exhaustion_2[i], CD19P_5_1[i], CD19P_10_1[i], one_to_one[i], five_to_one[i], ten_to_one[i], CD4_fdp[i], CD4CD8_fdp[i], CD8_fdp[i], NKT_fdp[i], Bcells_fdp[i], Eosinophil_fdp[i], Monocyte_fdp[i], Neutrophil_fdp[i], CD56CD16_fdp[i]]
    print(tbnk_vals)

    df = pd.DataFrame(release_table)
    print(df)
    tbnk_table_titles = ["Attribute", "Measurement"]
    tbnk_table_titles.extend(col_names)
    last = ["Median", "Range"]
    tbnk_table_titles.extend(last)


    df["Median"] = df.iloc[:, 2:].median(axis=1)
    df["Median"] =  df["Median"].round(1)

    list_min = (df.iloc[:, 2:].min(axis=1)).round(1)
    list_max = (df.iloc[:, 2:].max(axis=1)).round(1)
    df["Range"] = list_min.astype(str) + "-" + list_max.astype(str)


    for name in col_names:
        df[name] = df[name].round(1)


    df["colors"] = ['lavender', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue', 'peachpuff', 'peachpuff', 'lightyellow', 'lightyellow', 'tomato', 'tomato', 'tomato', 'violet', 'violet', 'violet', 'violet', 'violet', 'violet', 'violet', 'violet', 'violet'  ]
    fig_rel = go.Figure()
    fig_rel.add_trace(
    go.Table(
        header=dict(
            values=tbnk_table_titles,
            font=dict(size=14),
            align="center"
        ),
        cells=dict(
            values=[df[k].tolist() for k in df.columns[0:-1]],
            line_color='grey', fill_color=[df.colors],
            align = "center")
    )
    )
    fig_rel.update_layout(
    autosize=True,       # Automatically adjust the table size to fit the content
   #width=1000,           # Set the width of the table (adjust as needed)
    height=3000,          # Set the height of the table (adjust as needed)
    #margin=dict(l=10, r=10, t=10, b=10)  # Set margins to provide spacing
    )


    
    
    fig_rel.show()







    return fig, fig_tbnk_table, fig_table3, fig_tbnk_table2, fig_rel
    