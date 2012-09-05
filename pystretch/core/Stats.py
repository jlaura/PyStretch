import numpy
import gc
import time


_datatype_integer_ranges = {
    'Byte' : [0, 255],
    's8' : [-128,127],
    'UInt16' : [0, 65535],
    'Int16' : [-32768, 32767],
    'UInt32' : [0, 4294967295],
    'Int32' : [-2147483648, 2147483647],
    'Float32' : [-3.402823466**38, 3.402823466**38 ]
    }

_gdal_to_numpy = { 'Byte': numpy.int8,
                   'Int16' : numpy.int16,
                   'UInt16' : numpy.uint16,
                   'Int32' : numpy.int32,
                   'UInt32' : numpy.uint32,
                   'Float32' : numpy.float32 
                   }

def datatype(dtype):
    
    '''Function to convert from data type name to numpy.dtype
    
    For example, gdal.GetDataTypeName(raster.GetRasterBand(1) returns Float32

    This function converts that to numpy.float32.  This function exists only because 
    simple string methods are insufficient to convert from Float32 to numpy.float32
    '''
    
    arraytype = _gdal_to_numpy[dtype]
    
    return arraytype

def denorm(array, dtype, kwargs):

    #Do not attempt to rescale the histogram equalization
    if kwargs['histequ_stretch'] == True:
        pass
    
    #We do not normalize float, so do not rescale
    elif dtype == 'Float32':
        pass
    
    #Everything else needs to be rescaled
    else:
        for key, value in _datatype_integer_ranges.iteritems():
            if dtype == key:
                array *= value[1]
    del  array
    gc.collect()
    

def get_array_stats(array, stretch):
    '''
    Calculates the statistics from a numpy array and returns a dictionary containing:
    mean, maximum, minimum, and potentially standard deviation.
    
    Standard deviation is not calculated by devault as it duplicates the array in
    memory.  A fast implementation of the Welford Algorithm is being sought as a 
    replacement to numpy.std(array) or array.std()
    
    Returns a dictionary with mean, maximum, minimum, and possibly standard deviation
    '''
    stats = {}
    stats['mean'] = float(array.mean())
    stats['maximum'] = float(array.max())
    stats['minimum'] = float(array.min())
    gc.collect()
    #Standard Deviation takes a few seconds to calculate.  Skip it if you do not need it. Worse - numpy.std makes an in memory copy of the array...
    try:
        if stretch.__name__ == 'standard_deviation_stretch' or 'gaussian_stretch':
            #TODO Look at fast implementations of the Welford Algorithm
            std = array.std()
            stats['standard_deviation'] = float(std)
            del std
    except:
        pass
    
    del array
    gc.collect()
    return stats

def get_band_stats(band):
    
    '''
    Get the pre-cached statistics from the input band.
    
    Returns a dictionary with bandmin, bandmax, bandstd, ndv.
    '''
    
    stat = band.GetStatistics(False, True)
    ndv = band.GetNoDataValue()
    stats = {'bandmin' : stat[0],
          'bandmax' : stat[1],
          'bandmean' : stat[2],
          'bandstd' : stat[3],
          'ndv_band' : ndv
          }
    return stats

def gethist_cdf(array,num_bins):
    '''
    This function calculates the cumulative distribution function of a given array and requires that both the input array and the number of bins be provided.
    
    Returns: cumulative distribution function, bins
    '''
    hist, bins = numpy.histogram(array.flatten(), num_bins, density=False)
    cdf = hist.cumsum()
    cdf ** 0.5
    cdf = 256 * cdf / cdf[-1] #This needs to have a dtype lookup (16bit would be 2**16-1)
    return cdf, bins

def maskNDV(array, NDV):
    '''
    This function masks the no data values in an input array so that they are not included in
    any of the processing algorithms.  This is essential to ensure that statistics are calculated properly at the array level.

    Returns an array of type numpy.ma.masked.  This is NOT an ndarray.
    '''
    
    array = numpy.ma.masked_where(array == NDV, input_array, copy=False)
    return array

def normalize(array, bandmin, bandmax, dtype):
    '''
    This function normalizes a data set to between 0-1
    
    We normalize the dataset for a number of reasons:
        1. To avoid divide by zero errors
        2. To prepare for certain stretches that require values between -1 and 1
        
    We do not normalize float because the rounding errors are too large and skew a lot of the calculations

    Returns a normalized array
    '''
    
    if dtype == 'Float32':
        pass
    #If the data type is unsigned, normalize to between 0 and 1
    else:
        array -= bandmin
        array *= 1/(bandmax-bandmin)   

    #If the data type is signed, normalize to between -1 and 1
    #datarange = 2 / (bandmax - bandmin)
    #array *= datarange - 1
    #array = (array - ((bandmax-bandmin)/2))/((bandmax-bandmin)/2)
    return array

def scale(array, kwargs):
    '''
    This function is used to scale the data between a user defined range [c,d].  By default this range is between 1 and 255.  This maintains 0 as a special no data value should the user wish to set it.
    
    Scale from (a,b) to c,d)
        y = mx+b
        x = ((x-a)(d-c)/(b-a))+c
        
    Returns a scaled ndarray
    '''
    if kwargs['scale'] == None:
        scalemin = 1.0
        scalemax = 255.0
    else:
        scalemin = float(kwargs['scale'][0])
        scalemax = float(kwargs['scale'][1])
    #Unpack the scalemin and scalemax variables if they exist
    #array = ((array-kwargs['bandmin'])*(scalemax-scalemin)/(kwargs['bandmax']-kwargs['bandmin']))+scalemin
    array -= kwargs['bandmin']
    array *= (scalemax-scalemin)
    array *= 1/(kwargs['bandmax']-kwargs['bandmin'])
    array += scalemin
    return array

def setnodata(shared_arr, ndv):
    '''
    This function sets the numpy nan, presumed to be a masked no data value to either the input datasets no data value or a user specified no data value.
    
    Returns an ndarray with NaN replaced with the defined no data value.
    '''
    if ndv != None:
        arr = shared_arr.asarray()
        arr = numpy.nan_to_num(ndv)
        return arr
    else:
        pass

