---
layout: docs
title: Installation
prev_section: quickstart
next_section: usage
permalink: /docs/installation/
---

Getting PySAT installed and ready-to-go should only take a few minutes.  It it ever becomes difficult, please [file an
issue]({{ site.repository }}/issues/new) (or submit a pull request)
describing the issue you encountered and how we might make the process easier.

The remainder of this section assumes that you would like to run PySAT via the command-line, not using one of the precompiled binaries.   If you are running a binary, we have shipped everything that you should need.  If the binary is not working, please  please [file an issue]({{ site.repository }}/issues/new) with as much information as possible.

### Requirements

Installing PySAT is easy and straight-forward, but there are a few requirements
you’ll need to make sure your system has before you start.

- [Python 2.7.x](https://store.continuum.io/cshop/anaconda/) (Free)
- [Geospatial Data Abstraction Library](http://www.gdal.org)
- Linux, Unix, or Mac OS X

<div class="note info">
  <h5>Anaconda Python</h5>
  <p>
   While any installation of Python 2.7.x will work, we suggest using Anaconda Python.  This is a free Python distirbution that is designed to support scientific computing.  It ships with many of the other Python libraries that we depend on.  If you do not wish to utilize Anaconda, make sure that you have: NumPy, SciPy, MatPlotLib, PySide and the GDAL Python bindings installed.
  </p>
</div>

## Installing GDAL on OS X

The most onerous task is the installation of GDAL and the GDAL Python bindings.  For this reason, we suggest that you utilize the precompiled binaries that ship with PySAT.

### OS X

Other then installing from source, two options for installing GDAL are:

1. [KyngChaos Binary Installer](http://www.kyngchaos.com/software/frameworks) - We suggest the GDAL Complete installation.
2. [Homebrew](http://brew.sh) - An OS X package manager.

{% highlight bash %}
~ $ brew install gdal
{% endhighlight %}


### Windows
Multiple options exist to support the installation of GDAL on windows.

1. [Christoph Gohlke's Binary Installer](http://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal)
2. [OSGeo4W](https://trac.osgeo.org/osgeo4w/)
3. [Tamas Szekeres' Binary Installer](http://www.gisinternals.com/sdk/)

## Pre-releases

If you pull our code from [our repository]({{ site.repository }}) you will be getting the freshest, pre-release code.  Currently, we do note make use of any compiled code (e.g. Cython) and you can run at the bleeding edge via the [commandline](../quickstart).

To grab the prerelease:

{% highlight bash %}
~ $ git clone git://github.com/jlaura/pysat.git
~ $ cd pysat
~ $ python(w) spectraviewer.py
{% endhighlight %}



Running pre-release assumes that you are installing all of the necessary dependencies and that they are up to date.  Additionally, preprelease might be passing all our doctests, but hiding some bugs - you have been warned.  

