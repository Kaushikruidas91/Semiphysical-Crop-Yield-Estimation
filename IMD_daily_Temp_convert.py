import numpy as np
from PIL import Image as im
from osgeo import gdal, osr, ogr
import glob as glob
import rasterio

def getGeoTransform(extent, nlines, ncols):
    resx = (extent[2] - extent[0]) / ncols
    resy = (extent[3] - extent[1]) / nlines
    return [extent[0], resx, 0, extent[3] , 0, -1*resy]
extent = [67.25, 7.25, 97.75, 37.75]
nlat=61 # Obtained from the control file
nlon=61
ntime=1
#lons=np.arange(67.5,98,0.5) # Define latitude and longitude as obtained from control file
#print(lons)
#lats=np.arange(7.5,38,0.5)
#print(lats)

filepaths = glob.glob(r"D:\CIPL_WORK\Weather_Based_Yield_Jute\Weather_Data\Tmax\Tmax_2006\*.grd")
print(filepaths)
for file in filepaths:
    filename = file.split(".")
    f=open(file,'rb')
    data=np.fromfile(f,dtype="float32",count=-1) #Opening and reading the file into a one-dimensional array
    #print(len(data.shape))
    ################Reshaping data######################
    temp=np.reshape(data,(61,61),order='C')
    #print(temp[0])
    temp = np.flipud(temp)

    driver = gdal.GetDriverByName('GTiff')
    nrows = temp.shape[0]
    
    ncols = temp.shape[1]
    
    nbands = ntime
    data_type = gdal.GDT_Float32 # gdal.GDT_Float32
    #print(temp)
    # Create a temp grid
    #options = ['COMPRESS=JPEG', 'JPEG_QUALITY=80', 'TILED=YES']
    grid_data = driver.Create(filename[-2]+'.tif', ncols, nrows, 1, data_type)#, options)

    # Write data for each bands
    grid_data.GetRasterBand(1).WriteArray(temp)
    #print(grid_data)
    # Lat/Lon WSG84 Spatial Reference System
    srs = osr.SpatialReference()
    srs.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
    
    # Setup projection and geo-transform
    grid_data.SetProjection(srs.ExportToWkt())
    #print(getGeoTransform(extent, nlines, ncols))
    grid_data.SetGeoTransform(getGeoTransform(extent, nrows, ncols))
    # Save the file
    file_name = filename[-2]+'.tif'
    #print(f'Generated GeoTIFF: {file_name}')
    #driver.CreateCopy(file_name, grid_data, 0)  
    
    # Close the file
    driver = None
    grid_data = None

rasterpaths = glob.glob(r"D:\CIPL_WORK\Weather_Based_Yield_Jute\Weather_Data\Tmax\Tmax_2006\*.tif")
print(rasterpaths)

# Read metadata of first file
with rasterio.open(rasterpaths[0]) as src0:
    meta = src0.meta

# Update meta to reflect the number of layers
meta.update(count = len(rasterpaths))

# Read each layer and write it to stack
with rasterio.open('tmax_2022.tif', 'w', **meta) as dst:
    for id, layer in enumerate(rasterpaths, start=1):
        with rasterio.open(layer) as src1:
            dst.write_band(id, src1.read(1))

exit()