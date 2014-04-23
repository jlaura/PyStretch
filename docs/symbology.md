---
layout: docs
title: Symbology
prev_section: plottypes
next_section: bandcharacterization
permalink: /docs/symbology/
---

Symbology is broadly divided into color ramps used for map visualization and plot symbology used for line and point representation.

##Color Ramps & Color Bars
PySAT utilizes the built-in color ramps that ship with MatPlotLib (hence the cryptic names).  To alter the colormap of map simply select a new entry from <code>Image > Change Color Map</code>.  

![Color Maps](../../img/symbology/colormap.png)

To add a colorbar to visualize the range of values displayed, simply select <code>Image > Color Bar: > Add</code>.

![Color Bar](../../img/symbology/colorbar.png)

<div class="note info">
  <h5>Updating a Colorbar</h5>
  <p>PySAT automatically updates the colobar when a stretch is applied or the colorramp is altered.</p>
</div>


##Plot Symbology

PySAT attempts to natively handle the most common synbology requirements without need for user interaction.  For example, PySAT cycles coloration of spectra to correspond to points plotted in a map frame.

Finer control of the symbology of all elements within a plot are provided via the navigation toolbar.  Simply click on the green check mark to manually alter the symbology of all elements of the plot.

![Toolbar2](../../img/plottypes/toolbar2.png)

<div class="note info">
  <h5>Symbology and Map Plots</h5>
  <p>A map plot with a color bar consists of two plotting axis.  When attempting to change the symbology of a point on a map plot - the first entry <i>should</i> be the map plot.</p>
</div>

Within the <code>Figure options</code> dialog the <code>Axes</code> tab controls extent, scaling, and titling options.  For example, to alter the min / max of a given axis, simply alter the range and click apply.  To utilize log scaling, simply select log from the scale drop down.

![Figure Options 1](../../img/symbology/figopt1.png)

The <code>Curves</code> tab controls the symbology of individual elements.  For example, it is possible to relabel (in the legend) a given line or alter the marker style such that each point observtion along a plotted specctra is identified.

![Figure Options 2](../../img/symbology/figopt2.png)




