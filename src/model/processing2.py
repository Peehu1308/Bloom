import xarray as xr
import pandas as pd

# --- File path ---
file_path = "client/public/temperature/ID_C3S-glob-agric_gfdl-esm2m_hist_dek_19810101-20101231_v1.1.nc"

# --- Load dataset ---
print("Loading dataset...")
ds = xr.open_dataset(file_path)

# Variable to process
var_name = 'ID'  # change this if you want another variable
data_var = ds[var_name]

# Convert time to datetime
data_var['time'] = pd.to_datetime(data_var['time'].values)

# --- Resample to annual sum (or mean if appropriate) ---
print(f"Resampling to annual {var_name} (this may take a minute)...")
annual_var = data_var.resample(time='YE').sum(dim='time')  # sum works for counts; use .mean() if continuous
print("Resampling done.")

# --- Flatten the grid using stack ---
annual_var_stacked = annual_var.stack(grid=("lat", "lon"))

# --- Convert to pandas DataFrame ---
annual_var_df = annual_var_stacked.to_dataframe().reset_index(level="time")

# Rename columns
annual_var_df = annual_var_df.rename(columns={var_name: var_name.lower(), 'time':'year'})

# Convert year to integer
annual_var_df['year'] = annual_var_df['year'].dt.year

# --- Show how much data was processed ---
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
print(f" - Total rows in CSV: {total_rows}")

# --- Save to CSV ---
output_csv = f"client/public/temperature/{var_name.lower()}_annual.csv"
annual_var_df.to_csv(output_csv, index=False)
print(f"✅ CSV saved: {output_csv}")
