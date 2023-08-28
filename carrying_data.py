import pandas as pd
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from itertools import chain

def carry_data(df_infosheet, xls_patient, dfs, name):  
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

    # excel_file = pd.ExcelFile(file1)
    # dfs = {sheet_name: excel_file.parse(sheet_name) for sheet_name in excel_file.sheet_names}


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


    """""
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
    """