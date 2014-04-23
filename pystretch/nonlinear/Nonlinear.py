import numpy as np
import pystretch.core.globalarr as glb


def gamma_stretch(i, kwargs):
    """
    Perform a gamma stretch raising all pixels to 1/epsilon.
    """
    glb.sharedarray[i] = np.power(glb.sharedarray[i], 1.0 / kwargs['gamma'])
    glb.sharedarray[i] *= kwargs['maximum']

def histequ_stretch(shared_array, i, kwargs):
    cdf = kwargs['cdf']
    bins = kwargs['bins']
    shape = shared_array[i].shape
    #interpolate
    shared_array[i] = numpy.interp(shared_array[i],bins[:-1],cdf)
    #reshape
    shared_array[i] = shared_array[i].reshape(shape)

def logarithmic_stretch(shared_array, i, kwargs):
    maximum = kwargs['maximum']
    epsilon = kwargs['epsilon']
    #Find the scaling constant
    c = 255/(numpy.log10(1+abs(maximum)))
    shared_array[i] = c * numpy.log10(epsilon + abs(shared_array[i]))

