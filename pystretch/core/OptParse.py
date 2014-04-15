import optparse
import argparse
from pystretch.linear import Linear
from pystretch.nonlinear import Nonlinear
from pystretch.filter import Filter
from pystretch.custom import Custom


#Dict of functions available to the user
functions = {}

linearfunctions = {'sigma':Linear.standard_deviation_stretch, 'minmax':Linear.minmax_stretch,
             'clip':Linear.clip_stretch, 'inverse_stretch':Linear.inverse_stretch,
             'binary_pivot':Linear.binary_stretch, 'hicut_pivot':Linear.hicut_stretch,
             'lowcut_pivot':Linear.lowcut_stretch}

nonlinearfunctions = {'gamma':Nonlinear.gamma_stretch}

functions.update(linearfunctions)
functions.update(nonlinearfunctions)


def argget_stretch(args):
    """
    Parse the flag name as a key in the functions dict
    and return the value.  Value is the function to be called.
    """
    for k, v in args.iteritems():
        if v != None and k in functions.keys():
            return functions[k]


def global_args(parser):
    """
    Append the tool specific parser with the global parsing options.  This provides
    functionality where the subparser argument is always first, followed by the
    global arguments and local arguments.
    """
    parser.add_argument('input', help='The input image file.')
    parser.add_argument('-o', '--output', dest='output', default='output.tif', action='store', type=str, help='The output file')
    parser.add_argument('--cores', dest='ncores', type=int, help='The number of cores to use. Defaults to all cores.')
    parser.add_argument('-f', '--format',action='store',type=str,default='GTiff', dest="outputformat" ,help='Any GDAL supported output format. (Default: GTiff)')
    parser.add_argument('--ot', action='store', type=str, dest='dtype',default='Byte', help='A GDAL output format. (Byte, Int16, Float32 are likely candidates.' )
    parser.add_argument('--NDV', action='store', dest='ndv', type=float, help='Define an output NDV.  If the dataset has an NDV, this value and the intrinsic NDV are set to No Data in the output.  The output NDV is this value.')
    parser.add_argument('--scale','-s', action='store', dest='scale',nargs=2, type=str, help='Scale the data to 8-bit')
    parser.add_argument('-r', '--horizontal', action='store', dest='horizontal_segments', type=int, help='Number of horizontal segments')
    parser.add_argument('-e', '--vertical', action='store', dest='vertical_segments', type=int, help='Number of vertical segments')
    parser.add_argument('-p', '--statsper', action='store_true', dest='statsper', help='Flag to compute statistics and apply a stretch per segment')
    return parser


def argparse_arguments():
    """
    Subparsers that provide a github style parsing experience to the user.
    All subparsers make calls to global_args to prepend the argument list with
    the global args.  This is done to avoid complex positional argument issues
    where the subparser commands, including the subparser name, must be preceeded
    by the global argument lists.
    """

    desc='''A parallel raster image processing library that supports datasets larger than available RAM.'''
    usg = "Usage"

    parser = argparse.ArgumentParser(version='0.3')

    subparser = parser.add_subparsers(help='Subcommand Help')
    #Linear
    parser_linear = subparser.add_parser('linear', help='Perform a linear stretch: Standard Deviation, MinMax, Clip, Inverse, Binary, Low Cut, High Cut')
    parser_linear = global_args(parser_linear)
    parser_linear.add_argument('-d', '--std', dest='sigma', help='Perform a standard deviation stretch with some sigma', type=float)
    parser_linear.add_argument('-m', '--minmax', nargs=2, dest='minmax', type=int, help='Stretch the image to a given mininum and maximum')
    parser_linear.add_argument('-c', '--clip', type=float, dest='clip', help='A percentage to clip both ends of the histogram for stretching')
    parser_linear.add_argument('-i', '--inverse', action='store_true', dest='inverse_stretch', help='Perform an inverse stretch')
    parser_linear.add_argument('-y', '--binary', type=float, dest='binary_pivot', help='Performs a binary stretch at a given value.')
    parser_linear.add_argument('--hicut', type=float, dest='hicut_pivot', help='Set all values above the cut to the maximum.')
    parser_linear.add_argument('--lowcut',type=float, dest='lowcut_pivot', help='Set all vlues below the cut to the minimum.')

    #Nonlinear
    parser_nonlinear = subparser.add_parser('nonlinear', help='Perform a nonlinear stretch: Gamma, Histogram Equalization, Logarithmic')
    parser_nonlinear = global_args(parser_nonlinear)
    parser_nonlinear.add_argument('-g', '--gamma', dest='gamma', type=float, help='Gamma stretch with a given epsilon')
    parser_nonlinear.add_argument('-q', '--histogramequalization', dest='histequ_bins',type=int, default=128, help='Perform a histogram equalization with the defined number of bins')
    parser_nonlinear.add_argument('--log', '-l', dest='logarithmic_epsilon', type=float, default=1, help='Performs a logrithmic stretch with a given epsilon.  (Default: e=1. This is most likely appropriate for images with magnitudes typically much larger than 1.).')

    #Convolution
    parser_convolve = subparser.add_parser('convolve', help='Perform a convolution: Laplacian, High Pass, Gaussian, Gaussian High Pass, Mean, Conservative, Median ')
    parser_convolve.add_argument('--laplacian', '--lap', action='store_true', default=False, dest='laplacian_filter', help='Perform a laplacian filter.')
    parser_convolve.add_argument('--hipass3', '--hi3', action='store_true', default=False, dest='hipass_filter_3x3', help='Perform a hipass filter.')
    parser_convolve.add_argument('--hipass5', '--hi5', action='store_true', default=False, dest='hipass_filter_5x5', help='Perform a hipass filter.')
    parser_convolve.add_argument('--gaussianfilter','--gf', action='store_true', default=False, dest='gaussian_filter', help='Performs a gaussian (lowpass) filter on an image')
    parser_convolve.add_argument('--gaussianhipass','--gh', action='store_true', default=False, dest='gaussian_hipass', help='Performs a gaussian hipass filter on an image')
    parser_convolve.add_argument('--meanfilter', '--mf', action='store_true', default=False, dest='mean_filter', help ='Perform mean filter.')
    parser_convolve.add_argument('--conservativefilter', '--cf', action='store_true', default=False, dest='conservative_filter', help='Perform a conservative filter.')
    parser_convolve.add_argument('--median', '--md', action='store_true', default=False, dest='median_filter', help='Perform a median filtering of the input image with a 3x3 kernel.')

    return vars(parser.parse_args())

def parse_arguments():

    desc='''Description: %prog leverages GDAL and NUMPY to stretch raster images.  GDAL 1.8.0 and NUMPY 1.5.1 or greater are required. Both linear and non-linear stretches are available.'''

    usg='''%prog <inputfile> [options]'''

    parser = optparse.OptionParser(description=desc, usage=usg, formatter=optparse.TitledHelpFormatter(width=78))

    generalOptions = optparse.OptionGroup(parser, 'I/O Options')
    linearStretches = optparse.OptionGroup(parser, 'Linear Stretches' )
    directionOptions = optparse.OptionGroup(parser, 'Directional Options')
    nonlinearstretches = optparse.OptionGroup(parser, 'Non-linear Stretches')
    filters = optparse.OptionGroup(parser, 'Filters')
    custom = optparse.OptionGroup(parser, 'Custom')

    generalOptions.add_option('--output', '-o',action='store',type='string',default='output.tif',dest='output',help='The optional output file')
    generalOptions.add_option('--format', '-f',action='store',type='string',default='GTiff', dest="outputFormat" ,help='Any GDAL supported output format. Default: [%default]')
    generalOptions.add_option('--ot', action='store', type='string', dest='dtype',default=None, help='A GDAL output format. (Byte, Int16, Float32 are likely candidates.' )
    generalOptions.add_option('--visualize', '-z', action='store_true', default=False, dest='visualize', help='show the output histogram.')
    generalOptions.add_option('--NDV', action='store', dest='ndv', type='float', help='Define an output NDV.  If the dataset has an NDV, this value and the intrinsic NDV are set to No Data in the output.  The output NDV is this value.')
    generalOptions.add_option('--scale','-s', action='store', dest='scale',nargs=2, type='string', help='Scale the data to 8-bit')
    generalOptions.add_option('--segment', '--seg', action='store_true', default=False, dest='segment', help='Use this flag to calculate statistics per segment instead of per band.  Best for removing spatially describale systematic error.')

    custom.add_option('--custom', action='store_true', default=False, dest='custom_stretch', help='Use this flag to call your own custom stretch.  You will need to code it into the custom_stretch function inside the Custom module')

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
    nonlinearstretches.add_option('--log', '-r', action='store_true', dest='logarithmic_stretch', default=False, help='Performs a logrithmic stretch with default epsilon of 1.  This is most likely appropriate for images with magnitudes typically much larger than 1.  To modify epsilon use "-e <float epsilon value>".')
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
    parser.add_option_group(custom)


    options, args = parser.parse_args()

    if not args:
        print "Error - arguments required."
        parser.print_help()


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
    elif options['logarithmic_stretch'] == True:
        return Nonlinear.logarithmic_stretch
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
    elif options['custom_stretch'] == True:
        return Custom.custom_stretch
