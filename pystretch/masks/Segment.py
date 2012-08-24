import numpy

def segment_image(xsize, ysize, xsegment=1, ysegment=1):
    """Function to segment the images into a user defined number of sections and store the segment dimensions in a dictionary.
    
    We assume that the image has the same dimensions, with the same pixel size in every band.  This may not hold true for formats like JP2k."""

        
    intervalx = xsize / xsegment
    intervaly = ysize / ysegment

    #Setup to segment the image storing the start values and key into a dictionary.
    xstart = 0
    ystart = 0
    output = []
    
    for y in xrange(0, ysize, intervaly):
        numberofrows = intervaly if y + (intervaly * 2) < ysize else ysize -y
        for x in xrange(0, xsize, intervalx):
            numberofcolumns = intervalx if x + (intervalx * 2) < xsize else xsize -x
            tple = (x,y,numberofcolumns, numberofrows)
            output.append(tple)    
    return output
    

    

