import pandas as pd
import numpy as np
from scipy.stats import linregress
from tqdm import tqdm
import os

# --- File paths ---
input_csv = "client/public/temperature/frost_days_annual.csv"
output_csv = "client/public/temperature/frost_days_metrics.csv"
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

# --- Load CSV ---
df = pd.read_csv(input_csv)

# --- Derived Features ---
df['frost_occurred'] = df['frost_days'] > 0

# --- Spatial Metrics ---
spatial_mean = df.groupby(['lat','lon'])['frost_days'].mean().reset_index().rename(columns={'frost_days':'frost_mean'})
spatial_max = df.groupby(['lat','lon'])['frost_days'].max().reset_index().rename(columns={'frost_days':'frost_max'})
spatial_min = df.groupby(['lat','lon'])['frost_days'].min().reset_index().rename(columns={'frost_days':'frost_min'})
spatial_prob = df.groupby(['lat','lon'])['frost_occurred'].mean().reset_index().rename(columns={'frost_occurred':'frost_prob'})

# --- Trend calculation with progress bar ---
def frost_trend(y):
    x = np.arange(len(y))
    slope, _, _, _, _ = linregress(x, y)
    return slope

# Prepare storage
trend_list = []

print("Calculating frost trend per location...")
lat_lon_groups = df.groupby(['lat','lon'])
for (lat, lon), group in tqdm(lat_lon_groups, total=len(lat_lon_groups)):
    slope = frost_trend(group['frost_days'].values)
    trend_list.append({'lat': lat, 'lon': lon, 'frost_trend': slope})

spatial_trend = pd.DataFrame(trend_list)

# Merge all spatial metrics
spatial_metrics = spatial_mean.merge(spatial_max, on=['lat','lon']) \
                              .merge(spatial_min, on=['lat','lon']) \
                              .merge(spatial_prob, on=['lat','lon']) \
                              .merge(spatial_trend, on=['lat','lon'])

# Merge with original data
final_df = df.merge(spatial_metrics, on=['lat','lon'], how='left')

# Save CSV
final_df.to_csv(output_csv, index=False)
print(f"✅ Completed! Metrics saved to {output_csv}")
