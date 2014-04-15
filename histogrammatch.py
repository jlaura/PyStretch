import argparse
import numpy as np
from osgeo import gdal
import time

from scipy.interpolate import interp1d

import matplotlib.pyplot as plt


def histequalization(im, bins=256):
    shape = im.shape
    im = im.ravel()
    hist, bins = np.histogram(im.compressed(), bins=256, normed=True)
    cdf = hist.cumsum()
    cdf = 255 * cdf / cdf[-1]
    im_func = interp1d( bins[:-1], cdf, bounds_error=False)
    im = im_func(im)
    return im.reshape(shape), cdf, bins


def main(args):
    reference = args['reference']
    images = args['images']

    matchlist = []
    ds = gdal.Open(reference)
    projection = ds.GetProjection()
    geotransform = ds.GetGeoTransform()
    band = ds.GetRasterBand(1)
    ndv = band.GetNoDataValue()
    arr = band.ReadAsArray()

    plt.subplot(1,4,1)
    plt.imshow(arr, cmap='gray')

    arr = np.ma.masked_equal(arr, ndv, copy=False)

    arr, obscdf, bins = histequalization(arr)
    """
    plt.subplot(1,4,2)
    plt.imshow(arr, cmap='gray')

    plt.subplot(1,4,3)
    plt.plot(np.arange(256), obscdf)
    """
    invcdf = interp1d(obscdf, bins[:-1], bounds_error=False)

    driver = gdal.GetDriverByName('GTiff')

    x = np.arange(256)
    for i, im in enumerate(images):
        print "Processing image {} of {}".format(i + 1, len(images))
        outname = im.split('.')[0]
        outname += '_eq.tif'

        ds = gdal.Open(im)
        xsize = ds.RasterXSize
        ysize = ds.RasterYSize

        band = ds.GetRasterBand(1)
        ndv = band.GetNoDataValue()
        arr = band.ReadAsArray()

        arr = np.ma.masked_equal(arr, ndv, copy=False)
        arr = arr.ravel()
        hist, bins = np.histogram(arr.compressed(), bins=bins, normed=True)
        simcdf = np.cumsum(hist)
        simcdf = 255 * simcdf / simcdf[-1]


        #plt.plot(bins[:-1], obscdf, 'r-')
        #I need to use the obscdf here...
        transformation = invcdf(simcdf)
        #plt.plot(bins[:-1], transformation)

        tranfunc = interp1d(bins[:-1], transformation, bounds_error=False)
        arr = tranfunc(arr).reshape(ysize, xsize)

        """
        plt.subplot(1,4,4)
        plt.imshow(arr, cmap='gray')

        plt.show()
        return
        """
        projection = ds.GetProjection()
        geotransform = ds.GetGeoTransform()
        outdataset = driver.Create(outname, xsize,ysize,1,gdal.GDT_Byte, options = [ 'COMPRESS=LZW' ])
        outdataset.SetProjection(projection)
        outdataset.SetGeoTransform(geotransform)
        outdataset.GetRasterBand(1).SetNoDataValue(ndv)
        outdataset.GetRasterBand(1).WriteArray(arr)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(version='0.3')
    parser.add_argument('reference',
                        help='The reference image the histogram will match')
    parser.add_argument('images', nargs='*',
                       help='The images to be manipulated')

    args = vars(parser.parse_args())

    main(args)
