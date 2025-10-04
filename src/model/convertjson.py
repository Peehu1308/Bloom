import xarray as xr
import json

ds = xr.open_dataset("client/public/Mhmd08___inaturalist/type_of_low_vegetation_0_daily-mean.nc")
tvl_day = ds['tvl'].isel(valid_time=0)  # pick first day

lat = ds['latitude'].values.tolist()
lon = ds['longitude'].values.tolist()
data = tvl_day.values.tolist()

points = []
for i in range(len(lat)):
    for j in range(len(lon)):
        points.append({
            "lat": lat[i],
            "lng": lon[j],
            "size": 0.2,
            "value": data[i][j]  # you can normalize later
        })

# Save as JSON
with open("client/public/Mhmd08___inaturalist/low_vegetation_points.json", "w") as f:
    json.dump(points, f)
