import pandas as pd

# --- Config ---
DATA_FILE = "client/public/data/bloomwatch_land.csv"
CENTROID_FILE = "client/public/data/country_centroid.csv"
OUTPUT_FILE = "client/public/data/bloomwatch_filtered.csv"
RADIUS_DEGREES = 5  # ±5 degrees latitude/longitude from centroid

# --- Load country centroids ---
centroids = pd.read_csv(CENTROID_FILE)

# --- User input ---
country_name = input("Enter a country name: ").strip()
start_year = int(input("Enter start year (e.g., 1981): "))
end_year = int(input("Enter end year (e.g., 2010): "))

# --- Get centroid for country ---
if country_name not in centroids['country'].values:
    print(f"Error: {country_name} not found in centroids CSV!")
    exit()

lat_center = centroids.loc[centroids['country'] == country_name, 'lat'].values[0]
lon_center = centroids.loc[centroids['country'] == country_name, 'lon'].values[0]

# --- Load bloom/frost data ---
df = pd.read_csv(DATA_FILE)

# --- Filter by latitude/longitude ---
lat_min = lat_center - RADIUS_DEGREES
lat_max = lat_center + RADIUS_DEGREES
lon_min = lon_center - RADIUS_DEGREES
lon_max = lon_center + RADIUS_DEGREES

df_filtered = df[
    (df['lat'] >= lat_min) & (df['lat'] <= lat_max) &
    (df['lon'] >= lon_min) & (df['lon'] <= lon_max) &
    (df['year'] >= start_year) & (df['year'] <= end_year)
].reset_index(drop=True)

# --- Save filtered data ---
df_filtered.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Filtered data saved to: {OUTPUT_FILE}")
print(f"Total points: {len(df_filtered)}")
