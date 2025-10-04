import pandas as pd

df = pd.read_csv("client/src/data/bloomwatch_land.csv")
df.to_json("client/src/data/bloomwatch_land.json", orient="records")
