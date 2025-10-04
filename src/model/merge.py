import pandas as pd
import os

# --- File paths ---
files = {
    "frost_days": "client/public/temperature/frost_days_annual.csv",
    "ice_days": "client/public/temperature/id_annual.csv",
    "tg": "client/public/temperature/tg_annual_clean.csv",
    "tn": "client/public/temperature/tn_annual_clean.csv",
    "tnn": "client/public/temperature/tnn_annual_clean.csv"
}

# --- Load CSVs ---
print("Loading CSV files...")
fd = pd.read_csv(files["frost_days"])
id = pd.read_csv(files["ice_days"])
tg = pd.read_csv(files["tg"])
tn = pd.read_csv(files["tn"])
tnn = pd.read_csv(files["tnn"])

# --- Merge all datasets on ['year','lat','lon'] ---
print("Merging datasets...")
df = fd.merge(id, on=['year','lat','lon'], how='outer') \
       .merge(tg, on=['year','lat','lon'], how='outer') \
       .merge(tn, on=['year','lat','lon'], how='outer') \
       .merge(tnn, on=['year','lat','lon'], how='outer')

# --- Optional: check for remaining NaNs ---
print("Missing values per column:")
print(df.isna().sum())


df_land = df.dropna(subset=['tg', 'tn', 'tnn']).reset_index(drop=True)
print(f"Rows after filtering land points: {len(df_land)}")


output_csv = "client/public/temperature/bloomwatch_land.csv"
df_land.to_csv(output_csv, index=False)
print(f"✅ Land-only merged CSV saved: {output_csv}")

os.makedirs(os.path.dirname(output_csv), exist_ok=True)
df.to_csv(output_csv, index=False)
print(f"✅ Merged CSV saved: {output_csv}")
