import time

def starttimer():
    starttime = time.time()
    return starttime

#Determine total processing time.
def totaltime(starttime):
    endtime = time.time()
    totaltime = round(endtime-starttime)
    if totaltime <= 60:
        print "Total time to process the image was " + str(totaltime) + " seconds."
    else:
        totalminutes = int(totaltime / 60)
        totalseconds = int(totaltime % 60)
        if totalseconds < 10:
            totalseconds = str(0) + str(totalseconds)
        print "Total time to process the image was " + str(totalminutes) + ':' + str(totalseconds) + '.'