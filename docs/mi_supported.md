---
layout: docs
title: Multiband Imager 
prev_section: sp_supported
next_section: requestformat 
permalink: /docs/mi_supported/
---

PySAT supports Multiband Imager in ISIS3 <code>.cub</code> format.

![MI Sample](../../img/mi_supported/misample.png)

<div class="note info">
  <h5>Overviews or Pyramids</h5>
  <p>
    Overviews are lower resolution versions of an image that support faster screen rendering.  The <code>.cub</code> format does not support overviews.  Therefore, the entire, full resolution image must be read from disk and rendered.  To improve performance, PySAT samples the data, if either the number of lines or number of samples is greater than 2000.  We hope to support overviews in other image formats in the future and to provide a preference where a user can disable this sampling at the cost of rendering performance.
  </p>
</div>




Multiband Imager is composed of two disrete imagers that overlap at 1000nm.  PySAT renders the spectra as a single spectrum by averaging the reflectance at the overlap.

![MI Reflectance](../../img/mi_supported/miref.png)
