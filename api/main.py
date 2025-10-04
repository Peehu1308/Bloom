from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import xarray as xr
from geopy.geocoders import Nominatim

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # set your frontend URL here in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

file_path = r"C:\Users\peehu\OneDrive\Desktop\React\BloomWatch\client\public\Mhmd08___inaturalist\leaf_area_index_high_vegetation_0_daily-mean.nc"
ds = xr.open_dataset(file_path)
lai = ds['lai_hv']

@app.get("/lai")
def get_lai(place: str):
    geolocator = Nominatim(user_agent="bloomwatch")
    location = geolocator.geocode(place)
    if not location:
        return {"error": "Location not found"}

    lat, lon = location.latitude, location.longitude
    ts = lai.sel(latitude=lat, longitude=lon, method="nearest")

    data = {
        "place": place,
        "latitude": float(lat),
        "longitude": float(lon),
        "times": [str(t.values) for t in ts['valid_time']],
        "lai_values": [float(v) for v in ts.values],
    }
    return data
