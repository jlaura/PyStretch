#!/usr/bin/env python

#Internal imports
from pystretch.core import OptParse, Stats, Timer
from pystretch.core.GdalIO import OpenDataSet, create_output
from pystretch.masks import Segment
import pystretch.core.globalarr as glb
from pystretch.core import maskndv


#Debugging imports
#import profile
#Core imports

import multiprocessing as mp
import ctypes
import sys
import time
import gc

#External imports
try:
    from osgeo import gdal
    from osgeo.gdalconst import *
    version_num = int(gdal.VersionInfo('VERSION_NUM'))
    if version_num <1800 :
        print 'ERROR: Python bindings of GDAL version 1.8.0 or later required'
        raise
    else:
        pass
except ImportError:
    print "GDAL and the GDAL python bindings must be installed."
    raise

try:
    import numpy as np
except ImportError:
    print "NumPY must be installed."
    raise

try:
    import scipy
except ImportError:
    print "Some functionality will not work without scipy installed."


_gdal_to_ctypes = {1:ctypes.c_short}
_gdal_to_numpy = {1:np.int16}

_ctypes_to_np = {
    ctypes.c_char : np.int8,
    ctypes.c_wchar : np.int16,
    ctypes.c_byte : np.int8,
    ctypes.c_ubyte : np.uint8,
    ctypes.c_short : np.int16,
    ctypes.c_ushort : np.uint16,
    ctypes.c_int : np.int32,
    ctypes.c_uint : np.int32,
    ctypes.c_long : np.int32,
    ctypes.c_ulong : np.int32,
    ctypes.c_float : np.float32,
    ctypes.c_double : np.float64
}


def standard_deviation_stretch(i, kwargs):

    array_mean = kwargs['mean']
    array_standard_deviation = kwargs['standard_deviation']
    sigma = kwargs['sigma']
    newmin = array_mean - (array_standard_deviation * sigma)
    newmax = array_mean + (array_standard_deviation * sigma)

    #arr = shared_array.asarray()
    sharedarray[i] -= newmin
    sharedarray[i] *= 1.0/(newmax-newmin)


def segment_image(xsize, ysize, xsegment, ysegment):
    """Function to segment the images into a user defined number of sections
    and store the segment dimensions in a tuple.

    We assume that the image has the same dimensions, with the same pixel
    size in every band.  This may not hold true for formats like JP2k."""

    if xsegment is None:
        xsegment = 1
    if ysegment is None:
        ysegment = 1

    intervalx = xsize / xsegment
    intervaly = ysize / ysegment

    #Setup to segment the image storing the start values and key into a dictionary.
    xstart = 0
    ystart = 0
    output = []
    for y in xrange(0, ysize, intervaly):
        if y + intervaly * 2 <= ysize:
            numberofrows = intervaly
        else:
            numberofrows = ysize - y
        for x in xrange(0, xsize, intervalx):
            if x + intervalx * 2 <= xsize:
                numberofcolumns = intervalx
            else:
                numberofcolumns = xsize - x
            output.append((x,y,numberofcolumns, numberofrows))
    return output




def main(args):
    starttime = Timer.starttimer()
    #Cache thrashing is common when working with large files
    # we help alleviate misses by setting a larger than normal cache.  1GB

    gdal.SetCacheMax(1073741824)

    #Get stretch type
    stretch = OptParse.argget_stretch(args)

    #Get some info about the machine for mp
    cores = args['ncores']
    if cores is None:
        cores = mp.cpu_count()

    #Load the input dataset using the GdalIO class and get / set the output datatype.
    dataset = OpenDataSet(args['input'])
    raster = dataset.load()
    xsize, ysize, nbands, projection, geotransform = dataset.info(raster)


    #Get band information
    bands = [raster.GetRasterBand(b) for b in range(1, nbands + 1)]
    bandstats = [Stats.get_band_stats(b) for b in bands]
    b = bands[0]
    banddtype = b.DataType
    blocksize = b.GetBlockSize()
    xblocksize = blocksize[0]
    yblocksize = blocksize[1]

    output = create_output(args['outputformat'],args['output'],
                        xsize, ysize, len(bands), projection,
                        geotransform, gdal.GetDataTypeByName(args['dtype']))

    #Intelligently segment the image based upon number of cores and intrinsic block size
    if args['horizontal_segments'] is not None or args['vertical_segments'] is not None:
        #The user is defining the segmentation
        segments = segment_image(xsize, ysize, args['vertical_segments'],args['horizontal_segments'])
    else:
        segments = [(0,0,xsize, ysize)]

    carray_dtype = _gdal_to_ctypes[banddtype]
    #Preallocate a sharedmem array of the correct size
    ctypesxsize, ctypesysize= segments[0][2:]
    carray = mp.RawArray(carray_dtype, ctypesxsize * ctypesysize)
    glb.sharedarray = np.frombuffer(carray,dtype=_gdal_to_numpy[banddtype]).reshape(ctypesysize, ctypesxsize)

    pool = mp.Pool(processes=cores, initializer=glb.init, initargs=(glb.sharedarray, ))

    #A conscious decision to iterate over the bands in serial - a IO bottleneck anyway
    for j,band in enumerate(bands):
        stats = bandstats[j]
        args.update(stats)

        for i, chunk in enumerate(segments):
            xstart, ystart, intervalx, intervaly = chunk
            #Read the array into the buffer
            glb.sharedarray[:] = band.ReadAsArray(xstart, ystart, intervalx, intervaly)
            #If the input has an NDV - mask it.
            if stats['ndv'] != None:
                glb.sharedarray = np.ma.masked_equal(glb.sharedarray, stats['ndv'], copy=False)
                mask = np.ma.getmask(glb.sharedarray)
            if args['statsper'] is True:
                args.update(Stats.get_array_stats(glb.sharedarray, stretch))

            #Determine the decomposition for each core
            step = glb.sharedarray.shape[0] // cores
            starts = range(ystart, ysize, step)

            stops = starts[1:]
            stops.append(ysize-1)
            offsets = zip(starts, stops)
            for o in offsets:
                res = pool.apply_async(stretch, args=(slice(o[0], o[1]), args))

            res.wait()
            res.get()



            """

            #Calculate the hist and cdf if we need it.  This way we do not calc it per core.
            if options['histequ_stretch'] == True:
                cdf, bins = Stats.gethist_cdf(array,options['num_bins'])
                options['cdf'] = cdf
                options['bins'] = bins


            step = y // cores
            jobs = []
            if step != 0:
                for i in range(0,y,step):
                    p = mp.Process(target=stretch,args= (shared_arr,slice(i, i+step)),kwargs=options)
                    jobs.append(p)

                for job in jobs:
                    job.start()
                    del job
                for job in jobs:
                    job.join()
                    del job

            #Return the array to the proper data range and write it out.  Scale if that is what the user wants
            if options['histequ_stretch'] or options['gamma_stretch']== True:
                pass
            elif 'filter' in stretch.__name__:
                pass
            else:
                Stats.denorm(shared_arr, dtype, kwargs=options)

            if options['scale'] != None:
                Stats.scale(shared_arr, kwargs=options)

            #If their are NaN in the array replace them with the dataset no data value
            Stats.setnodata(shared_arr, options['ndv'])
            """
            #Write the output

            """
            #Manually cleanup to stop memory leaks.
            del array, jobs, shared_arr
            try:
                del stats
            except Exception:
                pass
            globals()['shared_arr'] = None
            gc.collect()
            """
            if args['ndv'] != None:
                glb.sharedarray[mask] = args['ndv']
                output.GetRasterBand(j+1).SetNoDataValue(float(args['ndv']))



            output.GetRasterBand(j+1).WriteArray(glb.sharedarray, xstart,ystart)


    Timer.totaltime(starttime)

    #Close up
    dataset = None
    output = None
    gc.collect()

def init(shared_arr_):
    global sharedarray
    sharedarray = shared_arr_ # must be inhereted, not passed as an argument global array

if __name__ == '__main__':
    mp.freeze_support()
    #If the script is run via the command line we start here, otherwise start in main.
    #(options, args) = OptParse.parse_arguments()
    #gdal.SetConfigOption('CPL_DEBUG', 'ON')

    main(OptParse.argparse_arguments())
