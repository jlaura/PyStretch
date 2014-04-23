---
layout: docs
title: Continuum Correction 
prev_section: requestformat
next_section: spectralsmoothing
permalink: /docs/continuumcorrection/
---

PySAT currently supports 4 different continuum correction methods: two point linear, piece-wise linear (three point linear), OLS regression, and a polynomial fit (Horgan).  Additionally, it is possible to plot the raw reflectance data and a continuum fit line.  The latter visualizes the raw reflectance and the fit line.  It does not perform the correction. 

![Continuum Type](../../img/continuumcorrection/continuumtype.png)

Parameterization of a continuum is accomplished by first selecting the method and then defining the end points.  PySAT utilizes three 'spinners' to define up to three endpoints.  The central spinner is only used with the piece-wise linear and polynomial fits.

![Continuum Bounds](../../img/continuumcorrection/continuumbounds.png)

<div class="note">
  <h5>OLS Regression</h5>
  <p>OLS regression does not require that end points are defined.  A regresison line is fit to the global data.</p>
</div>

## Linear
The classic continuum correction method.  We fit a line between the two end points and divide the raw reflectance by that line.

![Linear](../../img/continuumcorrection/linear2.png)

## Piece-wise Linear
As above, except we fit two lines to the spectra.  This is the method frequently used to perform a linear correction of the M3 data, where a 1um and 2um absoprtion exist.

![Piece-Wise Linear](../../img/continuumcorrection/linear3.png)


## OLS Regression
PySAT treats reflectance observation as a discreet value (which it is) and utilizes classic Ordinary Least Squares (OLS) regression to generate a 'best-fit' line.  This is the method used by the SP team.

![OLS](../../img/continuumcorrection/regression.png)


## Polynomial 
Dubbed the 'Horgan' method, PySAT fits a piecewise, second order polynomial to the continuum.  This method seeks to find the maximum within a given range and use that local maxima as an endpoint.  To support this, PySAT has a spin box adjacent to the <code>Horgan</code> radio button.  This spinner controls the extent to which PySAT searchs for a maxima (centered on the continuum limits.  For example, if the spinner is set to 100 and the lower bound is set to 750, PySAT selects the maximum value between 650 and 850. 

![Horgan](../../img/continuumcorrection/horgan.png)

