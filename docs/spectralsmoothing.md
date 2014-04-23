---
layout: docs
title: Spectral Smoothing 
prev_section: continuumcorrection
next_section: plottypes
permalink: /docs/spectralsmoothing/
---

PySAT supports smoothing of noisy spectra.  Spectral smoothing can be applied in one of two ways.  Both methods are managed via the Spectral Smoothing Dock.

![Smoothing Dock](../../img/spectralsmoothing/dock.png)

For automatic smoothing, select the <code>Smooth</code> radio button.  For manual smoothing, the radio buttons are ignored.

We utilize a box filter with a two-tailed extent.  For the default of 7, this means that a window (box filter) is centered on each spectra and the average computed from three neighbors above and three neighbors below. 

<div class="note info">
  <h5>Spectral Resolution and Smoothing</h5>
  <p>The PySAT spectral smoothing algorithm defines neighbors based upon number of bands and not spectral resolution.  Therefore, composite imstruments that have multiple spectral resolutions are smoothed based solely upon the number of bands without regard for the band spacing.</p>
</div>


##Automatic Smoothing 
To enable automatic smoothing, select the <code>Smooth</code> radio button from the Spectral Smoothing dock.  When clicking on a map window, the reflectance or continuum removed reflectacne values will be automatically smoothed using a box filter to the desired distance.

##Manual Smoothing
Using a contextual menu, it is possible to plot the unsmoothed spectra and then add a smoothed spectra to the same plot.  The amount of smoothing is controlled by the <code>Two Tailed Distance</code> spinner.  

<div class="note">
  <h5>No Smoothing or Smoothing?</h5>
  <p>When manually smoothing a spectra, PySAT assumes that you wish to apply the smoothing algorithm (you did click on the menu item to smooth).  Therefore, PySAT ignores the <code>No Smoothing</code> and <code>Smoothing</code> radio buttons.</p>
</div>

![Smoothing Context](../../img/spectralsmoothing/context.png)

The smoothed spectra is then added to the plot.

![Smoothed](../../img/spectralsmoothing/smoothed.png)

Within the literature, it is common to see plots with the smoothed spectra as continuous data and the raw spectra as discrete data.  PySAT supports this by allowing you to alter the [symbology of a spectra](../symbology/).

![Smoothed with points](../../img/spectralsmoothing/smoothedpts.png)



 
