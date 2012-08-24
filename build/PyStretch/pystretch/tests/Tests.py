from osgeo import gdal
import sys
import subprocess
import os
 
def getpixelcrop(testimage, testimagedir, srcwin):
    #1 prepended to the original name to get it to be at the top of teh directory
    original = testimagedir + '/1original_cropped_image.tif'
    subprocess.call("gdal_translate -srcwin '%i' '%i' '%i' '%i' '%s' '%s'" %(srcwin[0], srcwin[1], srcwin[2], srcwin[3], testimage, original), shell=True)
    

def getprojcrop(testimage, testimagedir, projwin):
    original = testimagedir + 'original_cropped_image.tif'
    subprocess.call("gdal_translate -projwin '%i' '%i' '%i' '%i' '%s' '%s'" %(projwin[0], projwin[1], projwin[2], projwin[3], testimage, original), shell=True)
    