import numpy
import gc


_datatype_integer_ranges = {
    'Byte' : [0, 255],
    's8' : [-128,127],
    'UInt16' : [0, 65535],
    'Int16' : [-32768, 32767],
    'UInt32' : [0, 4294967295],
    'Int32' : [-2147483648, 2147483647],
    'Float32' : [-3.402823466**38, 3.402823466**38 ]
    }
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
    """Get statistics from the input array"""
    mean = array.mean()
    maximum = array.max()
    minimum = array.min()
    stats = {'mean':float(mean), 'maximum':float(maximum), 'minimum':float(minimum)}
    del maximum, minimum, mean
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
    """Get statistics from the input band, including the NoData Value"""
    ndv = band.GetNoDataValue()
    bandmin = band.GetMinimum()
    bandmax = band.GetMaximum()
    
    if bandmin is None or bandmax is None:
        #Approx has to be set to false to ensure that an accurate Min/Max are calculated...
        (bandmin, bandmax) = band.ComputeRasterMinMax(False)
    stats = {'ndv':ndv, 'bandmin':bandmin, 'bandmax':bandmax}
    return stats

def gethist_cdf(array,num_bins):
    hist, bins = numpy.histogram(array.flatten(), num_bins, density=False)
    cdf = hist.cumsum()
    cdf ** 0.5
    cdf = 256 * cdf / cdf[-1] #This needs to have a dtype lookup (16bit would be 2**16-1)
    return cdf, bins

def maskNDV(array, NDV):
    """Maks the NoData values in an array.  
    This is essential to ensure that statistics are calculated properly."""
    array = numpy.ma.masked_where(array == NDV, input_array, copy=False)
    return array

def normalize(array, bandmin, bandmax, dtype):
    """Normalize the dataset for a number of reasons:
        1. To avoid divide by zero errors
        2. To prepare for certain stretches that require values between -1 and 1 """
    #Do not normalize float, the rounding errors are too large and skew a lot of the calculations
    #TODO -  How can we handle float32 if we must normalize?
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
    '''Scale from (a,b) to c,d)
        y = mx+b
        x = ((x-a)(d-c)/(b-a))+c
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
    if ndv != None:
        arr = shared_arr.asarray()
        arr = numpy.nan_to_num(ndv)
        return arr
    else:
        pass

