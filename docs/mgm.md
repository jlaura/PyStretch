---
layout: docs
title: MGM 
prev_section: clementine_derived
next_section: troubleshooting
permalink: /docs/mgm/
---

PySAT implements the [Modified Gaussian Model](http://www.planetary.brown.edu/mgm/) as a direct port of the MatLab Code released by Brown University.  MGM supports two data entry methodologies, (1) loading of <code>.fit</code> and <code>.asc</code> files and (2) direct integration with a plotted spectra.

##Loading parameter and wavelength files
To open a new MGM window, via the main menu bar select <code>Tools > Modified Gaussian Model</code>.  

![MGM Menu](../../img/mgm/mgmmenu.png)

A new, unpopulated MGM window is opened.  Opened using this method, the MGM windows expects that the user will supply, at a minimum, a spectra file with wavelength and natural log reflectance information.  Additionally, a user can supply a parameter file which loads polynomial coefficients, coefficient errors, absorption band information, continuum type, and stopping criteria.  

![Open Files](../../img/mgm/openfiles.png)

PySAT expects that data files will be in the same format as used by the original MatLab MGM code.

###Sample <code>.fit</code>
{% highlight bash %}
 :
 opx1b
 -220,50,50
 300,2600,300
.002,1E-06
 Q
   0.85E+00  -0.1E-05  0.0E+00   0.0E+00
   10.        0.1E-3   0.1E-6    0.1E-6
 3
   0.3330E+03   0.400E+03 -0.20E+02
   10000.         10000.    100.
   0.1000E+04   0.250E+03 -0.1E+01
   200.           400.      10.
   0.2000E+04   0.300E+03 -0.1E+01
   300.           400.      10.

 Old RMS  0.112768E-01     New RMS=  0.112768E-01     Imp=  0.651926E-08
{% endhighlight %}

###Sample <code>.asc</code>
{% highlight bash %}
 372.00      0.705308
 376.00      0.715715
 381.00      0.728052
 386.00      0.736994
 389.00      0.742412
 392.00      0.746045
{% endhighlight %}

Once loaded the user can modify all cells by simply clicking within them.  Locking and unlocking of parameters and band parameters is supported through contextual menus, i.e., it is possible to lock a column or row by right clicking on the column header or row number.

![Context](../../img/mgm/context.png)

<div class="note">
  <h5>Sample Data</h5>
  <p>The supplied sample data can be fit once before the stopping criteria are hit.  Selecting <code>Fit Until</code> will therefore only fit one time; the stopping criteria have been reached after a single iteration.</p>
</div>

Once fit, absoprtion band specifications are updated.  Additionally, PySAT has updated all of the plot lines.  These can be displayed via the <code>Display</code> menu.

![Display](../../img/mgm/display.png)

## Integration with PySAT  
<div class="note unreleased">
  <h5>Under Active Development</h5>
  <p>This functionality is in an alpha stage and undergoing development as the PySAT development team becomes more familiar with MGM parameterization.</p>
</div>

Alternatively, it is possible to interactively select a continuum corrected spectra from a plot window via the contextual menu.

![MGM Context](../../img/mgm/mgmcontext.png)

This opens a new MGM window, with the spectra added and the continuum parameters populated with a best guess continuum.

![MGM Main](../../img/mgm/mgmmain.png)

<div class="note warning">
  <h5>Linear Spline Coefficient Estimation</h5>
  <p>Moving between PySAT and the MGM interface, we estimate the standard form coefficients using a polynomial fit.  For regression and linear continuum this is a first order fit.  The Horgan correction method estimates a 3rd order polynomial.  We have decided to estimate the linear spline (3 point linear) using a second order polynomial.</p>
</div>



