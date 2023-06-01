import pandas as pd
from langdetect import detect

print(detect("War doesn't show who's right, just who's left."))

df_data = pd.read_csv('playground/data_short2.csv', encoding='latin-1', header=None)

for i in range(0, len(df_data.index)):
    df_data['lang'] = detect(df_data[5][i])

print(df_data.head())