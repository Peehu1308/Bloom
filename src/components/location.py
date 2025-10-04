import xarray as xr
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
import numpy as np

# Step 1: Load dataset
file_path = r"C:\Users\peehu\OneDrive\Desktop\React\BloomWatch\client\public\Mhmd08___inaturalist\leaf_area_index_high_vegetation_0_daily-mean.nc"
ds = xr.open_dataset(file_path)
lai = ds['lai_hv']

# Step 2: Enter the place name
place_name = input("Enter a place name: ")

# Step 3: Get latitude and longitude using geopy
geolocator = Nominatim(user_agent="bloomwatch")
location = geolocator.geocode(place_name)

if location:
    lat, lon = location.latitude, location.longitude
    print(f"📍 {place_name} → Latitude: {lat:.2f}, Longitude: {lon:.2f}")

    # Step 4: Extract LAI data for that location
    ts = lai.sel(latitude=lat, longitude=lon, method="nearest")

    # Step 5: Plot the bloom curve
    ts.plot()
    plt.title(f"🌸 High Vegetation LAI over Time ({place_name})")
    plt.xlabel("Date")
    plt.ylabel("Leaf Area Index (LAI)")
    plt.show()

    # Step 6: Optional — detect bloom onset date
    bloom_threshold = 2.5
    onset_index = np.argmax(ts.values > bloom_threshold)
    onset_date = ts['valid_time'].values[onset_index]
    print("🌿 Estimated Bloom Onset Date:", np.datetime_as_string(onset_date, unit='D'))

else:
    print("❌ Could not find that location. Please check the name.")
