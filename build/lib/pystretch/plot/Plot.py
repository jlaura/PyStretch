try:
    import pylab
except:
    print "Pylab not installed."

def show_hist(data_to_plot):
    '''This requires a fair bit of RAM as the array is duplicated.  NOT for large images'''
    pylab.hist(data_to_plot.flatten(), 256, range=(0.0, 255.0))
    pylab.show()

def show_plot(data_to_plot):
    pylab.plot(data_to_plot)
    pylab.show() 