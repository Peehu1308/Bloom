import pandas as pd

df = pd.read_csv("client/public/temperature/id_annual.csv")
print(df.head())
print(df.describe())
print(df['year'].unique())  # check all years
