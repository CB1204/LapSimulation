import numpy as np

class Track:
    def __init__(self, curvature, ds):
        n = curvature.shape[0]
        l = (n - 1) * ds
        self.s = np.linspace(0, l, n)
        self.curvature = curvature
        self.ds = ds