.. contents::

=================
PyStretch
=================


PyStretch provides a python based image manipulation tool which is able to
handle images which are larger than a systems available RAM. This tools was
designed to support planetary cartographic images and leverages the Geospatial
Data Abstraction Library (GDAL) to handle projection, transformation, and
georeferencing information, as well as available supported data formats and
image arrays.

For more detailed documentation, with images, examples, etc, check out
http://packages.python.org/PyStretch.

Introduction 
------------

The package author's goal is to provide an image processing toolset which allows
for persistent manipulation and analysis of large, spatially enabled raster
datasets, on machines which are traditionally RAM constrained. The RAM
constraint can be imposed either by a lack of memory or by the size of the
raster for analysis. Additionally, this package allows for the systematic
removal spatially definable camera error.

What about bugs or feature requests? 
------------------------------------

With any initial release, bugs are undoubtably present. To report a bug or
request a feature, open a ticket at http://github.com/jlaura/PyStretch

The code can also be cloned and forked via git, if you are a github user.


Getting started immediately - a super brief overview
----------------------------------------------------

This package is intended to be run primarily from the pystretch.py script
located in Python##/bin/. Ideally this directory is already added to your Path
of your PYTHONPATH. If not, you either need to run the script from the bin
directory or add that directroy to your PATH.

For help use:

    python pystretch.py --help

Typical usage often looks like this:

    python pystretch.py <stretch> <optional segmentation> <input> <optional
    output>

or

    python pystretch.py -l -t 5 input.tif -o output_image.tif

The code above performs a linear stretch <-l> by segmenting the image into 5
horizontal sections <-t 5> and writes to the output <output_image.tif>.

Note that segmenting the image into 5 pieces will likely result in 6 total
sections as the image is subdivided into 5 sections of equal size and one
'remainder' section.

For a much more in depth look at the functionality checkout:
http://packages.python.org/PyStretch

PyStretch Test 
==============

As a means to both test the functionality of the script and show the results of
the different processing techniques users are encouraged to select a sample
image and run it through pystretch_test.py. This script takes a subsection of
the input image and processes it with all of the available processing techniques
so that users can see some of the most common parameters. For example, the
standard deviation stretch is performed with sigma (n) values between 0
(essentially a binary image with the threshold at the mean) and 3 (~98% of the
histogram maintained).

To run this test to both validate the input and assess the functionality of the
script use:

    python pystretch_test.py -srcwin xorigin yorigin width height input_image

For example:

    python pystretch_test.py -srcwin 0 0 250 250 myimage.jp2

If you do not know the pixel offset that you wish to test at, but do know the
geographic coordinates you can use:

    python pystretch_test.py -projwin ulx uly lrx lry input_image

Known Issues 
--------------

1. When reading against the intrinsic image block size rad and write times are
quite long due to thrashing. This is a known issue with the way in which GDAL
RasterIO works. It is therefore suggested that images be read in either the
block size or multiples of the block size.

For example, the block size on a GTiff is most often one scanline. Therefore,
using horizontal segments will read in multiples of the scanline and avoid Band
Thrashing. Reading the same image in the vertical direction can increase
processing time threefold.

2. The numpy implementation of ndarray.std(), which calculates the standard
deviation, creates an in memory copy of the array. Be aware of this when
deciding on image segmentation size. The standard deviation of the image or
image segment is only calculated when performing a standard deviation or
gaussian stretch. In all other cases this calculation is omitted.

Accessing classes via imports 
----------------------------------- 
It is hoped that this package will provide a number of tools to leverage the segmentation and
image analysis algorithms in your own work. For this reason the majority of the
functionality is importable.

Imports are intentionally left explicit. That is to say that the following will not work

    import \* 
    from pystretch.core import \* will not work.

Instead explicitly import the modules you want to use

    from pystretch.core import ArrayConvert 
    from pystretch.linear import Linear
    from pystretch.plot import Plot