import numpy as np
from scipy.interpolate import interp1d
from sliceable import Sliceable


class vehicleOneDimLookup:
    def __init__(self, latG = 2*9.81, driveG = 9.81, brakeG = -9.81, upper_max_speed=1000):
        self.lim_ay = latG
        self.lim_f = interp1d([0.0, 1.0], [driveG, 0.0,])
        self.lim_r = interp1d([0.0, 1.0], [brakeG, 0.0,])
        self.upper_max_speed = upper_max_speed
        self.min_curvature = latG / upper_max_speed**2

    def create_state(self, ls):
        n = ls.trackmap.curvature.shape[0]
        return State(n, maxspeed=self.upper_max_speed)

    def max_speed_calc(self, ls):
        k = np.fabs(ls.trackmap.curvature)
        corner = k > self.min_curvature

        ls.state_max.speed[corner] = np.transpose([np.sqrt(self.lim_ay/np.fabs(k[corner]))])

    def lim_accel(self, ls, state):
        k = ls.trackmap.curvature[[ls.counter]]
        cp = ls.counter in ls.critical_points
        ay = np.abs(state.speed**2*k)
        if (ay <= self.lim_ay) | cp:
            if cp:
                ay_norm = 1.0
            else:
                ay_norm = ay/self.lim_ay

            if ls.dir == 1:
                ax = self.lim_f(ay_norm)
            else:
                ax = self.lim_r(ay_norm)

            ls.run = True

        else:
            ax = 0
            ls.run = False

        state.speed = np.sqrt(state.speed**2 + 2 * ax * ls.trackmap.ds * ls.dir)
        state.AccelX = ax
        return state


class State(Sliceable):
    def __init__(self, n, maxspeed=100):
        self.speed = np.ones((n, 1)) * maxspeed
        self.AccelX = np.zeros((n, 1))
