import xarray as xr
import pandas as pd

# --- File path ---
file_path = "client/public/temperature/FD_C3S-glob-agric_gfdl-esm2m_hist_dek_19810101-20101231_v1.1.nc"

# --- Load dataset ---
print("Loading dataset...")
ds = xr.open_dataset(file_path)

# Variable is 'FD' (Frost Days)
fd = ds['FD']

# Convert time to datetime
fd['time'] = pd.to_datetime(fd['time'].values)

# --- Resample to annual frost days ---
print("Resampling to annual frost days (this may take a minute)...")
annual_fd = fd.resample(time='YE').sum(dim='time')
print("Resampling done.")

# --- Flatten the grid using stack ---
annual_fd_stacked = annual_fd.stack(grid=("lat", "lon"))

# --- Convert to pandas DataFrame ---
# Keep lat/lon clean, avoid duplication
annual_fd_df = annual_fd_stacked.to_dataframe().reset_index(level="time")

# Rename columns
annual_fd_df = annual_fd_df.rename(columns={'FD':'frost_days', 'time':'year'})

# Convert year to integer
annual_fd_df['year'] = annual_fd_df['year'].dt.year

# --- Show how much data was processed ---
num_years = len(annual_fd['time'])
num_lat = len(fd['lat'])
num_lon = len(fd['lon'])
num_gridpoints = num_lat * num_lon
total_rows = len(annual_fd_df)
print(f"📊 Processed data summary:")
print(f" - Years: {num_years}")
print(f" - Latitude points: {num_lat}")
print(f" - Longitude points: {num_lon}")
print(f" - Total grid points per year: {num_gridpoints}")
print(f" - Total rows in CSV: {total_rows}")

# --- Save to CSV ---
output_csv = "client/public/temperature/frost_days_annual.csv"
annual_fd_df.to_csv(output_csv, index=False)
print(f"✅ CSV saved: {output_csv}")
