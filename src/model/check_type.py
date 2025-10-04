import xarray as xr

data = xr.open_dataset("client/public/Mhmd08___inaturalist/type_of_low_vegetation_0_daily-mean.nc")
print(data)
