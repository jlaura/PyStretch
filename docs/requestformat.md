---
layout: docs
title: Request Format
prev_section: mi_supported
next_section: continuumcorrection
permalink: /docs/requestformat/
---

PySAT currently supports a limit number of images and an even smaller number of formats for hyper-spectral analysis.  Inclusion of new formats is dependent upon input from the community.

##How can I get a new format added?
Please [file an enhancement request]({{site.repository}}/issues/new) so that we know how to better serve you.  

##What is the processes to get a new format added?
If we already have a reader, for example for M3, but you would like the reader to support <code>.cub</code> formatted M3 data, we can quickly write an extension to our driver.

If we do not have a native reader, we will need to spend a bit of time determing how best to parse the header data to extract essential wavelength information.  Any insight you can provide is appreciated (but not essential).

##Contributing
If you are comfortable in Python and with the data you require, please condsider [submitting a pull request]({{site.repository}}/pulls) with the updated driver infrormation to share with the rest of the community.
