import numpy as np
import pystretch.core.globalarr as glb

def minmax_stretch( i, kwargs):
    """
    Rescale image pixels between a user defined minimum and maximum
    """
    minimum = kwargs['minimum']
    maximum = kwargs['maximum']
    a = kwargs['minmax'][0]
    b = kwargs['minmax'][1]

    glb.sharedarray[i] = (b-a) * (glb.sharedarray[i]  - minimum) / (maximum - minimum) + a

def clip_stretch(i,kwargs):
    """
    Recale image pixels between a minimum and maximum defined as some percentage from
    the existing minimum and maximum.
    """
    clip = kwargs['clip']
    minimum = kwargs['minimum']
    maximum = kwargs['maximum']
    a = minimum * ((100.0-clip)/100.0)
    b = maximum * ((100.0-clip)/100.0)

    glb.sharedarray[i] = (b-a) * (glb.sharedarray[i]  - minimum) / (maximum - minimum) + a

def standard_deviation_stretch(i, kwargs):
    print i, glb.sharedarray[:,i].shape
    """
    Rescale image pixels between a minimum and maximum defined by some number
    of standard deviation from the mean.
    """

    if kwargs['byline'] is True or kwargs['bycolumn'] is True:
        array_mean = glb.sharedarray[:,i].mean()
        array_standard_deviation = glb.sharedarray[:,i].std()
    else:
        array_mean = kwargs['mean']
        array_standard_deviation = kwargs['standard_deviation']
    sigma = kwargs['sigma']
    newmin = array_mean - (array_standard_deviation * sigma)
    newmax = array_mean + (array_standard_deviation * sigma)

    glb.sharedarray[:,i] -= newmin
    glb.sharedarray[:,i] *= kwargs['maximum']/(newmax-newmin)
def inverse_stretch(i, kwargs):
    """
    Invert an image by subtracting the maximum and the adding
    the minimum to the absolute value of the image.
    """
    maximum = kwargs['maximum']
    minimum = kwargs['minimum']
    glb.sharedarray[i] -= maximum
    glb.sharedarray[i] = abs(glb.sharedarray[i]) + minimum

def binary_stretch(i, kwargs):
    """
    Reclassify an image with all values greater than the pivot
    set to the image maximum and all values less than or equal
    to the pivot set to the minimum.
    """
    threshold = kwargs['binary_pivot']
    low_value_index = glb.sharedarray[i] < threshold
    glb.sharedarray[i][low_value_index] = kwargs['minimum']
    high_value_index = glb.sharedarray[i] >= threshold
    glb.sharedarray[i][high_value_index] = kwargs['maximum']

def hicut_stretch(i, kwargs):
    """
    Reclassify an image with all values greater than the pivot
    set the the image maximum.  All other pixels are unchanged.
    """
    high_value_index = glb.sharedarray[i] > kwargs['hicut_pivot']
    glb.sharedarray[i][high_value_index] = kwargs['maximum']

def lowcut_stretch(i, kwargs):
    """
    Reclassify an image with all values less than the pivot
    set to the image minimum.  All other pixels are unchanged
    """
    low_value_index = glb.sharedarray[i] < kwargs['lowcut_pivot']
    glb.sharedarray[i][low_value_index] = kwargs['minimum']
