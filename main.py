import pandas as pd
import matplotlib.pyplot as plt

import csvedit


def filter_complete_years_with_january_start(df):
    grouped = df.groupby('Year')['Month'].apply(list).reset_index()
    valid_years = grouped[
        grouped['Month'].apply(lambda months: months[0] == 1 and len(months) == 12 and set(months) == set(range(1,13)))
    ]['Year']
    return df[df['Year'].isin(valid_years)]

        
def analyze_cities(city_names, directory_path='./CsvData'):
    colors=['b', 'g', 'r', 'c', 'm', 'y', 'k']
    plt.figure(figsize=(14,6))
    if not isinstance(city_names, list):
        city_names = [city_names]

    for idx, city_name in enumerate(city_names):
        try:
            climite_data_path=f'{directory_path}/{city_name}.csv'
            data = pd.read_csv(climite_data_path)
            #data = data.dropna()
            data['Date'] = pd.to_datetime(data['Date'], format='%Y/%m')
            data['Year'] = data['Date'].dt.year
            data['Month'] = data['Date'].dt.month

            filtered_data = data[data['Quality'].isin([5,8])]
            filtered_data = filter_complete_years_with_january_start(filtered_data)

            # filtered_data.loc[:,'Year'] = filtered_data['Date'].dt.year
            yearly_avg_temp = filtered_data.groupby('Year')['Avg_Temp'].mean()

            color = colors[idx % len(colors)]

            city_name_capitalized=city_name.capitalize()
            plt.plot(
                yearly_avg_temp.index,
                yearly_avg_temp.values,
                marker='o',
                color=color,
                label=city_name_capitalized
            )
        except FileExistsError:
            print(f"File for city '{city_name}' not found in directory '{directory_path}'.")
        except Exception as e:
            print(f"An error cocrred for city '{city_name}':{e}")

    plt.title('Yearly Average Tempurature', fontsize=16)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Average Temp (℃)', fontsize=12)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


csvedit.csvedit()
print('都市名コンマ区切りで入力')
city_names = input().split(",")
analyze_cities([name.strip() for name in city_names])