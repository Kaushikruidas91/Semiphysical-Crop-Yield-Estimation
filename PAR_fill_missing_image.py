from osgeo import gdal
import numpy as np
import glob
from datetime import date, timedelta

crop = 'wheat'

def nan_if(arr, value):
    return np.where(arr == value, np.nan, arr)

def mon(test):
    if (test == '01'): 
        mon = 'JAN'
    elif (test == '02'):
            mon = 'FEB'
    elif (test == '03'):
            mon = 'MAR'
    elif (test == '04'):
            mon = 'APR'
    elif (test == '04'):
            mon = 'APR'
    elif (test == '05'):
            mon = 'MAY'
    elif (test == '06'):
            mon = 'JUN'
    elif (test == '07'):
            mon = 'JUL'
    elif (test == '08'):
            mon = 'AUG'
    elif (test == '09'):
            mon = 'SEP'
    elif (test == '10'):
            mon = 'OCT'
    elif (test == '11'):
            mon = 'NOV'
    elif (test == '12'):
            mon = 'DEC'
    return mon
#tt = mon('11')
#print(tt)
#year = 2023

file_paths = []
path = 'D:/Amit_MNCFC/Yeild_estimation_data/APAR_Data/Year_2023/'

d1 = date(2023, 1, 1)
d2 = date(2023, 12, 31)
d = d2-d1
print(d.days)
for i in range(d.days+1):
    st_day = d1 + timedelta(days=(i)*1)
    x = str(st_day).split("-")
    #print(x)
    month = mon(x[1])
    #print(month)
    file_name = path+'3DIMG_'+x[2]+month+x[0]+'_0000_L3C_INS_DLY_V01R00_INS_DLY.tif'
    file_paths += [file_name]
    ds = gdal.Open(file_name)
    if (ds):
        print('available')
    else:
        print(file_name)
        bf_dt = st_day - timedelta(days=1)
        af_dt = st_day + timedelta(days=1)
        print(bf_dt)
        print(af_dt)
        date_bf = str(bf_dt).split('-')[2]
        date_af = str(af_dt).split('-')[2]

        month_bf = str(bf_dt).split('-')[1]
        month_bf = mon(month_bf)
        month_af = str(af_dt).split('-')[1]
        month_af = mon(month_af)
        print(date_bf)
        print(date_af)
        file_name_bf = path+'3DIMG_'+str(date_bf).zfill(2)+month_bf+x[0]+'_0000_L3C_INS_DLY_V01R00_INS_DLY.tif'
        file_name_af = path+'3DIMG_'+str(date_af).zfill(2)+month_af+x[0]+'_0000_L3C_INS_DLY_V01R00_INS_DLY.tif'
        res = []
        ds = gdal.Open(file_name_bf)
        ds1 = gdal.Open(file_name_af)
        res.append(ds.GetRasterBand(1).ReadAsArray())
        res.append(ds1.GetRasterBand(1).ReadAsArray())
        stacked = np.dstack(res)

        mean = np.nanmean(nan_if(stacked, -9999), axis=-1)
        mean[np.isnan(mean)] = -9999
        mean = nan_if(mean,-9999)
        #print(img)
        
        # Finally save a new raster with the result. 
        # This assumes that all inputs have the same geotransform since we just copy the first
        driver = gdal.GetDriverByName('GTiff')
        #out_file_name = 'PAR'+str(st_day)+'_to_'+str(en_day)+'.tif'
        result = driver.CreateCopy(path+'3DIMG_'+x[2]+month+x[0]+'_0000_L3C_INS_DLY_V01R00_INS_DLY.tif', gdal.Open(file_paths[0]))
        result.GetRasterBand(1).WriteArray(mean)
        result = None

