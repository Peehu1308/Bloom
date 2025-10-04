import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from PIL import Image


# Path to your file
file_path = r"C:/Users/peehu/OneDrive/Desktop/React/BloomWatch/client/public/data/matthews.dat"

# Load the grid (skip header lines)
data = np.loadtxt(file_path, skiprows=6)

# Replace NODATA values (-9999) with NaN for clean plotting
data[data == -9999] = np.nan

# Define latitude and longitude (center of each 1° cell)
lats = np.linspace(89.5, -89.5, data.shape[0])
lons = np.linspace(-179.5, 179.5, data.shape[1])

# --- Plot ---
plt.figure(figsize=(12, 6))
ax = plt.axes(projection=ccrs.Robinson())

# Plot the vegetation grid
im = ax.pcolormesh(
    lons, lats, data,
    cmap='tab20',               # categorical color map
    transform=ccrs.PlateCarree()
)

# Add coastlines and colorbar
ax.coastlines()
plt.colorbar(im, label='Vegetation Type Code', shrink=0.7)
ax.set_title("Global Vegetation Types (Matthews 1971–1982)", fontsize=14)
plt.show()