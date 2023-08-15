import pandas as pd


def test():
    xls = pd.ExcelFile("/Users/lseyahi/Desktop/glo.xlsx")
   # print(xls)
    # Read the Excel file into a dictionary of DataFrames
    dfs = {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names}
    data_frame = dfs["QC Release Results Summary"] 
    print(data_frame)
    col_names = list(data_frame.columns.values[4:].tolist())

    #row 10 is %CAR of final DP = CAR Transduction 
    row_list = (data_frame.loc[6, :].values.tolist())[4:]
    print(row_list)

    #purity
    purity = (data_frame.loc[7, :].values.tolist())[4:]
    print(purity)

    #vcn
    vcn = (data_frame.loc[17, :].values.tolist())[4:]
    print(vcn)

    #viability % viable cells
    via = (data_frame.loc[8, :].values.tolist())[4:]
    print(via)

    #actual dose 
    dose = (data_frame.loc[12, :].values.tolist())[4:]
    print(dose)
    
    ip_data_frame = dfs["In Process Data Summary"]
    print(ip_data_frame)
    print(ip_data_frame.loc[0, :].values.tolist())





if __name__ == "__main__":
    test()