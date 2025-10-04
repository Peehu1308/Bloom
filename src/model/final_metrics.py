import pandas as pd
import numpy as np
from scipy.stats import linregress
from tqdm import tqdm

# Load merged land-only CSV
df = pd.read_csv("client/public/temperature/bloomwatch_land.csv")

# Frost occurrence
df['frost_occurred'] = df['frost_days'] > 0

# --- Compute Growing Degree Days (GDD) ---
# Base temp 278.15 K (~5°C)
df['gdd'] = np.maximum(0, df['tg'] - 278.15)

# --- Trend of frost days per grid ---
trend_list = []
for (lat, lon), group in tqdm(df.groupby(['lat','lon']), total=df.groupby(['lat','lon']).ngroups):
    slope, _, _, _, _ = linregress(group['year'], group['frost_days'])
    trend_list.append({'lat': lat, 'lon': lon, 'frost_trend': slope})

df_trend = pd.DataFrame(trend_list)

# Merge trend back
df = df.merge(df_trend, on=['lat','lon'], how='left')

# --- Save final metrics CSV ---
output_csv = "client/public/temperature/bloomwatch_metrics.csv"
df.to_csv(output_csv, index=False)
print(f"✅ Blooming metrics saved: {output_csv}")
