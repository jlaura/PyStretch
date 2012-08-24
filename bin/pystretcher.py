#!/usr/bin/env python

#Internal imports
from pystretch.core import GdalIO, ArrayConvert, OptParse, Stats, Timer
from pystretch.masks import Segment

#Debugging imports
#import profile


#Core imports
import multiprocessing
from contextlib import closing
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
    import numpy
except ImportError:
    print "NumPY must be installed."
    raise

try:
    import scipy
except ImportError:
    print "Some functionality will not work without scipy installed."

    
def main(options, args):
    starttime = Timer.starttimer()
    #Cache thrashing is common when working with large files, we help alleviate misses by setting a larger than normal cache.  1GB
    gdal.SetCacheMax(1073741824)

    #Check for input
    if not args:
        print "\nERROR: You must supply an input data set.\n"
        sys.exit(0)
    
    #Get stretch type
    stretch = OptParse.get_stretch(options)
    
    #Get some info about the machine for multiprocessing
    cores = multiprocessing.cpu_count()
    cores *= 2
    print "Processing on %i cores." %cores
    
    #Load the input dataset using the GdalIO class and get / set the output datatype.
    dataset = GdalIO.GdalIO(args[0])
    raster = dataset.load()

    #Default is none, unless user specified
    if options['dtype'] == None:
        dtype = raster.GetRasterBand(1).DataType
    else:
        dtype=gdal.GetDataTypeByName(options['dtype'])
        
    #Create an output if the stretch is written to disk
    xsize, ysize, bands, projection, geotransform = dataset.info(raster)
    output = dataset.create_output("",options['output'],xsize,ysize,bands,projection, geotransform, dtype)

    #Segment the image to handle either RAM constraints or selective processing
    segments = Segment.segment_image(xsize,ysize,options['vint'], options['hint'])

    for b in xrange(bands):

        band = raster.GetRasterBand(b+1)
        dtype = gdal.GetDataTypeName(band.DataType)
        bandstats = Stats.get_band_stats(band)
        for key in bandstats.iterkeys():
            options[key] = bandstats[key]            
        print "Read band %i of %i" %(b+1, bands)
        
        #Get the size of the segments to be manipulated
        piecenumber = 1
        for chunk in segments:
            
            print "Image segmented.  Processing segment %i of %i" %(piecenumber, len(segments))
            piecenumber += 1
            (xstart, ystart, intervalx, intervaly) = chunk
            array = band.ReadAsArray(xstart, ystart, intervalx, intervaly).astype(numpy.float)
            if options['ndv'] != None:
                array = numpy.ma.masked_values(array, options['ndv'], copy=False)
            if 'stretch' in stretch.__name__:
                array = Stats.normalize(array, options['bandmin'], options['bandmax'], dtype)
            stats = Stats.get_array_stats(array, stretch) 
            for key in stats.iterkeys():
                options[key] = stats[key]
  
            y,x = array.shape
            
            #Calculate the hist and cdf if we need it.  This way we do not calc it per core.
            if options['histequ_stretch'] == True:
                cdf, bins = Stats.gethist_cdf(array,options['num_bins'])
                options['cdf'] = cdf
                options['bins'] = bins
            

            #Fill the masked values with NaN to get to a shared array
            if options['ndv'] != None:
                array = array.filled(numpy.nan)

            #Create an ctypes array
            init(ArrayConvert.SharedMemArray(array))
            
            
            step = y // cores
            jobs = []
            if step != 0:
                for i in range(0,y,step):        
                    p = multiprocessing.Process(target=stretch,args= (shared_arr,slice(i, i+step)),kwargs=options)
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
                Stats.denorm(shared_arr.asarray(), dtype, kwargs=options)

            if options['scale'] != None:
                Stats.scale(shared_arr.asarray(), kwargs=options)
                
            #If their are NaN in the array replace them with the dataset no data value
            Stats.setnodata(shared_arr, options['ndv'])

            #Write the output
            output.GetRasterBand(b+1).WriteArray(shared_arr.asarray(), xstart,ystart)            

            #Flush the GDAL cache to avoid band thrashing and cache misses
            output.GetRasterBand(b+1).FlushCache()
            band.FlushCache()

            #Manually cleanup to stop memory leaks.
            del stats,array, jobs, shared_arr.data, p
            del globals()['shared_arr']
            gc.collect()
            if options['ndv'] != None:
                output.GetRasterBand(b+1).SetNoDataValue(float(options['ndv']))

    if options['visualize'] == True:
        Plot.show_hist(shared_arr.asarray())
    
    Timer.totaltime(starttime)
    
    #Close up
    dataset = None
    output = None
    gc.collect()

def init(shared_arr_):
    global shared_arr
    shared_arr = shared_arr_ # must be inhereted, not passed as an argumentglobal array
    


if __name__ == '__main__':
    multiprocessing.freeze_support()
    #If the script is run via the command line we start here, otherwise start in main.
    (options, args) = OptParse.parse_arguments()
    #gdal.SetConfigOption('CPL_DEBUG', 'ON')

    main(options, args)
    
