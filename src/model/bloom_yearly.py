import pandas as pd
import numpy as np
from scipy.stats import linregress
from tqdm import tqdm

# --- Load merged land CSV ---
df = pd.read_csv("client/public/temperature/bloomwatch_land.csv")

# --- Frost & Ice derived metrics ---
df['frost_occurred'] = df['frost_days'] > 0
df['ice_occurred'] = df['id'] > 0

# --- Growing Degree Days (GDD) ---
T_base = 278.15  # ~5°C in Kelvin
df['gdd'] = np.maximum(0, df['tg'] - T_base)

# --- Frost trend per grid ---
trend_list = []
lat_lon_groups = df.groupby(['lat','lon'])
for (lat, lon), group in tqdm(lat_lon_groups, total=len(lat_lon_groups)):
    slope, _, _, _, _ = linregress(group['year'], group['frost_days'])
    trend_list.append({'lat': lat, 'lon': lon, 'frost_trend': slope})
df_trend = pd.DataFrame(trend_list)
df = df.merge(df_trend, on=['lat','lon'], how='left')

# --- Aggregate spatial metrics per year (optional) ---
yearly_metrics = df.groupby('year').agg({
    'frost_days': ['mean','max','min'],
    'id': ['mean','max','min'],
    'tg': ['mean','max','min'],
    'tn': ['mean','max','min'],
    'tnn': ['mean','max','min'],
    'gdd': ['mean','max'],
    'frost_trend': 'mean'
}).reset_index()
yearly_metrics.columns = ['_'.join(col).strip('_') for col in yearly_metrics.columns]

# --- Save CSV ---
df.to_csv("client/public/temperature/bloomwatch_metrics.csv", index=False)
yearly_metrics.to_csv("client/public/temperature/bloomwatch_yearly.csv", index=False)
print("✅ Metrics saved for visualization!")
