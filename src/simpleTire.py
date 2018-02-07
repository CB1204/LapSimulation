import numpy as np


class Tire:
    def __init__(self, pdx1=1.0, pdx2=-0.1, pdy1=1.0, pdy2=-0.2, fzn=2000, pkx1=10, pky1=-10):
        self.pdx1 = pdx1
        self.pdx2 = pdx2
        self.pdy1 = pdy1
        self.pdy2 = pdy2
        self.pkx1 = pkx1
        self.pky1 = pky1
        self.fzn = fzn

    def force(self, sr, sa, fz):
        nfz = (fz - self.fzn) / self.fzn
        mux = self.pdx1 + self.pdy2 * nfz
        nsr = self.pkx1 * sr / mux
        nfx = nsr / np.sqrt(1.0 + nsr ** 2)
        fxi = mux * nfx * fz

        muy = self.pdy1 + self.pdy2 * nfz
        nsa = self.pky1 * sa / muy
        nfy = nsa / np.sqrt(1 + nsa ** 2)
        fyi = muy * nfy * fz

        rxsr = 1 / (1 + nsr ** 2)
        rysa = 1 / (1 + nsa ** 2)

        gxsa = 1 / np.sqrt(1 + rxsr * nsa**2)
        gysr = 1 / np.sqrt(1 + rysa * nsr**2)

        fxc = gxsa * fxi
        fyc = gysr * fyi

        return [fxc, fyc]
