
import pandas as pd
import ee

ee.Authenticate()  # run once
ee.Initialize(project='warm-rock-448811-k9')



# point and date range
pt = ee.Geometry.Point([77.59, 12.97])   # lon, lat
col = ee.ImageCollection('MODIS/061/MOD13Q1') \
        .select('NDVI') \
        .filterDate('2023-01-01', '2023-12-31') \
        .filterBounds(pt)

# map images to (date, value)
def toFeature(img):
    mean = img.reduceRegion(ee.Reducer.first(), pt, 250).get('NDVI')
    return ee.Feature(None, {'date': img.date().format('YYYY-MM-dd'), 'ndvi': mean})

ts = col.map(toFeature).filter(ee.Filter.notNull(['ndvi']))
fc = ee.FeatureCollection(ts)

# get client-side - careful with length (small things ok)
data = fc.getInfo()  # for small number of dates; else export to Drive/Cloud
rows = [(f['properties']['date'], f['properties']['ndvi']) for f in data['features']]
df = pd.DataFrame(rows, columns=['date','ndvi'])
print(df)
