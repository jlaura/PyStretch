import optparse
from pystretch.linear import Linear
from pystretch.nonlinear import Nonlinear
from pystretch.filter import Filter

def parse_arguments():
    
    desc='''Description: %prog leverages GDAL and NUMPY to stretch raster images.  GDAL 1.8.0 and NUMPY 1.5.1 or greater are required. Both linear and non-linear stretches are available.'''
    
    usg='''%prog <inputfile> [options]'''
    
    parser = optparse.OptionParser(description=desc, usage=usg)
    
    generalOptions = optparse.OptionGroup(parser, 'I/O Options')
    linearStretches = optparse.OptionGroup(parser, 'Linear Stretches' )
    directionOptions = optparse.OptionGroup(parser, 'Directional Options')
    nonlinearstretches = optparse.OptionGroup(parser, 'Non-linear Stretches')
    filters = optparse.OptionGroup(parser, 'Filters')
    
    generalOptions.add_option('--output', '-o',action='store',type='string',default='output.tif',dest='output',help='The optional output file')
    generalOptions.add_option('--format', '-f',action='store',type='string',default='GTiff', dest="outputFormat" ,help='Any GDAL supported output format. Default: [%default]') 
    generalOptions.add_option('--ot', action='store', type='string', dest='dtype',default=None, help='A GDAL output format. (Byte, Int16, Float32 are likely candidates.' )
    generalOptions.add_option('--writesize', '-w', action='store', type='int', default=50, dest='writesize', help='An integer to control the size of the array blocks stored in memory prior to writing.  In short, this is the number of array blocks stored in memory prior to writing.')
    generalOptions.add_option('--visualize', '-z', action='store_true', default=False, dest='visualize', help='show the output histogram.')
    generalOptions.add_option('--NDV', action='store', dest='NDV', type='float', help='Define a no data value if teh dataset does not have one.')    
    generalOptions.add_option('--scale','-s', action='store', dest='scale',nargs=2, type='string', help='Scale the data to 8-bit')
    
    directionOptions.add_option('--horizontal', '-t', action='store',type='int', dest='hint', default=1, help='The number of horizontal segments to divide the image into.  This will likely leave a small "remainder" segment at the edge of the image.')
    directionOptions.add_option('--vertical', '-v', action='store', type='int', dest ='vint', default=1, help='The number of vertical segments to divide the image into.  This will likely leave a small "remainder" segment at the edge of the image.')
    
    linearStretches.add_option('--std', '-d', action='store_true', dest='standard_deviation_stretch',default=False,help='Perform a standard deviation stretch with default n=2. Set "-n <float> to specify a different number of standard deviations.')
    linearStretches.add_option('--standarddeviations','-n', action='store', type='float', dest='sigma', default=2, help='The number of standard deviations over which the stretch is performed.')
    linearStretches.add_option('--linear', '-l', action='store_true', dest='linear_stretch', default=False, help='Perform a linear stretch.  To set clipping set "-c <integer>.')
    linearStretches.add_option('--clip', '-c', action='store', type='float', default=0, dest='clip', help='The percentage to clip the tails of the histogram by')
    linearStretches.add_option('--inverse', '-i', action='store_true', default=False, dest='inverse_stretch', help='Perform an inverse stretch')
    linearStretches.add_option('--binary', '-y', action='store_true', default=False, dest='binary_stretch', help='Performs a binary stretch')
    linearStretches.add_option('--threshold', '--th', action='store', type='float', default='128', dest='threshold', help='The threshold value for the binary stretch.')
    linearStretches.add_option('--hicut', action='store_true', default=False, dest='hicut_stretch', help='Set all values above the cut to a user defined value (defaults to 0)')
    linearStretches.add_option('--lowcut', action='store_true', default=False, dest='lowcut_stretch', help='Set all vlues below the cut to a user defined value (defaults to 0)')
    linearStretches.add_option('--cutvalue', action='store', type='float',dest='cutvalue', default=0, help = 'The cut value used with either lowcut or hicut.')
    
    nonlinearstretches.add_option('--gamma', '-g', action='store_true', dest='gamma_stretch', default=False, help='Perform a gamma stretch')
    nonlinearstretches.add_option('--gammavalue', '--gv', action='store', type='float', default=1.6, dest='gammavalue', help='The gamma value to be used.  Processed as 1/gamma.')
    nonlinearstretches.add_option('--histogramequalization', '-q', action='store_true', default=False, dest='histequ_stretch', help='Perform a histogram equalization.  It is suggested that sample size be set to 1 to ensure that the entire image is processed.  Default number of bins is 128, to change this set "-b <integer number of bins>".')
    nonlinearstretches.add_option('--bins', '-b', action='store', type='int', default=128, dest='num_bins', help='The number of bins to be used with the histogram equalization.')
    nonlinearstretches.add_option('--log', '-r', action='store_true', dest='logrithmic_stretch', default=False, help='Performs a logrithmic stretch with default epsilon of 1.  This is most likely appropriate for images with magnitudes typically much larger than 1.  To modify epsilon use "-e <float epsilon value>".')
    nonlinearstretches.add_option('--epsilon', '-e', action='store', type='float', default=1, dest='epsilon', help='The desired epsilon value.')
    #nonlinearstretches.add_option('--gaussian', '-u', action='store_true', default=False, dest='gaussian_stretch', help='Performs a gaussian stretch.')
    #nonlinearstretches.add_option('--histogrammatch', '-m', action='store_true', default=False,dest='histogram_match', help='Perform a histogram match to another image. Be sure to define the input reference histogram')
    #nonlinearstretches.add_option('--referenceimage','--ref', action='store',dest='reference_input', help='The reference histogram to match')
    
    filters.add_option('--laplacian', '--lap', action='store_true', default=False, dest='laplacian_filter', help='Perform a laplacian filter.')
    filters.add_option('--hipass3', '--hi3', action='store_true', default=False, dest='hipass_filter_3x3', help='Perform a hipass filter.')
    filters.add_option('--hipass5', '--hi5', action='store_true', default=False, dest='hipass_filter_5x5', help='Perform a hipass filter.')
    filters.add_option('--gaussianfilter','--gf', action='store_true', default=False, dest='gaussian_filter', help='Performs a gaussian (lowpass) filter on an image')
    filters.add_option('--gaussianhipass','--gh', action='store_true', default=False, dest='gaussian_hipass', help='Performs a gaussian hipass filter on an image')
    filters.add_option('--meanfilter', '--mf', action='store_true', default=False, dest='mean_filter', help ='Perform mean filter.')
    filters.add_option('--conservativefilter', '--cf', action='store_true', default=False, dest='conservative_filter', help='Perform a conservative filter.')
    filters.add_option('--kernelsize', '-k', action='store', default=3, type='int', dest='kernel_size', help='A positive, odd, integer which is the size of the kernel to be created')
    filters.add_option('--median', '--md', action='store_true', default=False, dest='median_filter', help='Perform a median filtering of the input image with default 3x3 kernel.  Specify -k int, where int is an odd integer for a larger kernel')


    
    parser.add_option_group(generalOptions)
    parser.add_option_group(directionOptions)
    parser.add_option_group(linearStretches)
    parser.add_option_group(nonlinearstretches)
    parser.add_option_group(filters)

    
    (options, args) = parser.parse_args()
    
    options = vars(options)
    return options, args

#This needs to get cleanup / improved.  It would be better to use the dict function in ArrayConvert.
def get_stretch(options):
    if options['linear_stretch'] == True:
        return Linear.linear_stretch
    elif options['standard_deviation_stretch'] == True:
        return Linear.standard_deviation_stretch
    elif options['inverse_stretch'] == True:
        return Linear.inverse_stretch
    elif options['binary_stretch'] == True:
        return Linear.binary_stretch
    elif options['hicut_stretch'] == True:
        return Linear.hicut_stretch
    elif options['lowcut_stretch'] == True:
        return Linear.lowcut_stretch
    elif options['gamma_stretch'] == True:
        return Nonlinear.gamma_stretch
    elif options['histequ_stretch'] == True:
        return Nonlinear.histequ_stretch
    elif options['mean_filter'] == True:
        return Filter.mean_filter
    elif options['median_filter'] == True:
        return Filter.median_filter
    elif options['laplacian_filter'] == True:
        return Filter.laplacian_filter
    elif options['hipass_filter_3x3'] == True:
        return Filter.hipass_filter_3x3
    elif options['hipass_filter_5x5'] == True:
        return Filter.hipass_filter_5x5
    elif options['gaussian_filter'] == True:
        return Filter.gaussian_filter
    elif options['gaussian_hipass'] == True:
        return Filter.gaussian_hipass
    elif options['conservative_filter'] == True:
        return Filter.conservative_filter
        
            