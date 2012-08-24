"""
GdalIO to provide read and write capabilities leveraging GDAL.
All GDAL supported file formats are supported via this FileIO.
Consult the GDAL documentation for your version for a listing of the supported file formats.
"""
from osgeo import gdal

# set up some default nodatavalues for each datatype
DefaultNDVLookup={'Byte':255, 'UInt16':65535, 'Int16':-32767, 'UInt32':4294967293, 'Int32':-2147483647, 'Float32':1.175494351E-38, 'Float64':1.7976931348623158E+308}


class GdalIO(object):
    
    def __init__(self, inputdataset):
        """Method docstring"""
        self.inputds = inputdataset
    
    def load(self):
        """Method to open any GDAL supported raster dataset"""

        #Open the dataset read only using GDAL
        dataset = gdal.Open(self.inputds, gdal.GA_ReadOnly)
        
        return dataset
    

            #print "Failed to open %s. Is it a GDAL supported format?" %(self.inputds)

    def info(self,dataset):
        xsize = dataset.RasterXSize
        ysize = dataset.RasterYSize
        bands = dataset.RasterCount
        projection = dataset.GetProjection()
        geotransform = dataset.GetGeoTransform()
        
        return xsize, ysize, bands, projection, geotransform
    
    def create_output(self,driverformat, outputname,xsize,ysize,bands,projection, geotransform, dtype):

        """Method to create an output of the same type, size, projection, and transformation as the input dataset"""

        if not outputname:
            outputname = "output.tif"
            
        if not driverformat:
            driverFormat = 'Gtiff'

        driver = gdal.GetDriverByName(driverFormat)
        outdataset = driver.Create(outputname, xsize, ysize, bands,dtype)
        outdataset.SetProjection(projection)
        outdataset.SetGeoTransform(geotransform)
        
        return outdataset