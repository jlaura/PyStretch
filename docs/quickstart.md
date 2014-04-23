---
layout: docs
title: Quick-start guide
prev_section: home
next_section: installation
permalink: /docs/quickstart/
---

For the impatient, here's how to get up and running immediately.

## Binary Application (.app, .exe)

If you have downloaded the OS X application file, just double click it like any other application.

## Script
If you have the script directory or an 'all-in-one' directory:

{% highlight bash %}
~ $ cd /spectraviewer_directory 
~ $ python spectraviewer.py
{% endhighlight %}

This launches your X-server (on OS X and Windows) and displays the main interface or simply launches the interface (Linux).

<div class="note info">
  <h5>OS X Python</h5>
  <p>On OSX to run PySAT via the commandline is <code>pythonw spectraviewer.py</code>.  This ensures that PySide (PyQT) works properly and launches Python in windowed (the extra 'w') mode.</p>
</div>

If you're running into problems, ensure you have all the [requirements installed][Installation].

[Installation]: /docs/installation/
