import pandas as pd
from datasets import load_dataset

ds = load_dataset("ba188/inaturalist")
train_df = ds["train"].to_pandas()
test_df  = ds["test"].to_pandas()

train_plants = train_df[train_df['taxon'].str.strip().str.lower() == "plantae"]
test_plants  = test_df[test_df['taxon'].str.strip().str.lower() == "plantae"]


train_plants.to_json("train_plants.json", orient="records")
test_plants.to_json("test_plants.json", orient="records")
