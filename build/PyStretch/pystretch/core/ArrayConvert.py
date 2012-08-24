import ctypes
import numpy
from multiprocessing import RawArray


_ctypes_to_numpy = {
    ctypes.c_char : numpy.int8,
    ctypes.c_wchar : numpy.int16,
    ctypes.c_byte : numpy.int8,
    ctypes.c_ubyte : numpy.uint8,
    ctypes.c_short : numpy.int16,
    ctypes.c_ushort : numpy.uint16,
    ctypes.c_int : numpy.int32,
    ctypes.c_uint : numpy.int32,
    ctypes.c_long : numpy.int32,
    ctypes.c_ulong : numpy.int32,
    ctypes.c_float : numpy.float32,
    ctypes.c_double : numpy.float64
}


_numpy_to_ctypes = dict((value, key) for key, value in
                                _ctypes_to_numpy.iteritems())

class SharedMemArray(object):
    """ Wrapper around multiprocessing.Array to share an array accross
        processes.
        
        From: http://www.alexfb.com/cgi-bin/twiki/view/PtPhysics/WebHome
    """

    def __init__(self, array):
        """ Initialize a shared array from a numpy array.

            The data is copied.
        """
        self.data = ndarray_to_shmem(array)
        self.dtype = array.dtype
        self.shape = array.shape

    def __array__(self):
        """ Implement the array protocole.
        """
        array = shmem_as_ndarray(self.data, dtype=self.dtype)
        array.shape = self.shape
        return array
 
    def asarray(self):
        return self.__array__()
    
    
def shmem_as_ndarray(data, dtype=float):
    """ Given a multiprocessing.Array object, as created by
    ndarray_to_shmem, returns an ndarray view on the data.
    """
    dtype = numpy.dtype(dtype)
    size = data._wrapper.get_size()/dtype.itemsize
    arr = numpy.frombuffer(buffer=data, dtype=dtype, count=size)
    return arr


def ndarray_to_shmem(array):
    """ Converts a numpy.ndarray to a multiprocessing.Array object.
    
        The memory is copied, and the array is flattened.
    """
    arr = array.reshape((-1, ))
    data = RawArray(_numpy_to_ctypes[array.dtype.type], 
                                        arr.size)
    ctypes.memmove(data, array.data[:], len(array.data))
    return data

