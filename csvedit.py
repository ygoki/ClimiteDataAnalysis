import os
import pandas as pd

def csvedit():
    directory_path = './CsvData/'
    csv_files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]

    for file_name in csv_files:
        file_path = os.path.join(directory_path,file_name)
        try:
            data = pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding='shift_jis', header=None, skiprows=2)
            df = df[df[0].notna()]
            df = df[~df[0].str.contains("年月|品質情報", na=False)]
            df.columns  = ['Date', 'Avg_Temp', 'Quality', '均質番号']
            df.to_csv(file_path, index=False)
            print("CSVデータを書き換えました。:" + file_name)