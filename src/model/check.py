import pandas as pd

# Load CSV
df = pd.read_csv("client/public/temperature/tnn_annual.csv")

# Check column names
print("Columns in CSV:")
print(df.columns)

# Show first 10 rows
print("\nFirst 10 rows:")
print(df.head(10))

# Show last 10 rows
print("\nLast 10 rows:")
print(df.tail(10))

# Show random 10 rows to check data spread
print("\nRandom sample 10 rows:")
print(df.sample(10))

# Quick info and data types
print("\nDataFrame info:")
print(df.info())

# Basic statistics
print("\nDescriptive stats:")
print(df.describe())
