from osgeo import gdal
import numpy as np
import glob
from datetime import date, timedelta

#crop = 'paddy'

def nan_if(arr, value):
        return np.where(arr == value, np.nan, arr)



#year = 2023


path = 'D:/Amit_MNCFC/Yeild_estimation_data/APAR_Data/Year_2023/'
num = 16
d1 = date(2023, 1, 1)
d2 = date(2023, 12, 31)
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
        
        if (x[1] == '01'): 
            mon = 'JAN'
        elif (x[1] == '02'):
             mon = 'FEB'
        elif (x[1] == '03'):
             mon = 'MAR'
        elif (x[1] == '04'):
             mon = 'APR'
        elif (x[1] == '04'):
             mon = 'APR'
        elif (x[1] == '05'):
             mon = 'MAY'
        elif (x[1] == '06'):
             mon = 'JUN'
        elif (x[1] == '07'):
             mon = 'JUL'
        elif (x[1] == '08'):
             mon = 'AUG'
        elif (x[1] == '09'):
             mon = 'SEP'
        elif (x[1] == '10'):
             mon = 'OCT'
        elif (x[1] == '11'):
             mon = 'NOV'
        elif (x[1] == '12'):
             mon = 'DEC'
        file_name = path+'3DIMG_'+x[2]+mon+x[0]+'_0000_L3C_INS_DLY_V01R00_INS_DLY.tif'
        
        file_paths += [file_name]

    print(file_paths)

    res = []
    for f in file_paths:
        #print(f)
        ds = gdal.Open(f)
        res.append(ds.GetRasterBand(1).ReadAsArray()) # We assume that all rasters has a single band
    stacked = np.dstack(res) # We assume that all rasters have the same dimensions
    #print(stacked)
    sum = np.nansum(nan_if(stacked, -9999), axis=-1)
    sum[np.isnan(sum)] = -9999
    sum = nan_if(sum,-9999)
    #print(img)
    img = sum * 0.5
       
    img[np.isnan(img)] = -9999
    #mean1 = np.nan_to_num(mean)

    # Finally save a new raster with the result. 
    # This assumes that all inputs have the same geotransform since we just copy the first
    driver = gdal.GetDriverByName('GTiff')
    out_file_name = 'PAR'+str(st_day)+'_to_'+str(en_day)+'.tif'   
    result = driver.CreateCopy('D:/FASAL/Rabi_rice_23-24/23-24_SP/Insolation/PAR_16_day/'+out_file_name, gdal.Open(file_paths[0]))   
    result.GetRasterBand(1).WriteArray(img)   
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
#     tscaler = ((img - tmin)*(img -tmax))/(((img - tmin)*(img - tmax)) - ((img - topt)*(img - topt)))
    
#     tscaler[img < tmin] = 0
#     tscaler[np.isnan(tscaler)] = -9999
#     #print(tscaler)
   
#     driver = gdal.GetDriverByName('GTiff')
#     out_file_name = 'T_scaler_'+f_split[0][-8:]+'.tif'
#     result = driver.CreateCopy('E:\\Drought_kharif_2022\\Stats\\IMD_gridded_data\\python_code\\temp_data\\daily\\tscaler\\'+str(year)+'\\'+out_file_name, gdal.Open(file_paths[0]))
#     result.GetRasterBand(1).WriteArray(tscaler)
#     result.GetRasterBand(1).SetNoDataValue(-9999)
#     result = None