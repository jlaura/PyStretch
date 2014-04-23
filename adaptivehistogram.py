import sys

from osgeo import gdal
import numpy as np
from skimage import exposure

ds = gdal.Open(sys.argv[1])
bandcount = ds.RasterCount

#Output
driver = gdal.GetDriverByName('GTiff')
outds = driver.Create('output.tif', ds.RasterXSize, ds.RasterYSize, bandcount, gdal.GDT_Float32, options=['COMPRESS=LZW'])

for i in range(1, bandcount + 1):
    band = ds.GetRasterBand(i)
    ndv = band.GetNoDataValue()
    array = band.ReadAsArray()
    array = np.ma.masked_equal(array, ndv, copy=False).astype(np.float32)
    outarray = np.sqrt(array)
    #outarray = exposure.equalize_adapthist(array, ntiles_x=12, ntiles_y=12, clip_limit=0.001)

    outds.GetRasterBand(i).WriteArray(outarray)


ds = None
outds = None

