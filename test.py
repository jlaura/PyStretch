from osgeo import gdal
import numpy as np
import time
import sys

ds = gdal.Open(sys.argv[1])
time.sleep(5)
print "Reading"
arr = ds.GetRasterBand(1).ReadAsArray().astype(np.int8)
print arr.dtype
time.sleep(5)
print "Stats"
minimum = np.amin(arr)
maximum = np.amax(arr)

time.sleep(5)




