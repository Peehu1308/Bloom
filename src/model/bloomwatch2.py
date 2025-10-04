import pandas as pd
import numpy as np
from scipy.stats import linregress
from tqdm import tqdm
import os

# --- File paths ---
input_csv = "client/public/temperature/id_annual.csv"
output_csv = "client/public/temperature/id_metrics.csv"
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

# --- Load CSV ---
df = pd.read_csv(input_csv)

# --- Derived features ---
# If you want a binary indicator (e.g., ID > 0)
df['id_occurred'] = df['id'] > 0

# --- Spatial metrics ---
spatial_mean = df.groupby(['lat','lon'])['id'].mean().reset_index().rename(columns={'id':'id_mean'})
spatial_max = df.groupby(['lat','lon'])['id'].max().reset_index().rename(columns={'id':'id_max'})
spatial_min = df.groupby(['lat','lon'])['id'].min().reset_index().rename(columns={'id':'id_min'})
spatial_prob = df.groupby(['lat','lon'])['id_occurred'].mean().reset_index().rename(columns={'id_occurred':'id_prob'})

# --- Trend per location with progress bar ---
def calc_trend(y):
    x = np.arange(len(y))
    slope, _, _, _, _ = linregress(x, y)
    return slope

trend_list = []
print("Calculating ID trend per location...")
lat_lon_groups = df.groupby(['lat','lon'])
for (lat, lon), group in tqdm(lat_lon_groups, total=len(lat_lon_groups)):
    slope = calc_trend(group['id'].values)
    trend_list.append({'lat': lat, 'lon': lon, 'id_trend': slope})

spatial_trend = pd.DataFrame(trend_list)

# Merge all spatial metrics
spatial_metrics = spatial_mean.merge(spatial_max, on=['lat','lon']) \
                              .merge(spatial_min, on=['lat','lon']) \
                              .merge(spatial_prob, on=['lat','lon']) \
                              .merge(spatial_trend, on=['lat','lon'])

# Merge with original data
final_df = df.merge(spatial_metrics, on=['lat','lon'], how='left')

# --- Temporal metrics ---
temporal_metrics = df.groupby('year')['id'].agg(['mean','min','max']).reset_index()
temporal_metrics = temporal_metrics.rename(columns={'mean':'id_mean','min':'id_min','max':'id_max'})
temporal_metrics.to_csv("client/public/temperature/id_temporal_metrics.csv", index=False)

# --- Save final CSV ---
final_df.to_csv(output_csv, index=False)
print(f"✅ Metrics computed and saved: {output_csv}")
print(f"✅ Temporal metrics saved: client/public/temperature/id_temporal_metrics.csv")
