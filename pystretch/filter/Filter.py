import numpy
from scipy import signal
from scipy import ndimage

def conservative_filter(shared_array, i, **kwargs):
    kernel_size = kwargs['kernel_size']
    def _minormax(arr):
        size = len(arr)
        element = size / 2
        if arr[element] > numpy.amax(arr):
            arr[element] = numpy.amax(arr)
        elif arr[element] < numpy.amin(arr):
            arr[element] = numpy.amin(arr)
        return arr[element]
    shared_array[i] = ndimage.generic_filter(shared_array[i], _minormax, size=kernel_size)

def createkernel(size):
    size = (size, size)
    kernel = numpy.ones(size)
    return kernel

def gaussian_filter(shared_array, i, **kwargs):
    kernel_size = kwargs['kernel_size']
    shared_array[i] = ndimage.gaussian_filter(shared_array[i], kernel_size)

def gaussian_hipass(shared_array, i, **kwargs):
    kernel_size = kwargs['kernel_size']
    gaussian_filter = ndimage.gaussian_filter(shared_array[i], kernel_size)
    shared_array[i] = shared_array[i] - gaussian_filter

def hipass_filter_3x3(shared_array, i, **kwargs):
    kernel = numpy.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])
    shared_array[i] = ndimage.convolve(shared_array[i], kernel)

def hipass_filter_5x5(shared_array, i, **kwargs):
    kernel = numpy.array([[-1,-1,-1, -1, -1],[-1, 1, 2, 2, -1],[-1,2,4,2,-1],[-1,1,2,1,-1],[-1,-1,-1, -1, -1]])
    shared_array[i] = ndimage.convolve(shared_array[i], kernel)

def laplacian_filter(shared_array, i, **kwargs):
    laplacian = numpy.array([[0,1,0],[1,-4,1],[0,1,0]],numpy.float64) #Created once per processor, but overhead should be small.
    shared_array[i] = ndimage.filters.correlate(shared_array[i], laplacian, mode='nearest')


def mean_filter(shared_array, i, **kwargs):
    kernel_size = kwargs['kernel_size']
    kernel = createkernel(kernel_size)
    kernel *= 1/float(kernel_size)
    shared_array[i] = ndimage.filters.correlate(shared_array[i], kernel, mode='nearest')


def median_filter(shared_array, i, **kwargs):
    shared_array[i] = signal.medfilt(shared_array[i], kwargs['kernel_size'])
