import xarray as xr
import pandas as pd
import numpy as np
from scipy.stats import linregress
from tqdm import tqdm
import os

# --- File path ---
file_path = "client/public/temperature/TN_C3S-glob-agric_gfdl-esm2m_hist_dek_19810101-20101231_v1.1.nc"

# --- Load dataset ---
print("Loading dataset...")
ds = xr.open_dataset(file_path)

# Variable to process
var_name = 'TN'  # daily minimum temperature
data_var = ds[var_name]

# Convert time to datetime
data_var['time'] = pd.to_datetime(data_var['time'].values)

# --- Resample to annual mean (continuous variable) ---
print(f"Resampling to annual {var_name} (this may take a minute)...")
annual_var = data_var.resample(time='YE').mean(dim='time')
print("Resampling done.")

# --- Flatten the grid using stack ---
annual_var_stacked = annual_var.stack(grid=("lat", "lon"))

# --- Convert to pandas DataFrame ---
annual_var_df = annual_var_stacked.to_dataframe().reset_index(level="time")

# Rename columns
annual_var_df = annual_var_df.rename(columns={var_name: var_name.lower(), 'time':'year'})

# Convert year to integer
annual_var_df['year'] = annual_var_df['year'].dt.year

# --- Optional: clean NaNs ---
annual_var_df = annual_var_df.dropna(subset=[var_name.lower()]).reset_index(drop=True)

# --- Show data summary ---
num_years = len(annual_var['time'])
num_lat = len(data_var['lat'])
num_lon = len(data_var['lon'])
num_gridpoints = num_lat * num_lon
total_rows = len(annual_var_df)

print(f"📊 Processed data summary for {var_name}:")
print(f" - Years: {num_years}")
print(f" - Latitude points: {num_lat}")
print(f" - Longitude points: {num_lon}")
print(f" - Total grid points per year: {num_gridpoints}")
print(f" - Total rows in CSV (after cleaning NaNs): {total_rows}")

# --- Save annual CSV ---
annual_csv = f"client/public/temperature/{var_name.lower()}_annual.csv"
os.makedirs(os.path.dirname(annual_csv), exist_ok=True)
annual_var_df.to_csv(annual_csv, index=False)
print(f"✅ Annual CSV saved: {annual_csv}")


# --- Compute spatial & temporal metrics ---
df = annual_var_df.copy()

# Derived feature: is temp > 0°C? (binary indicator, optional)
df[f'{var_name.lower()}_occurred'] = df[var_name.lower()] > 0

# --- Spatial metrics ---
spatial_mean = df.groupby(['lat','lon'])[var_name.lower()].mean().reset_index().rename(columns={var_name.lower():f'{var_name.lower()}_mean'})
spatial_max = df.groupby(['lat','lon'])[var_name.lower()].max().reset_index().rename(columns={var_name.lower():f'{var_name.lower()}_max'})
spatial_min = df.groupby(['lat','lon'])[var_name.lower()].min().reset_index().rename(columns={var_name.lower():f'{var_name.lower()}_min'})
spatial_prob = df.groupby(['lat','lon'])[f'{var_name.lower()}_occurred'].mean().reset_index().rename(columns={f'{var_name.lower()}_occurred':f'{var_name.lower()}_prob'})

# --- Trend per location with progress bar ---
def calc_trend(y):
    x = np.arange(len(y))
    slope, _, _, _, _ = linregress(x, y)
    return slope

trend_list = []
print(f"Calculating {var_name} trend per location...")
lat_lon_groups = df.groupby(['lat','lon'])
for (lat, lon), group in tqdm(lat_lon_groups, total=len(lat_lon_groups)):
    slope = calc_trend(group[var_name.lower()].values)
    trend_list.append({'lat': lat, 'lon': lon, f'{var_name.lower()}_trend': slope})

spatial_trend = pd.DataFrame(trend_list)

# Merge all spatial metrics
spatial_metrics = spatial_mean.merge(spatial_max, on=['lat','lon']) \
                              .merge(spatial_min, on=['lat','lon']) \
                              .merge(spatial_prob, on=['lat','lon']) \
                              .merge(spatial_trend, on=['lat','lon'])

# Merge with original data
final_df = df.merge(spatial_metrics, on=['lat','lon'], how='left')

# --- Temporal metrics ---
temporal_metrics = df.groupby('year')[var_name.lower()].agg(['mean','min','max']).reset_index()
temporal_metrics = temporal_metrics.rename(columns={'mean':f'{var_name.lower()}_mean','min':f'{var_name.lower()}_min','max':f'{var_name.lower()}_max'})
temporal_metrics_csv = f"client/public/temperature/{var_name.lower()}_temporal_metrics.csv"
temporal_metrics.to_csv(temporal_metrics_csv, index=False)

# --- Save final CSV ---
metrics_csv = f"client/public/temperature/{var_name.lower()}_metrics.csv"
final_df.to_csv(metrics_csv, index=False)

print(f"✅ Metrics CSV saved: {metrics_csv}")
print(f"✅ Temporal metrics CSV saved: {temporal_metrics_csv}")
