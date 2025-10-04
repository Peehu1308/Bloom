from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import xarray as xr
from geopy.geocoders import Nominatim
from datetime import datetime
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace with frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load dataset once
file_path = r"C:\Users\peehu\OneDrive\Desktop\React\BloomWatch\client\public\Mhmd08___inaturalist\leaf_area_index_low_vegetation_0_daily-mean.nc"
ds = xr.open_dataset(file_path)
lai = ds['lai_lv']  # low vegetation LAI

geolocator = Nominatim(user_agent="bloomwatch")

@app.get("/lai_lv")
def get_lai_lv(
    place: str,
    start_date: str = Query(..., description="YYYY-MM-DD"),
    end_date: str = Query(..., description="YYYY-MM-DD")
):
    # Get location coordinates
    location = geolocator.geocode(place)
    if not location:
        return {"error": "Location not found"}
    
    lat, lon = location.latitude, location.longitude

    # Convert input dates to np.datetime64
    start = np.datetime64(start_date)
    end = np.datetime64(end_date)

    # Select data for location and time range
    ts = lai.sel(latitude=lat, longitude=lon, method="nearest").sel(valid_time=slice(start, end))

    # Return JSON
    data = {
        "place": place,
        "latitude": float(lat),
        "longitude": float(lon),
        "times": [str(t.values) for t in ts['valid_time']],
        "lai_values": [float(v) for v in ts.values],
    }
    return data
