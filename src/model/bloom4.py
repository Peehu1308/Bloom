import pandas as pd
import os

# --- Set input CSV here ---
input_csv = "client/public/temperature/tn_annual.csv"  # change this for each variable
var_name = os.path.basename(input_csv).split("_")[0]  # e.g., 'tn'

# --- Load CSV ---
df = pd.read_csv(input_csv)

# --- Optional: drop rows with NaN in main variable ---
main_col = var_name.lower()  # e.g., 'tn'
if main_col not in df.columns:
    # If the CSV has 'tn_mean', use that
    main_col = f"{main_col}_mean"

df_clean = df.dropna(subset=[main_col]).reset_index(drop=True)

# --- Check how many rows remain ---
print(f"Rows before cleaning: {len(df)}")
print(f"Rows after cleaning NaN: {len(df_clean)}")

# --- Save cleaned CSV ---
output_csv = f"client/public/temperature/{var_name}_annual_clean.csv"
os.makedirs(os.path.dirname(output_csv), exist_ok=True)
df_clean.to_csv(output_csv, index=False)
print(f"✅ Cleaned CSV saved: {output_csv}")

# --- Optional: preview first few rows ---
print(df_clean.head(10))
