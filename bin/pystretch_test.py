#!/usr/bin/env python

from pystretch.tests import Tests

import sys
import subprocess
from osgeo import gdal
import os

def Usage():
    print('Usage: pystretch_test.py [-srcwin xoff yoff width height] [-projwin ulx uly lrx lyx] srcfile')
    print
    sys.exit(1)
    
def main():
    srcwin = None
    projwin = None
    srcfile = None
    dstfile = None
    
    gdal.AllRegister()
    argv = gdal.GeneralCmdLineProcessor(sys.argv )
    if argv is None:
        sys.exit(0)
    
    #Parse the command line args
    i = 1
    while i < len(argv):
        arg = argv[i]
        
        if arg == '-srcwin':
            srcwin = (int(argv[i+1]),int(argv[i+2]),
                      int(argv[i+3]),int(argv[i+4]))
            i = i + 4
        elif arg == 'projwin':
            projwin = (int(argv[i+1]),int(argv[i+2]),
                      int(argv[i+3]),int(argv[i+4]))
            i = i + 4
            
        elif arg[0] == '-':
            Usage()
        
        elif srcfile is None:
            srcfile = arg
            
        elif dstfile is None:
            dstfile = arg
        
        else: 
            Usage()
        
        i +=1
    
    if srcfile is None:
        Usage()
        
    srcds = gdal.Open(srcfile)
    if srcds is None:
        print "Could not open %s." %srcfile
        sys.exit(1)
  
    #Create an output directory
    workingdirectory = os.getcwd()
    if os.path.exists(workingdirectory + '/testimages') == False:
        os.mkdir(workingdirectory + '/testimages')
        testimagedir = workingdirectory + '/testimages'      
    else:
        testimagedir = workingdirectory + '/testimages'
        

    if srcwin is not None:
        Tests.getpixelcrop(srcfile, testimagedir, srcwin)
    elif projwin is not none:
        Tests.getprojcrop(srcfile, testimagedir, projwin)
    else:
        print "Unable to get crop of the input image."
        
    inputtestimage = testimagedir + '/1original_cropped_image.tif'

    #Test linear
    for c in range(0, 10, 2):
        output = testimagedir + "/linearstretch_clipped_%i_percent.tif" %c
        try:
            subprocess.call("pystretcher.py -l -c '%i' -o '%s' %s"%(c,output,inputtestimage), shell = True)
        except:
            print "Failed to perform a linear stretch with clip %i." %c
    
    #Test standard deviation
    for n in range(4, 35, 5):
        n *= 1.0/10.0
        
        output = testimagedir + "/stdstretch_sigma_%i.tif" %n
        try:
            subprocess.call("pystretcher.py --std -n %f -o '%s' %s"%(n,output, inputtestimage), shell = True)
        except:
            print "Failed to perform a standard deviation stretch with sigma (n) %f." %n

    #Test inverse
    output = testimagedir + "/inverse_stretch.tif"
    try:
        subprocess.call("pystretcher.py -i -o '%s' %s"%(output, inputtestimage), shell = True)
    except:
        print "Failed to perform an inverse stretch."

    #Test binary
    for th in range(64,256,64):
        output = testimagedir + "/binary_stretch_threshold_%i.tif" %th
        try:
            subprocess.call("pystretcher.py -y --th '%i' -o '%s' %s"%(th, output, inputtestimage), shell = True)
        except:
            print "Failed to perform a binary stretch with threshold %i." %th
            
    #Test High Cut 
    for cutvalue in range(64,256, 24):
        output = testimagedir + "/hi_stretch_cutvalue_%i.tif" %cutvalue
        try:
            subprocess.call("pystretcher.py --hicut --cutvalue '%i' -o '%s' %s"%(cutvalue, output, inputtestimage), shell = True)
        except:
            print "Failed to perform a high cut stretch with cut value %i." %cutvalue
    
    #Test Low Cut
    for cutvalue in range(64,192, 24):
        output = testimagedir + "/low_stretch_cutvalue_%i.tif" %cutvalue
        try:
            subprocess.call("pystretcher.py --lowcut --cutvalue '%i' -o '%s' %s"%(cutvalue, output, inputtestimage), shell = True)
        except:
            print "Failed to perform a low cut stretch with cut value %i." %cutvalue
    
    #Test Gamma
    for gv in range(8, 28, 4):
        gv *= 1.0/10.0
        output = testimagedir + "/gamma_stretch_gamma_%f.tif" %gv
        try:
            subprocess.call("pystretcher.py -g --gv '%f' -o '%s' %s"%(gv, output, inputtestimage), shell = True) 
        except:
            print "Failed to perform a gamma stretch with gamma %f." %gv

    #Test Histogram Equalization
    for b in range(64, 256, 64):
        output = testimagedir + "/histogramequalization_stretch_%i_bins.tif" %b
        try:
            subprocess.call("pystretcher.py -q -b '%i' -o '%s' %s"%(b, output, inputtestimage), shell = True)
        except:
            print "Failed to perform a histogram equalization stretch with %i bins." %b
          
    #Test Logarithmic
    for epsilon in range(8, 12, 2):
        epsilon *= 1.0/10.0
        output = testimagedir + "/log_stretch_epsilon_%f.tif" %epsilon
        try:
            subprocess.call("pystretcher.py -r -e '%f' -o '%s' %s"%(epsilon, output, inputtestimage), shell = True)
        except:
            print "Failed to perform a logarithmic stretch with epsilon %f." %epsilon

    #Test filters
    for k in range(3,7,2):
        
        #Laplacian
        output = testimagedir + "/laplacian_filter_kernelsize_%i.tif" %k
        try:
            subprocess.call("pystretcher.py --lap -k '%i' -o '%s' %s"%(k, output, inputtestimage), shell = True)
        except:
            print "Failed to perform a laplacian filter with a %i x %i kernel." %(k, k)
     
        #Gaussian
        output = testimagedir + "/gaussian_filter_kernelsize_%i.tif" %k
        try:
            subprocess.call("pystretcher.py --gf -k '%i' -o '%s' %s"%(k, output, inputtestimage), shell = True)
        except:
            print "Failed to perform a gaussian filter with a %i x %i kernel." %(k, k)      
          
        #Gaussian High Pass
        output = testimagedir + "/gaussianhi_filter_kernelsize_%i.tif" %k
        try:
            subprocess.call("pystretcher.py --gh -k '%i' -o '%s' %s"%(k, output, inputtestimage), shell = True)
        except:
            print "Failed to perform a gaussian high pass filter with a %i x %i kernel." %(k, k)
         
        #Mean
        output = testimagedir + "/mean_filter_kernelsize_%i.tif" %k
        try:
            subprocess.call("pystretcher.py --mf -k '%i' -o '%s' %s"%(k, output, inputtestimage), shell = True)
        except:
            print "Failed to perform a mean filter with a %i x %i kernel." %(k, k)
      
        #Median
        output = testimagedir + "/median_filter_kernelsize_%i.tif" %k
        try:
            subprocess.call("pystretcher.py --md -k '%i' -o '%s' %s"%(k, output, inputtestimage), shell = True)        
        except:
            print "Failed to perform a median filter with a %i x %i kernel." %(k, k)  
            
        #Conservative
        output = testimagedir + "/conservative_filter_kernelsize_%i.tif" %k
        try:
            subprocess.call("pystretcher.py --cf -k '%i' -o '%s' %s"%(k, output, inputtestimage), shell = True)
        except:
            print "Failed to perform a conservative filter with a %i x %i kernel." %(k, k)            
            
            
    #High3
    output = testimagedir + "/HighPass3x3_filter.tif"
    try:
        subprocess.call("pystretcher.py --hi3 -k '%i' -o '%s' %s"%(k, output, inputtestimage), shell = True)
    except:
        print "Failed to perform a high pass3 filter."
    
    #High5  
    output = testimagedir + "/HighPass5x5_filter.tif"
    try:
        subprocess.call("pystretcher.py --hi5 -k '%i' -o '%s' %s"%(k, output, inputtestimage), shell = True)
    except:
        print "Failed to perform a high pass5 filter."
            
if __name__ == '__main__':
    main()