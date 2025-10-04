import xarray as xr

# Open the downloaded NetCDF file
ds = xr.open_dataset('era5_vegetation.nc')

# See the variables and metadata
print(ds)

# Access a specific variable, e.g., high vegetation cover
high_veg = ds['high_vegetation_cover']

# Convert to pandas DataFrame if needed
df = high_veg.to_dataframe().reset_index()
print(df.head())
