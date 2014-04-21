try:
    from osgeo import gdal
except ImportError:
    import gdal

try:
    progress = gdal.TermProgress_nocb
except:
    progress = gdal.TermProgress

import sys
import math
import numpy as np

import matplotlib.pyplot as plt

#from astropy.convolution import convolve
from scipy.ndimage import convolve
verbose = 1
quiet = 1

import pyximport
pyximport.install(reload_support=True, setup_args={"include_dirs": np.get_include()})
import mosaic



def names_to_fileinfos( names ):
    """
    Translate a list of GDAL filenames, into file_info objects.

    names -- list of valid GDAL dataset names.

    Returns a list of file_info objects.  There may be less file_info objects
    than names if some of the names could not be opened as GDAL files.
    """

    file_infos = []
    for name in names:
        fi = FileInfo()
        if fi.init_from_name( name ) == 1:
            file_infos.append( fi )

    return file_infos

def raster_copy( s_fh, s_xoff, s_yoff, s_xsize, s_ysize, s_band_n,
                 t_fh, t_xoff, t_yoff, t_xsize, t_ysize, t_band_n,
                 nodata=None ):

    if nodata is not None:
        return raster_copy_with_nodata(
            s_fh, s_xoff, s_yoff, s_xsize, s_ysize, s_band_n,
            t_fh, t_xoff, t_yoff, t_xsize, t_ysize, t_band_n,
            nodata )

    if verbose != 0:
        print('Copy %d,%d,%d,%d to %d,%d,%d,%d.' \
              % (s_xoff, s_yoff, s_xsize, s_ysize,
             t_xoff, t_yoff, t_xsize, t_ysize ))

    s_band = s_fh.GetRasterBand( s_band_n )
    t_band = t_fh.GetRasterBand( t_band_n )

    data = s_band.ReadRaster( s_xoff, s_yoff, s_xsize, s_ysize,
                             t_xsize, t_ysize, t_band.DataType )
    t_band.WriteRaster( t_xoff, t_yoff, t_xsize, t_ysize,
                        data, t_xsize, t_ysize, t_band.DataType )


    return 0

def raster_copy_with_nodata( s_fh, s_xoff, s_yoff, s_xsize, s_ysize, s_band_n,
                             t_fh, t_xoff, t_yoff, t_xsize, t_ysize, t_band_n,
                             nodata ):
    try:
        import numpy as Numeric
    except ImportError:
        import Numeric

    if verbose != 0:
        print('Copy %d,%d,%d,%d to %d,%d,%d,%d.' \
              % (s_xoff, s_yoff, s_xsize, s_ysize,
             t_xoff, t_yoff, t_xsize, t_ysize ))

    s_band = s_fh.GetRasterBand( s_band_n )
    t_band = t_fh.GetRasterBand( t_band_n )

    data_src = s_band.ReadAsArray( s_xoff, s_yoff, s_xsize, s_ysize,
                                   t_xsize, t_ysize )
    data_dst = t_band.ReadAsArray( t_xoff, t_yoff, t_xsize, t_ysize )

    plt.subplot(1,2,1)
    plt.imshow(data_src, cmap='gray')
    plt.subplot(1,2,2)
    plt.imshow(data_dst, cmap='gray')
    plt.show()

    nodata_test = Numeric.equal(data_src,nodata)
    to_write = Numeric.choose( nodata_test, (data_src, data_dst) )

    t_band.WriteArray( to_write, t_xoff, t_yoff )

    return 0

class FileInfo:
    """A class holding information about a GDAL file."""

    def init_from_name(self, filename):
        """
        Initialize file_info from filename

        filename -- Name of file to read.

        Returns 1 on success or 0 if the file can't be opened.
        """
        fh = gdal.Open( filename )
        if fh is None:
            return 0

        self.fh = fh
        self.filename = filename
        self.bands = fh.RasterCount
        self.xsize = fh.RasterXSize
        self.ysize = fh.RasterYSize
        self.band_type = fh.GetRasterBand(1).DataType
        self.projection = fh.GetProjection()
        self.geotransform = fh.GetGeoTransform()
        self.ulx = self.geotransform[0]
        self.uly = self.geotransform[3]
        self.lrx = self.ulx + self.geotransform[1] * self.xsize
        self.lry = self.uly + self.geotransform[5] * self.ysize

        ct = fh.GetRasterBand(1).GetRasterColorTable()
        if ct is not None:
            self.ct = ct.Clone()
        else:
            self.ct = None

        return 1

    def report( self ):
        print('Filename: '+ self.filename)
        print('File Size: %dx%dx%d' \
              % (self.xsize, self.ysize, self.bands))
        print('Pixel Size: %f x %f' \
              % (self.geotransform[1],self.geotransform[5]))
        print('UL:(%f,%f)   LR:(%f,%f)' \
              % (self.ulx,self.uly,self.lrx,self.lry))

    def copy_into( self, t_fh, s_band = 1, t_band = 1, nodata_arg=None ):
        """
        Copy this files image into target file.

        This method will compute the overlap area of the file_info objects
        file, and the target gdal.Dataset object, and copy the image data
        for the common window area.  It is assumed that the files are in
        a compatible projection ... no checking or warping is done.  However,
        if the destination file is a different resolution, or different
        image pixel type, the appropriate resampling and conversions will
        be done (using normal GDAL promotion/demotion rules).

        t_fh -- gdal.Dataset object for the file into which some or all
        of this file may be copied.

        Returns 1 on success (or if nothing needs to be copied), and zero one
        failure.
        """
        t_geotransform = t_fh.GetGeoTransform()
        t_ulx = t_geotransform[0]
        t_uly = t_geotransform[3]
        t_lrx = t_geotransform[0] + t_fh.RasterXSize * t_geotransform[1]
        t_lry = t_geotransform[3] + t_fh.RasterYSize * t_geotransform[5]

        # figure out intersection region
        tgw_ulx = max(t_ulx,self.ulx)
        tgw_lrx = min(t_lrx,self.lrx)
        if t_geotransform[5] < 0:
            tgw_uly = min(t_uly,self.uly)
            tgw_lry = max(t_lry,self.lry)
        else:
            tgw_uly = max(t_uly,self.uly)
            tgw_lry = min(t_lry,self.lry)

        # do they even intersect?
        if tgw_ulx >= tgw_lrx:
            return 1
        if t_geotransform[5] < 0 and tgw_uly <= tgw_lry:
            return 1
        if t_geotransform[5] > 0 and tgw_uly >= tgw_lry:
            return 1

        # compute target window in pixel coordinates.
        tw_xoff = int((tgw_ulx - t_geotransform[0]) / t_geotransform[1] + 0.1)
        tw_yoff = int((tgw_uly - t_geotransform[3]) / t_geotransform[5] + 0.1)
        tw_xsize = int((tgw_lrx - t_geotransform[0])/t_geotransform[1] + 0.5) \
                   - tw_xoff
        tw_ysize = int((tgw_lry - t_geotransform[3])/t_geotransform[5] + 0.5) \
                   - tw_yoff

        if tw_xsize < 1 or tw_ysize < 1:
            return 1

        # Compute source window in pixel coordinates.
        sw_xoff = int((tgw_ulx - self.geotransform[0]) / self.geotransform[1])
        sw_yoff = int((tgw_uly - self.geotransform[3]) / self.geotransform[5])
        sw_xsize = int((tgw_lrx - self.geotransform[0]) \
                       / self.geotransform[1] + 0.5) - sw_xoff
        sw_ysize = int((tgw_lry - self.geotransform[3]) \
                       / self.geotransform[5] + 0.5) - sw_yoff

        if sw_xsize < 1 or sw_ysize < 1:
            return 1

        #Extract the source and the destination arrays
        print "Input offsets: ",  sw_xoff, sw_yoff, sw_xsize, sw_ysize
        print "Destination offsets: ", tw_xoff, tw_yoff, tw_xsize, tw_ysize
        # Open the source file, and copy the selected region.
        s_fh = gdal.Open( self.filename )

        return \
            raster_copy( s_fh, sw_xoff, sw_yoff, sw_xsize, sw_ysize, s_band,
                         t_fh, tw_xoff, tw_yoff, tw_xsize, tw_ysize, t_band,
                         nodata_arg )


def main(names):
    """
    names:  A variable number of georeferenced images in the same projection.
    """
    #TODO: Remove these declarations that are known to be none
    ulx = None
    psize_x = None
    band_type = None
    out_file = 'out.tif'
    bTargetAlignedPixels = False
    separate = 0
    copy_pct = 0
    createonly = 0
    nodata = 0.0
    a_nodata = 0.0
    pre_init = []
    create_options = []

    # Collect information on all the source files.
    file_infos = names_to_fileinfos( names )

    #Get the total extent
    if ulx is None:
        ulx = file_infos[0].ulx
        uly = file_infos[0].uly
        lrx = file_infos[0].lrx
        lry = file_infos[0].lry

        for fi in file_infos:
            ulx = min(ulx, fi.ulx)
            uly = max(uly, fi.uly)
            lrx = max(lrx, fi.lrx)
            lry = min(lry, fi.lry)

    #Get the pixel size of the first image
    if psize_x is None:
        psize_x = file_infos[0].geotransform[1]
        psize_y = file_infos[0].geotransform[5]

    #Get the data_type of the first image
    if band_type is None:
        band_type = file_infos[0].band_type

    # Try opening as an existing file.
    gdal.PushErrorHandler( 'CPLQuietErrorHandler' )
    t_fh = gdal.Open( out_file, gdal.GA_Update )
    gdal.PopErrorHandler()

    # Create output file if it does not already exist.
    if t_fh is None:

        if bTargetAlignedPixels:
            ulx = math.floor(ulx / psize_x) * psize_x
            lrx = math.ceil(lrx / psize_x) * psize_x
            lry = math.floor(lry / -psize_y) * -psize_y
            uly = math.ceil(uly / -psize_y) * -psize_y

        geotransform = [ulx, psize_x, 0, uly, 0, psize_y]

        xsize = int((lrx - ulx) / geotransform[1] + 0.5)
        ysize = int((lry - uly) / geotransform[5] + 0.5)


        if separate != 0:
            bands=0

            for fi in file_infos:
                bands=bands + fi.bands
        else:
            bands = file_infos[0].bands

        Driver = gdal.GetDriverByName('GTiff')
        t_fh = Driver.Create( out_file, xsize, ysize, bands,
                              band_type, create_options )
        if t_fh is None:
            print('Creation failed, terminating gdal_merge.')
            sys.exit( 1 )

        t_fh.SetGeoTransform( geotransform )
        t_fh.SetProjection( file_infos[0].projection )

        if copy_pct:
            t_fh.GetRasterBand(1).SetRasterColorTable(file_infos[0].ct)
    else:
        if separate != 0:
            bands=0
            for fi in file_infos:
                bands=bands + fi.bands
            if t_fh.RasterCount < bands :
                print('Existing output file has less bands than the input files. You should delete it before. Terminating gdal_merge.')
                sys.exit( 1 )
        else:
            bands = min(file_infos[0].bands,t_fh.RasterCount)

    # Do we need to set nodata value ?
    if a_nodata is not None:
        for i in range(t_fh.RasterCount):
            t_fh.GetRasterBand(i+1).SetNoDataValue(a_nodata)

    # Do we need to pre-initialize the whole mosaic file to some value?
    if pre_init is not None:
        if t_fh.RasterCount <= len(pre_init):
            for i in range(t_fh.RasterCount):
                t_fh.GetRasterBand(i+1).Fill( pre_init[i] )
        elif len(pre_init) == 1:
            for i in range(t_fh.RasterCount):
                t_fh.GetRasterBand(i+1).Fill( pre_init[0] )

    # Copy data from source files into output file.
    t_band = 1

    if quiet == 0 and verbose == 0:
        progress( 0.0 )
    fi_processed = 0

    intersections = {}
    files_to_check = list(file_infos)
    for outfi in file_infos:
        for infi in files_to_check:
            if outfi == infi:
                continue
            intersection = checkforintersection(infi, outfi)
            if intersection != 1:
                intersections.update(intersection)
        files_to_check.remove(outfi)

    #TODO: This is naive, in that we know the number of intersections per image is 1
    # In a real implementation, we would need to generate a tree and iterate
    # through from least overlaps to most, reducing the total datasize with
    # each iteration
    for k, v in intersections.iteritems():
        print k[0].filename, k[1].filename
        print v[0], v[1]
        fha = k[0].fh
        fhb = k[1].fh

        #Differentiate using Laplcian - this could be Sobel as well - this is approximate
        dest = fhb.GetRasterBand(1).ReadAsArray(v[1][0], v[1][1], v[1][2], v[1][3]).astype(np.float32)
        src = fha.GetRasterBand(1).ReadAsArray(v[0][0], v[0][1], v[0][2], v[0][3])
        #Get the indices of valid data in the source and the destination.
        #Source indices are the mask

        validsrc = np.nonzero(src)
        validdest = np.nonzero(dest)
        n = len(validsrc[0])

        src = src.astype(np.float32)
        src = np.ma.masked_equal(src, nodata, copy=False)
        np.ma.set_fill_value(src, np.nan)
        srclap = convolve(src, np.array([[0,-1,0],[-1, 4, -1],[0, -1, 0]]))

        """
        #Plot the src and the laplacian (2nd derivative)
        lt.subplot(1,2,1)
        plt.imshow(src, cmap='gray')
        plt.subplot(1,2,2)
        plt.imshow(srclap, cmap='gray')
        plt.show()
        """
        #Blend
        #Ax = b
        imidx, count = mosaic.idxarr(src)
        #Compute A and b
        A, b = mosaic.genAb(src, srclap, imidx, dest, n)
        sol = np.linalg.solve(A, b)
        print np.amin(sol), np.amax(sol), np.std(sol)

        print "A Generated.  Solving..."
        print "Solved.  Recreating the matrix..."
        exit()
        for x in range(xsize-1):
            for y in range(ysize-1):
                if src[y, x] != 0.0:
                    idx = imidx[y,x]
                    print y, x, sol[idx]
                    dest[y,x] = sol[idx]

        return dest


        #Solve
        plt.imshow(img, cmap='gray')
        plt.show()
        exit()
    return
    #Iterate through all of the input images and begin to merge them.
    for fi in file_infos:
        if createonly != 0:
            continue

        if verbose != 0:
            print("")
            print("Processing file %5d of %5d, %6.3f%% completed." \
                  % (fi_processed+1,len(file_infos),
                     fi_processed * 100.0 / len(file_infos)) )
            fi.report()

        if separate == 0 :
            for band in range(1, bands+1):
                fi.copy_into( t_fh, band, band, nodata )
        else:
            for band in range(1, fi.bands+1):
                fi.copy_into( t_fh, band, t_band, nodata )
                t_band = t_band+1

        fi_processed = fi_processed+1
        if quiet == 0 and verbose == 0:
            progress( fi_processed / float(len(file_infos))  )

def checkforintersection(infi, outfi):
        infi_geotransform = infi.geotransform
        infi_ulx = infi_geotransform[0]
        infi_uly = infi_geotransform[3]
        infi_lrx = infi_geotransform[0] + infi.xsize * infi_geotransform[1]
        infi_lry = infi_geotransform[3] + infi.ysize* infi_geotransform[5]

        outfi_geotransform = outfi.geotransform
        outfi_ulx = outfi_geotransform[0]
        outfi_uly = outfi_geotransform[3]
        outfi_lrx = outfi_geotransform[0] + outfi.xsize * outfi_geotransform[1]
        outfi_lry = outfi_geotransform[3] + outfi.ysize* outfi_geotransform[5]

        # figure out intersection region
        tgw_ulx = max(infi_ulx,outfi_ulx)
        tgw_lrx = min(infi_lrx,outfi.lrx)
        if infi_geotransform[5] < 0:
            tgw_uly = min(infi_uly,outfi_uly)
            tgw_lry = max(infi_lry,outfi_lry)
        else:
            tgw_uly = max(infi_uly,outfi_uly)
            tgw_lry = min(infi_lry,outfi_lry)

        # do they even intersect?
        if tgw_ulx >= tgw_lrx:
            return 1
        if infi_geotransform[5] < 0 and tgw_uly <= tgw_lry:
            return 1
        if infi_geotransform[5] > 0 and tgw_uly >= tgw_lry:
            return 1

        print tgw_ulx, tgw_uly, tgw_lrx, tgw_lry

        # compute target window in pixel coordinates.
        tw_xoff = int((tgw_ulx - infi_geotransform[0]) / infi_geotransform[1] + 0.1)
        tw_yoff = int((tgw_uly - infi_geotransform[3]) / infi_geotransform[5] + 0.1)
        tw_xsize = int((tgw_lrx - infi_geotransform[0])/infi_geotransform[1] + 0.5) \
                   - tw_xoff
        tw_ysize = int((tgw_lry - infi_geotransform[3])/infi_geotransform[5] + 0.5) \
                   - tw_yoff

        if tw_xsize < 1 or tw_ysize < 1:
            return 1

        # Compute source window in pixel coordinates.
        sw_xoff = int((tgw_ulx - outfi_geotransform[0]) / outfi_geotransform[1])
        sw_yoff = int((tgw_uly - outfi_geotransform[3]) / outfi_geotransform[5])
        sw_xsize = int((tgw_lrx - outfi_geotransform[0]) \
                       / outfi_geotransform[1] + 0.5) - sw_xoff
        sw_ysize = int((tgw_lry - outfi_geotransform[3]) \
                       / outfi_geotransform[5] + 0.5) - sw_yoff

        if sw_xsize < 1 or sw_ysize < 1:
            return 1


        """
        #Plotting
        s_band = infi.fh.GetRasterBand(1)
        t_band = outfi.fh.GetRasterBand(1)

        data_src = t_band.ReadAsArray( sw_xoff, sw_yoff, sw_xsize, sw_ysize)
        data_dst = s_band.ReadAsArray( tw_xoff, tw_yoff, tw_xsize, tw_ysize )

        print data_src.shape
        print data_dst.shape
        plt.subplot(1,2,1)
        plt.imshow(data_src, cmap='gray')
        plt.subplot(1,2,2)
        plt.imshow(data_dst, cmap='gray')
        plt.show()
        """
        return {(outfi, infi) : ([sw_xoff, sw_yoff, sw_xsize, sw_ysize],
                                                   [tw_xoff, tw_yoff, tw_xsize, tw_ysize])}



if __name__ == '__main__':
    names = sys.argv[1:]
    main(names)
