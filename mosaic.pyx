import numpy as np
cimport numpy as np
cimport cython

np.import_array()

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def idxarr(float [:,:] src):
    cdef int x, y, xsize, ysize
    cdef int c = 1
    xsize = src.shape[1]
    ysize = src.shape[0]

    ididx = np.zeros((src.shape[0], src.shape[1]), dtype=np.int)


    for x in range(xsize):
        for y in range(ysize):
            if src[y, x] != 0:
                ididx[y, x] = c
                c += 1
    return ididx, c

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def genAb(float [:,:] src,
          float [:,:] srclap,
          long [:,:] imidx,
          float [:,:] dest,
          int n):
    """
    This is a gigantic laplacian filter the the destination image
    """
    cdef int count, x, y, xsize, ysize, colidx


    xsize = src.shape[1]
    ysize = src.shape[0]
    A = np.empty((n,n))
    b = np.zeros(n, dtype=np.float64)
    sol = np.zeros(n, dtype=np.float64)
    print n, xsize * ysize
    count = 1
    print "Generating A and b"
    for x in range(1, xsize-1):
        for y in range(1, ysize-1):
            if src[y,x] != 0.0:
                #Upper pixel
                if src[y-1, x] != 0:
                    colidx = imidx[y - 1, x]
                    A[count, colidx] = -1
                else:
                    b[count] = b[count] + dest[y-1, x]
                if src[y, x-1] != 0:
                    colidx = imidx[y, x - 1]
                    A[count, colidx] = -1
                else:
                    b[count] = b[count] + dest[y, x-1]
                if src[y+1, x] != 0:
                    colidx = imidx[y+1, x]
                    A[count, colidx] = -1
                else:
                    b[count] = b[count] + dest[y+1, x]
                if src[y, x+1] != 0:
                    colidx = imidx[y, x + 1]
                    A[count, colidx] = -1
                else:
                    b[count] = b[count] + dest[y, x+1]
                A[count, count] = 4
                b[count] = b[count] + srclap[y,x]
                count += 1
    return A, b

