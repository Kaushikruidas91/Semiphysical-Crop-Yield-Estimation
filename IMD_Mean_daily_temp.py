from osgeo import gdal
import numpy as np
import glob
from datetime import date, timedelta

file_paths = []
file_paths1 = []
year = 2024
variable  = 'tmin'
variable1 = 'tmax'
#st_day = 1
#en_day = 13
#month = 'oct'
path = r"D:/FASAL/Semi-physical_raw_datasets/Temperature/2024/Temperature/T_daily/T_min/"  
path1 = r"D:/FASAL/Semi-physical_raw_datasets/Temperature/2024/Temperature/T_daily/T_max/" 
d1 = date(year, 1, 1)
d2 = date(year, 10, 22)
d = d2-d1
for i in range(d.days + 1):
    day = d1 + timedelta(days=i)
    #print(day)
    #print(str(day))
    x = str(day).split("-")
    file_name = path+variable+'_'+x[0]+x[1]+x[2]+'.tif'
    file_name1 = path1+variable1+'_'+x[0]+x[1]+x[2]+'.tif'
    file_paths += [file_name]
    file_paths1 += [file_name1]

def nan_if(arr, value):
    return np.where(arr == value, np.nan, arr)

#file_paths = glob.glob("E:/Drought_kharif_2022/Stats/IMD_gridded_data/python_code/*.tif")
    
print(file_paths)
print(file_paths1)

#file_paths = ['''List of paths to your files''']
# We build one large np array of all images (this requires that all data fits in memory)
res = []
for f in file_paths:
    for f1 in file_paths1:
        f1_split = f1.split('.')
        f_split = f.split('.')
        if (f1_split[0][-8:] == f_split[0][-8:]):         
            print(f1_split[0]+'_'+f_split[0])
            ds = gdal.Open(f)
            ds1 = gdal.Open(f1)
            res.append(ds.GetRasterBand(1).ReadAsArray())
            res.append(ds1.GetRasterBand(1).ReadAsArray())
            stacked = np.dstack(res)
            mean = np.nanmean(nan_if(stacked, 99.900002), axis=-1) 
            mean[np.isnan(mean)] = -9999

            driver = gdal.GetDriverByName('GTiff')                                
            out_file_name = 'T_mean_'+f1_split[0][-8:]+'.tif'
            result = driver.CreateCopy('D:\\FASAL\\Semi-physical_raw_datasets\\Temperature\\2024\\Temperature\\T_mean\\'+str(year)+'\\'+out_file_name, gdal.Open(file_paths[0]))
            result.GetRasterBand(1).WriteArray(mean)
            result = None