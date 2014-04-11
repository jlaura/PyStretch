import numpy as np
import pystretch.core.globalarr as glb

def minmax_stretch( i, kwargs):
    minimum = kwargs['minimum']
    maximum = kwargs['maximum']
    a = kwargs['minmax'][0]
    b = kwargs['minmax'][1]
    mask = np.where(glb.sharedarray[:, i[0]:i[1]] == kwargs['ndv'])
    glb.sharedarray[:, i[0]:i[1]] = (b-a) * (glb.sharedarray[:, i[0]:i[1]]  - minimum) / (maximum - minimum) + a
    glb.sharedarray[mask] = kwargs['ndv']
    print np.min(glb.sharedarray), np.max(glb.sharedarray)


def linear_stretch(shared_array, i,**kwargs):
    clip = kwargs['clip']
    minimum = kwargs['minimum']
    maximum = kwargs['maximum']
    newmin = minimum * ((100.0-clip)/100.0)
    newmax = maximum * ((100.0-clip)/100.0)
    #arr = shared_array.asarray()
    shared_array[i] -= newmin
    shared_array[i] *=((newmax - newmin)/(maximum-minimum)) + newmin

def standard_deviation_stretch(i, kwargs):
    print "a"
    array_mean = kwargs['mean']
    array_standard_deviation = kwargs['standard_deviation']
    sigma = kwargs['sigma']
    newmin = array_mean - (array_standard_deviation * sigma)
    newmax = array_mean + (array_standard_deviation * sigma)
    #arr = shared_array.asarray()
    glb.sharedarray[i] -= newmin
    glb.sharedarray[i] *= 1.0/(newmax-newmin)

def inverse_stretch(shared_array, i, **kwargs):
    maximum = kwargs['maximum']
    minimum = kwargs['minimum']
    shared_array[i] -= maximum
    shared_array[i] = abs(shared_array[i]) + minimum

def binary_stretch(shared_array, i, **kwargs):
    threshold = kwargs['threshold']
    #Normalize the threshold value because we normalized our data
    threshold = (threshold - kwargs['bandmin'])/(kwargs['bandmax']-kwargs['bandmin'])
    low_value_index = shared_array[i] < threshold
    shared_array[i][low_value_index] = 0.0
    high_value_index = shared_array[i] > threshold
    shared_array[i][high_value_index] = 255.0

def hicut_stretch(shared_array, i, **kwargs):
    threshold = kwargs['cutvalue']
    threshold = (threshold - kwargs['bandmin'])/(kwargs['bandmax']-kwargs['bandmin'])
    high_value_index = shared_array[i] > threshold
    shared_array[i][high_value_index] = kwargs['cutvalue']

def lowcut_stretch(shared_array, i, **kwargs):
    threshold = kwargs['cutvalue']
    threshold = (threshold - kwargs['bandmin'])/(kwargs['bandmax']-kwargs['bandmin'])
    low_value_index = shared_array[i] < threshold
    shared_array[i][low_value_index] = kwargs['cutvalue']



def clip_stretch(shared_array, i, **kwargs):
    pass
