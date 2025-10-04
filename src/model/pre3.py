import xarray as xr
import pandas as pd
import os

# --- File path ---
file_path = "client/public/temperature/TNn_C3S-glob-agric_gfdl-esm2m_hist_dek_19810101-20101231_v1.1.nc"

# --- Load dataset ---
print("Loading TNn dataset...")
ds = xr.open_dataset(file_path)

# --- Variable is 'TNn' (Nighttime Minimum Temperature) ---
tnn = ds['TNn']

# --- Convert time to datetime ---
tnn['time'] = pd.to_datetime(tnn['time'].values)

# --- Resample to annual mean (average over each year) ---
print("Resampling to annual TNn (this may take a minute)...")
annual_tnn = tnn.resample(time='YE').mean(dim='time')
print("Resampling done.")

# --- Flatten the grid using stack ---
annual_tnn_stacked = annual_tnn.stack(grid=("lat", "lon"))

# --- Convert to pandas DataFrame ---
annual_tnn_df = annual_tnn_stacked.to_dataframe().reset_index(level="time")

# --- Rename columns ---
annual_tnn_df = annual_tnn_df.rename(columns={'TNn':'tnn', 'time':'year'})

# --- Convert year to integer ---
annual_tnn_df['year'] = annual_tnn_df['year'].dt.year

# --- Show processed data summary ---
num_years = len(annual_tnn['time'])
num_lat = len(tnn['lat'])
num_lon = len(tnn['lon'])
num_gridpoints = num_lat * num_lon
total_rows = len(annual_tnn_df)

print(f"📊 Processed data summary for TNn:")
print(f" - Years: {num_years}")
print(f" - Latitude points: {num_lat}")
print(f" - Longitude points: {num_lon}")
print(f" - Total grid points per year: {num_gridpoints}")
print(f" - Total rows in CSV: {total_rows}")

# --- Save to CSV ---
output_csv = "client/public/temperature/tnn_annual.csv"
os.makedirs(os.path.dirname(output_csv), exist_ok=True)
annual_tnn_df.to_csv(output_csv, index=False)
print(f"✅ Annual CSV saved: {output_csv}")

# --- Optional: preview first few rows ---
print(annual_tnn_df.head(10))
