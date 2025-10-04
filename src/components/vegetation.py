import xarray as xr
import matplotlib.pyplot as plt

file_path = r"C:\Users\peehu\OneDrive\Desktop\React\BloomWatch\client\public\Mhmd08___inaturalist\leaf_area_index_high_vegetation_0_daily-mean.nc"

ds = xr.open_dataset(file_path)
print(ds)


lai = ds['lai_hv']


lat, lon = 28, 77
ts = lai.sel(latitude=lat, longitude=lon, method="nearest")

ts.plot()
plt.title("High Vegetation LAI over time (Tokyo)")
plt.show()
