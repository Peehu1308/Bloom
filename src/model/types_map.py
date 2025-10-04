import numpy as np
import json

file_path = r"C:/Users/peehu/OneDrive/Desktop/React/BloomWatch/client/public/data/matthews.dat"

data = np.loadtxt(file_path, skiprows=6)
data[data == -9999] = -1  # use -1 for no data

lats = np.linspace(89.5, -89.5, data.shape[0])
lons = np.linspace(-179.5, 179.5, data.shape[1])

points = []
for i, lat in enumerate(lats):
    for j, lon in enumerate(lons):
        points.append({
            "lat": float(lat),
            "lon": float(lon),
            "vegCode": int(data[i, j])
        })

# Save to JSON for React
with open("client/public/Mhmd08___inaturalist/vegetation_points.json", "w") as f:
    json.dump(points, f)
