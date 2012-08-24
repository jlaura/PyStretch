import numpy

def linear_stretch(shared_array, i,**kwargs):
    clip = kwargs['clip']
    minimum = kwargs['minimum']
    maximum = kwargs['maximum']
    newmin = minimum * ((100.0-clip)/100.0)
    newmax = maximum * ((100.0-clip)/100.0)
    arr = shared_array.asarray()
    arr[i] -= newmin
    arr[i] *=((newmax - newmin)/(maximum-minimum)) + newmin

def standard_deviation_stretch(shared_array, i,**kwargs):
    array_mean = kwargs['mean']
    array_standard_deviation = kwargs['standard_deviation']
    sigma = kwargs['sigma']
    newmin = array_mean - (array_standard_deviation * sigma)
    newmax = array_mean + (array_standard_deviation * sigma)
    arr = shared_array.asarray()
    arr[i] -= newmin
    arr[i] *= 1.0/(newmax-newmin)
    
def inverse_stretch(shared_array, i, **kwargs):
    maximum = kwargs['maximum']
    arr = shared_array.asarray()
    arr[i] -= maximum
    arr[i] = abs(arr[i])

def binary_stretch(shared_array, i, **kwargs):
    threshold = kwargs['threshold']
    #Normalize the threshold value because we normalized our data
    threshold = (threshold - kwargs['bandmin'])/(kwargs['bandmax']-kwargs['bandmin'])
    arr = shared_array.asarray()
    low_value_index = arr[i] < threshold
    arr[i][low_value_index] = 0.0
    high_value_index = arr[i] > threshold
    arr[i][high_value_index] = 255.0
    
def hicut_stretch(shared_array, i, **kwargs):
    threshold = kwargs['cutvalue']
    threshold = (threshold - kwargs['bandmin'])/(kwargs['bandmax']-kwargs['bandmin'])
    arr = shared_array.asarray()
    high_value_index = arr[i] > threshold
    arr[i][high_value_index] = kwargs['cutvalue']
    
def lowcut_stretch(shared_array, i, **kwargs):
    threshold = kwargs['cutvalue']
    threshold = (threshold - kwargs['bandmin'])/(kwargs['bandmax']-kwargs['bandmin'])
    arr = shared_array.asarray()
    low_value_index = arr[i] < threshold
    arr[i][low_value_index] = kwargs['cutvalue']