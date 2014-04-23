---
layout: docs
title: Basic Usage
prev_section: installation
next_section: m3_supported
permalink: /docs/usage/
---

Whether launched via the command line or the application binary, you should be greated by the PySAT interface, consisting of a number of docked parameter windows and a workspace.

![Main Interface](../../img/usage/mainscreen.png)

Currently PySAT works natively with M3 data in <code>.img</code> format, Kaguya Spectral Profiler data, and MI data in <code>.cub</code> format.  Additionally, a fallback driver, is available that reads any [GDAL supported](http://www.gdal.org/formats_list.html) file format.

<div class="note warning">
  <h5>GDAL Driver</h5>
  <p>
    The GDAL driver is naive, and does not support much of the spectral analysis functionality.  In fact, it does not even extract wavelength information from the image.  The driver is provided to allow you to visualize your data and apply basic image manipulation, e.g., contrast stretching or colorization.
  </p>
</div>

PySAT ships with two methods to interact with data: (1) open a support image file or (2) open a spectra file.

<div class="note info">
  <h5>Opening a spectral text file</h5>
  <p>
    PySAT expects ASCII spectral files with a header and two columns: (1) wavelength and (2) reflectance or radiance.  Future enhancement will support loading multiple spectra and potentially, binary data.
  </p>
</div>

To open an image file, select <code>File > Open Image</code>.  If the reader is able to determine the input data type, it will open automatically.  Otherwise a dialog will appear asking you to select the imager used to create the product.

![Open Dialog](../../img/usage/fileopen.png)

PySAT then opens the image and displays a single band, grayscale image.  In this case, we see a Level 2 Moon Mineralogy Mapper Image downloaded from the [PDS](http://pds-imaging.jpl.nasa.gov/volumes/m3.html).  We will refer to this window, where a map product is shown, as the map plot.

![Opened Image](../../img/usage/imageopened.png)

## Spectral Analysis
PySAT supports a range of spectral analysis functionality designed to support [Exploratory Data Analysis](http://en.wikipedia.org/wiki/Exploratory_data_analysis).  For supported multi and hyperspectral image formats (not those opened with the default reader) a pixel or spot observation (Spectral Profiler) can be selected and a spectra extracted.  We assume that this is an iterative workflow and in depth treatment of a proposed flow is provided [later in the documentation](later.md).

![Reflectance Plot](../../img/usage/reflectanceplot.png)

Here we see a raw reflectance plot color coded to the point in the image.  Next, we can select a continuum correction method

![Continuum Type](../../img/usage/continuumtype.png)

and set the end points for linear fitting.

![Continuum Limits](../../img/usage/continuumlimits.png)

Finally, we select the sectra with a left click, open a contextual menu with a right click, and select continuum correct.

![Continuum Corrected Context Menu](../../img/usage/continuumcontext.png)

The continuum corrected spectra is automatically added to the plot and can undergo further analysis.

![Continuum Corrected Spectra](../../img/usage/continuumcorrected.png)

## Derived Products
The map plot window is the 'main' window to interact with your map data.  For this short usage example, we will apply one of algorithms to derive a supplemental product - the olivine index.

<div class="note warning">
  <h5>Map Projected Data</h5>
  <p>
    We are still developing and testing visualization and analysis of map projected data.  Feel free to test our software with projected data and please [file an issue]({{site.repository}}/issue/new) if map projected data fails to load.
  </p>
</div>

The map plot window consists of a menu bar, toolbar, plot, and navigation bar (from top to bottom).  In the menu bar, many algorithms for creating deried products are provided. 

![Derived Products](../../img/usage/m3derived.png)

From <code>M3 Algorithms > Derived </code> select <code>Olivine Index</code>.  PySAT then applies the algorithm used to derive the olivine index and renders the output in supplemental window.  This window can be saved as a <code>.png</code> and added directly to a paper or exported as a geospatially tagged geotiff at full resolution and native data type.

![Derived - Olivine](../../img/usage/olivinederived.png)



