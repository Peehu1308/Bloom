import pandas as pd
import os

# --- File paths ---
input_csv = "client/public/temperature/tnn_annual.csv"
output_csv = "client/public/temperature/tnn_annual_clean.csv"
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

# --- Load CSV ---
df = pd.read_csv(input_csv)

# --- Drop rows where 'tnn' is NaN ---
df_clean = df.dropna(subset=['tnn']).reset_index(drop=True)

# --- Show how many rows remain ---
print(f"Rows before cleaning: {len(df)}")
print(f"Rows after dropping NaN: {len(df_clean)}")

# --- Save cleaned CSV ---
df_clean.to_csv(output_csv, index=False)
print(f"✅ Cleaned TNn CSV saved: {output_csv}")

# --- Optional: preview first few rows ---
print(df_clean.head(10))
