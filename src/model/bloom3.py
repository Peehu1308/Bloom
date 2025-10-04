import pandas as pd
import os

# --- Load CSV ---
input_csv = "client/public/temperature/tg_annual.csv"
df = pd.read_csv(input_csv)

# --- Optional: drop rows with NaN in 'tg' ---
df_clean = df.dropna(subset=['tg']).reset_index(drop=True)

# --- Optional: check how many rows remain ---
print(f"Rows before cleaning: {len(df)}")
print(f"Rows after cleaning NaN: {len(df_clean)}")

# --- Save cleaned CSV ---
output_csv = "client/public/temperature/tg_annual_clean.csv"
os.makedirs(os.path.dirname(output_csv), exist_ok=True)
df_clean.to_csv(output_csv, index=False)
print(f"✅ Cleaned CSV saved: {output_csv}")

# --- Optional: preview first few rows ---
print(df_clean.head(10))
