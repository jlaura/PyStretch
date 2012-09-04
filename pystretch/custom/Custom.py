'''This module exists so that you, the user, can implement your own stretching or filtering algorithms.  The first function, linear_stertch, is an exact copy the linear stretch function found in the linear module.  It is included solely for demonstration purposes.

To implement your own algorithm, simply code it (in python) in the blank space provided in the custom_stretch function.  A flag has already been added to the option parser for you, so that you can start using your new stretch immediately.  To do that you could use the pystertcher.py script like so:

$ pystretcher.py --custom

As long as the --custom flag is included, your algorithm will be used with all of the existing segmentation, no data value, spatial data propogation, and scaling functionality.

Please consider contributing your algorithm (or implementation of an existing algorithm with a citation) to http://github.com/jlaura/PyStretch
'''

#Imports go here.  Likely imports are included
import numpy

def linear_stretch(shared_array, i,**kwargs):
    '''This is the doc string, which is used to document the algorithm, show the citiation, and include other helpful information for the user.  If your algorithm is included in a release, the doc string will be automatically parsed to generate documentation. '''
    
    
    '''Browsing the internet we find an interesting stretch - the linear contrast stretch.  We find an algorithm that states:
    
    Pixel_out = (Pixel_in - c)(b-a/d-c) + a, where:
    
    a is the minimum pixel value of the input image
    b is the maximum pixel value of the input image
    c is the minimum pixel value of the desired output range
    d is the maximum pixel value of the desired output range
    Pixel_in is the input pixel value
    Pixel_out is the modified, output pixel value.
    
    PySTRETCH already stores the input min and input max in the options dict for us, so no need to calculate them.
    
    '''
    #First we take options from the kwargs dictionary that our stretch needs access to.
    #In this case we need to know the percentage clip, as well as the minimum and maximum values.
    clip = kwargs['clip']
    minimum = kwargs['minimum']
    maximum = kwargs['maximum']
    
    #Because we are working with a shared memory array, we need to get a view of the array
    # that numpy can read.  This line exists in custom_stretch, simply uncomment.
    arr = shared_array.asarray()    
    
    #For this stretch we need to calculate the new minimum and maximum values to 
    # stretch the array to.  We perform those calculations here.
    newmin = minimum * ((100.0-clip)/100.0)
    newmax = maximum * ((100.0-clip)/100.0)
    
    #Now we iterate over the array and apply the stretching algorithm.
    #arr[i] is used instead of just arr since we are multiprocessing and only want each 
    # process to be able to access a specific segment of the shared array.  Which segment
    # is handled by the main script so you do not have to worry about it.
    arr[i] -= newmin
    arr[i] *=((newmax - newmin)/(maximum-minimum)) + newmin
    
    '''
    Memory management is an issue, so we need to make sure that in-memory copies of an array are not generated.  Unfortunately, numpy really likes to make in memory copies.  To overcome this, we utilize in place manipulation.  Here is an example using the logic above.
    
    We could write: 
        
    arr[i] -= newmin 
    
    as
    
    arr[i] = arr[i] - newmin
    
    Unfortunately, that would cause a short lived in memory copy to be made.
    
    Here are a few additional hints:
    - Notation is arr[i] += or -= or *=
    - If you have to divide, multiply by the inverse a la, 
        arr[i] *= 1/whatever_you_need_to_multiply_by
    '''
    
def custom_stretch(shared_array, i, **kwargs):

    #Pull your arguments, from **kwargs here.
    
    #Uncomment the line below to access the image array segments
    #arr = shared_array.asarray()
    
    #Perform any stretch logic with the arguments.  This is logic which does not interact 
    # directly with the array, but which is essential to later iterating over the array elements
    
    #Finally, include your array manipulaiton logic here.  No need for a return call, we are
    # manipulating the array in shared memory space with a scope outside this function
    
    #Remember to avoid in memory array duplication
    
    #Finally, delete the 'pass' below
    pass
