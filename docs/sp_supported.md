---
layout: docs
title: Spectral Profiler
prev_section: m3_supported
next_section: mi_supported
permalink: /docs/sp_supported/
---

Spectral profiler is a spot profiler that records down the center of an MI image.  We parse the spectral profiler binary data and approximate the location of the spots within the frame.

<div class="note warning">
  <h5>Spot placement</h5>
  <p>SP spot placement is approximate (naive).  We assume that spots are placed with equal spacing down the center of the reference image.  We assume that the <code>*P.jpg</code> image is shipped to us with the correct orientation and that the imager images at an equal interval.  Additionally, this method discount the curvature of the body.  If you have an improved method for surface placement [file and issue]({{site.repository}}/issues/new)</p>
</div>

Spectral profiler ships data with a <code>.sl2</code> file suffix.  This can be renamed to <code>.zip</code> and opened normally.  Within the directory are three or four files:

1. \*.jpg - A thumbnail image.  We ignore this image, if the \*P.jpg is available.
2. \*P.jpg - The full resolution reference image.  This image is often, but not always included.
3. \*.spc - The binary data.
4. \*.ctg - A pseudo-world file that described that data in plain text.

<div class="note warning">
  <h5>.spc</h5>
  <p>PySAT expects that you will keep the SP files together in the same directory</p>
</div>

When opening an SP image, PySAT expects to be aimed at the <code>.spc</code>.  If you point at the <code>jpg</code> the default loader will load the reference image, but the spot spectrometer data will not be available.

![Open SP](../../img/sp_supported/openspc.png)

PySAT parses the image header, extracts all observations, cleans the data, and performs photometric correction.  The data is then ready for processing.

![Sample SP Data](../../img/sp_supported/samplespc.png)
