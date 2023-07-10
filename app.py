import pandas as pd
from flask import Flask, render_template, request, send_file, jsonify
import data_vis
from flask_cors import CORS

app = Flask(__name__, static_url_path='/static')
CORS(app)

@app.route('/')
def index():
    return jsonify({'message': 'Hello from the backend!'})

@app.route('/process-datavis', methods=['POST'])
def process_datavis():
    global_sheet = request.files['fileInput']
    data_vis.visualization(global_sheet)
    return jsonify({'message': 'Data visualization processed successfully'})

@app.route('/process-files', methods=['POST'])
def process_files():
    file1 = request.files['globalfile']
    file2 = request.files['patientfile']
    name = request.form['username']
    xls_patient = pd.ExcelFile(file2)
    df = pd.read_excel(xls_patient, "Characterization Data 2", header=[0,1]) 
    df.columns = ['.'.join(col).strip() for col in df.columns.values]
        
    TBNK_Day0_Pre = df.iloc[0:11, 1]
    TBNK_Day0_Post = df.iloc[0:11, 2]
    TBNK_Day9_Final = df.iloc[0:11, 3]
    TBNK_Day0_Pre = TBNK_Day0_Pre.to_list()
    TBNK_Day0_Post = TBNK_Day0_Post.to_list()
    TBNK_Day9_Final = TBNK_Day9_Final.to_list()
    TBNK_col = TBNK_Day0_Pre + TBNK_Day0_Post + TBNK_Day9_Final 

    MemDiff_Day0Post = (df.iloc[0:14, 5]).to_list()
    MemDiff_Day9Final = (df.iloc[0:14, 6]).to_list()
    MemDiff_col = MemDiff_Day0Post + MemDiff_Day9Final 

    exhaustion_day9 = (df.iloc[0:27, 8]).to_list()

    cytotox = (df.iloc[0:3, 10]).to_list()

    cytokine = (df.iloc[0:4, 12]).to_list()

    cell_count = (df.iloc[0:1, 14]).to_list() + (df.iloc[0:1, 15]).to_list() + (df.iloc[0:1, 16]).to_list() + (df.iloc[0:1, 17]).to_list() + (df.iloc[0:1, 18]).to_list() 

    excel_file = pd.ExcelFile(file1)
    dfs = {sheet_name: excel_file.parse(sheet_name) for sheet_name in excel_file.sheet_names}
        
    print(dfs)
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

    df_TBNK = dfs["Cell Growth plot"] 
    df_TBNK[name] = cell_count 
    
    output_file = "modified_global.xlsx"
    with pd.ExcelWriter(output_file) as writer:
        for sheet_name, df in dfs.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    return send_file(output_file, as_attachment=True), jsonify({'message': 'Data processed!'})

if __name__ == "__main__":
    app.debug = True
    app.run()
