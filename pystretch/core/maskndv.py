import numpy as np
import pystretch.core.globalarr as glb

def maskndv(ndv):
    return np.where(glb.sharedarray == ndv)[0]

