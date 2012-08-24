import numpy
from scipy import signal
from scipy import ndimage

def conservative_filter(shared_array, i, **kwargs):
    kernel_size = kwargs['kernel_size']
    arr = shared_array.asarray()
    def _minormax(arr):
        size = len(arr)
        element = size / 2
        if arr[element] > numpy.amax(arr):
            arr[element] = numpy.amax(arr)
        elif arr[element] < numpy.amin(arr):
            arr[element] = numpy.amin(arr)
        return arr[element] 
    arr[i] = ndimage.generic_filter(arr[i], _minormax, size=kernel_size)
    
def createkernel(size):
    size = (size, size)
    kernel = numpy.ones(size)
    return kernel

def gaussian_filter(shared_array, i, **kwargs):
    kernel_size = kwargs['kernel_size']
    arr = shared_array.asarray()
    arr[i] = ndimage.gaussian_filter(arr[i], kernel_size)

def gaussian_hipass(shared_array, i, **kwargs):
    kernel_size = kwargs['kernel_size']
    arr = shared_array.asarray()
    gaussian_filter = ndimage.gaussian_filter(arr[i], kernel_size)
    arr[i] = arr[i] - gaussian_filter

def hipass_filter_3x3(shared_array, i, **kwargs):
    arr=shared_array.asarray()
    kernel = numpy.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])
    arr[i] = ndimage.convolve(arr[i], kernel)    
    
def hipass_filter_5x5(shared_array, i, **kwargs):
    arr=shared_array.asarray()
    kernel = numpy.array([[-1,-1,-1, -1, -1],[-1, 1, 2, 2, -1],[-1,2,4,2,-1],[-1,1,2,1,-1],[-1,-1,-1, -1, -1]])
    arr[i] = ndimage.convolve(arr[i], kernel)

def laplacian_filter(shared_array, i, **kwargs):
    arr = shared_array.asarray()
    laplacian = numpy.array([[0,1,0],[1,-4,1],[0,1,0]],numpy.float64) #Created once per processor, but overhead should be small.
    arr[i] = ndimage.filters.correlate(arr[i], laplacian, mode='nearest')


def mean_filter(shared_array, i, **kwargs):
    kernel_size = kwargs['kernel_size']
    kernel = createkernel(kernel_size)
    kernel *= 1/float(kernel_size)
    arr = shared_array.asarray()
    arr[i] = ndimage.filters.correlate(arr[i], kernel, mode='nearest')

    
def median_filter(shared_array, i, **kwargs):
    arr = shared_array.asarray()
    arr[i] = signal.medfilt(arr[i], kwargs['kernel_size'])
