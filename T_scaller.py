from osgeo import gdal
import numpy as np
import glob
from datetime import date, timedelta

crop = 'paddy'

if (crop == 'paddy'):
    tmin = 10
    tmax = 40
    topt = 30

elif (crop == 'wheat'):
    tmin = 6
    tmax = 35
    topt = 25

file_paths = []

#year = 2016

#st_day = 1
#en_day = 31

path = f'D:/FASAL/Semi-physical_raw_datasets/Temperature/2024/Temperature/T_mean/2024/'

d1 = date(2024, 1, 1)
d2 = date(2024, 10, 22)
d = d2-d1
for i in range(d.days + 1):
    day = d1 + timedelta(days=i)
    #print(day)
    #print(str(day))
    x = str(day).split("-")
    file_name = path+'T_mean_'+x[0]+x[1]+x[2]+'.tif'
    file_paths += [file_name]

def nan_if(arr, value):
    return np.where(arr == value, np.nan, arr)

#file_paths = glob.glob("E:/Drought_kharif_2022/Stats/IMD_gridded_data/python_code/*.tif")

print(file_paths)


#file_paths = ['''List of paths to your files''']
# We build one large np array of all images (this requires that all data fits in memory)
res = []
for f in file_paths:
    f_split = f.split('.')
    print(f_split[0]+'_'+f_split[0])
    ds = gdal.Open(f)
    img = ds.GetRasterBand(1).ReadAsArray()
    img = nan_if(img,-9999)
    #print(img)
    tscaler = ((img - tmin)*(img -tmax))/(((img - tmin)*(img - tmax)) - ((img - topt)*(img - topt)))
    
    tscaler[img < tmin] = 0
    tscaler[np.isnan(tscaler)] = -9999
    #print(tscaler)   
   
    driver = gdal.GetDriverByName('GTiff')                      
    out_file_name = 'T_scaler_'+f_split[0][-8:]+'.tif'
    result = driver.CreateCopy(f'D:/FASAL/Kharif_Rice/Temperature/2024/T_scalar/2024/'+out_file_name, gdal.Open(file_paths[0]))
    result.GetRasterBand(1).WriteArray(tscaler)
    result.GetRasterBand(1).SetNoDataValue(-9999)
    result = None