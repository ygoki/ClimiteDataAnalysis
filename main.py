import pandas as pd
import matplotlib.pyplot as plt

import csvedit

def analysis(climite_data_path, city_name):
    def filter_complete_years_with_january_start(df):
        grouped = df.groupby('Year')['Month'].apply(list).reset_index()
        valid_years = grouped[
            grouped['Month'].apply(lambda months: months[0] == 1 and len(months) == 12 and set(months) == set(range(1,13)))
        ]['Year']

        return df[df['Year'].isin(valid_years)]
    
    data = pd.read_csv(climite_data_path)
    #data = data.dropna()
    data['Date'] = pd.to_datetime(data['Date'], format='%Y/%m')
    data['Year'] = data['Date'].dt.year
    data['Month'] = data['Date'].dt.month

    filtered_data = data[data['Quality'].isin([5,8])]
    filtered_data = filter_complete_years_with_january_start(filtered_data)

    # filtered_data.loc[:,'Year'] = filtered_data['Date'].dt.year
    yearly_avg_temp = filtered_data.groupby('Year')['Avg_Temp'].mean()

    plt.figure(figsize=(10,6))
    plt.plot(yearly_avg_temp.index, yearly_avg_temp.values, marker='o', color='b', label='Yearly Avg Temp')
    plt.title('Yearly Average Temperature (Quality:5 or 8) at '+city_name, fontsize=16)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Average Temp (℃)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

print('都市名を入力')
city_name = input().capitalize()
csvedit.csvedit()
analysis('./CsvData/'+city_name+'.csv', city_name)