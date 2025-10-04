import netCDF4
import json

# Path to your NetCDF-4 file
nc_file = "client/public/Mhmd08___inaturalist/high_vegetation_cover_stream-oper_daily-mean.nc"
json_file = "client/public/Mhmd08___inaturalist/high_vegetation_cover_stream-oper_daily-mean.json"

# Open NetCDF-4 file
ds = netCDF4.Dataset(nc_file)

# Convert all variables to lists
data = {var: ds.variables[var][:].tolist() for var in ds.variables}

# Save as JSON
with open(json_file, "w") as f:
    json.dump(data, f)

print(f"Converted {nc_file} to {json_file}")
