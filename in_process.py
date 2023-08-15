import pandas as pd 

def in_process_play():
    xls = pd.ExcelFile('/Users/lseyahi/desktop/glo.xlsx')

    # Read the Excel file into a dictionary of DataFrames
    dfs = {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names}

    data_frame = dfs['In Process Data Summary'] 
    list = data_frame['Batch #'].tolist()
    # print(list.index('Diluted Apheresis Viability (%)'))
    row = data_frame.loc[data_frame['Batch #'] == 'Harvest -1Day CAR%']
    # print(row)
    tbnk = dfs['TBNK']
    # print(tbnk)

    df = dfs['QC Release Results Summary']
    df = dfs['Cytotox']
    # print(df)
    release = dfs["QC Release Results Summary"]
    release_values = release['Unnamed: 1'].tolist()
   # print(release_values)
    cg_fdp = release_values.index('Viability')
  #  print(cg_fdp)
    cell_growth_fdp = (release.loc[release['Unnamed: 1'] == 'Viability'])[4:]

    xls_patient = pd.ExcelFile('/Users/lseyahi/desktop/patient.xlsx')
   # df = pd.read_excel(xls_patient, "In Process Data", header=[0]) 
   # print(df.iloc[[5]])
    #df.columns = ['.'.join(col).strip() for col in df.columns.values]
   # df = pd.read_excel(xls_patient, "General Information") 
  #  print(df['Value:'])
   # df_2 = pd.read_excel(xls_patient, "Date Tracking") 
  #  print(df_2)

    #student = pd.read_csv('/Users/lseyahi/desktop/turkish_data_ips.csv')
    #print(student)
    #print(student.count())
    #df = student.count()
    #print(df)
    # df.to_csv('nann')
   # list = ['2', '4']
   # list_2 = list + [None] + list
    
   # df = pd.read_excel(xls_patient, "In Process Data") 
    #print(df)
  
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
    input = [column[sub_id], column[don_id], column[cell_num], column[d0_title], column[aph_vol], column[aph_inc_vol], column[aph_vcc], column[aph_via], column[aph_tvc], column[aph_rec], column[aph_remv]]
    print(input)




if __name__ == "__main__":
    in_process_play()


