from osgeo import gdal
import numpy as np
import glob
from datetime import date, timedelta

crop = 'paddy'

def nan_if(arr, value):
        return np.where(arr == value, np.nan, arr)



year = 2024


path = f'D:/FASAL/Kharif_Rice/Temperature/2024/T_scalar/{year}/'  
num = 16
d1 = date(year, 5, 24)
d2 = date(year, 10, 14)
d = d2-d1
print(d.days)
print(round(d.days/num))
for i in range(round(d.days/num)):
    #print(d1)
    #print((d1 + timedelta(days=(i+1)*num)) - d1)
    st_day = (d1 + timedelta(days=(i+1)*num)) - timedelta(days=num)
    en_day = (d1 + timedelta(days=(i+1)*num)) - timedelta(1)
    print(st_day)
    print(en_day)
    diff = en_day - st_day
    print(diff.days+1)
    file_paths = []
    for j in range(diff.days+1):
        #print(j)
        day_single = st_day + timedelta(days=j)
        #print(day_single)
        #print(str(day))
        x = str(day_single).split("-")
        file_name = path+'T_scaler_'+x[0]+x[1]+x[2]+'.tif'
        
        file_paths += [file_name]

    print(file_paths)

    res = []
    for f in file_paths:
        #print(f)
        ds = gdal.Open(f)
        res.append(ds.GetRasterBand(1).ReadAsArray()) # We assume that all rasters has a single band
    stacked = np.dstack(res) # We assume that all rasters have the same dimensions
    #print(stacked)
    mean = np.nanmean(nan_if(stacked, -9999), axis=-1)
    mean[np.isnan(mean)] = -9999
    #mean1 = np.nan_to_num(mean)

    # Finally save a new raster with the result. 
    # This assumes that all inputs have the same geotransform since we just copy the first 
    driver = gdal.GetDriverByName('GTiff')  
    out_file_name = 'T_scaler_avg_'+str(st_day)+'to'+str(en_day)+'.tif'
    result = driver.CreateCopy(f'D:/FASAL/Kharif_Rice/Temperature/2024/T_scalar_16_day/{year}/'+out_file_name, gdal.Open(file_paths[0]))
    result.GetRasterBand(1).WriteArray(mean) 
    result = None
#for i in range()
# for i in range(d.days + 1):
#     day = d1 + timedelta(days=i)
#     #print(day)
#     #print(str(day))
#     x = str(day).split("-")
#     file_name = path+'T_mean_'+x[0]+x[1]+x[2]+'.tif'
#     file_paths += [file_name]

# def nan_if(arr, value):
#     return np.where(arr == value, np.nan, arr)

# #file_paths = glob.glob("E:/Drought_kharif_2022/Stats/IMD_gridded_data/python_code/*.tif")

# print(file_paths)


# #file_paths = ['''List of paths to your files''']
# # We build one large np array of all images (this requires that all data fits in memory)
# res = []
# for f in file_paths:
#     f_split = f.split('.')
#     print(f_split[0]+'_'+f_split[0])
#     ds = gdal.Open(f)
#     img = ds.GetRasterBand(1).ReadAsArray()
#     img = nan_if(img,-9999)
#     #print(img)
#     tscaler = ((img - tmin)(img -tmax))/(((img - tmin)(img - tmax)) - ((img - topt)*(img - topt)))
    
#     tscaler[img < tmin] = 0
#     tscaler[np.isnan(tscaler)] = -9999
#     #print(tscaler)
   
#     driver = gdal.GetDriverByName('GTiff')
#     out_file_name = 'T_scaler_'+f_split[0][-8:]+'.tif'
#     result = driver.CreateCopy('E:\\Drought_kharif_2022\\Stats\\IMD_gridded_data\\python_code\\temp_data\\daily\\tscaler\\'+str(year)+'\\'+out_file_name, gdal.Open(file_paths[0]))
#     result.GetRasterBand(1).WriteArray(tscaler)
#     result.GetRasterBand(1).SetNoDataValue(-9999)
#     result = None