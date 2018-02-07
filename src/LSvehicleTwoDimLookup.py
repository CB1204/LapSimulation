import numpy as np
import scipy.interpolate
from sliceable import Sliceable


class vehicleTwoDimLookup:
    def __init__(self,
                 x=np.array([[1.0, -0.1, -1.0], [0.25, -0.2, -1.25], [0.05, -0.5, -2.0]])*9.81,
                 y=np.array([[0.0,  1.5,  0.0], [0.0,  1.75,  0.0], [0.0,  3.0,  0.0]])*9.81,
                 v=np.array([[5, 5, 5], [20, 20, 20], [60, 60, 60]]),
                 upper_max_speed=60
                 ):

        self.x = x
        self.y = y
        self.v = v
        ymaxind = np.argmax(y[0, :])
        self.xmax = x[:, ymaxind]
        self.ymax = y[:, ymaxind]
        self.vmax = v[:, ymaxind]

        self.lim_f = RGI([v[:, 0], y[0, :ymaxind+1]/y[0, ymaxind]], x[:, :ymaxind+1])
        self.lim_r = RGI([v[:, 0], y[0, :ymaxind+1]/y[0, ymaxind]], x[:, ymaxind:][:, ::-1])
        self.lim_ay = RGI([(v[:, ymaxind])], y[:, ymaxind])

        self.upper_max_speed = upper_max_speed
        self.min_curvature = y.max() / upper_max_speed**2

    def create_state(self, ls):
        n = ls.trackmap.curvature.shape[0]
        return State(n, maxspeed=self.upper_max_speed)

    def max_speed_calc(self, ls):
        k = np.fabs(ls.trackmap.curvature)
        corner = k > self.min_curvature

        bins = self.ymax/(self.vmax**2)
        print(bins)
        pos = np.minimum(np.searchsorted(-bins, -k)-1, self.xmax.shape[0]-2)[corner]
        x0 = self.xmax[:-1][pos]
        x1 = self.xmax[1:][pos]-self.xmax[:-1][pos]
        y0 = self.ymax[:-1][pos]
        y1 = self.ymax[1:][pos]-self.ymax[:-1][pos]
        v0 = self.vmax[:-1][pos]
        v1 = self.vmax[1:][pos]-self.vmax[:-1][pos]

        k = k[corner]
        a = k*(v1**2)
        b = 2*k*v1*v0-y1
        c = k*(v0**2)-y0
        ns = (-b + np.sqrt((b**2)-4*a*c))/(2*a)
        
        # ax_max[corner] = x0 + x1*ns
        # ay_max = y0 + y1*X
        # max_speed[corner] = v0 + v1*ns

        ls.state_max.speed[corner] = np.transpose([v0 + v1*ns])
        ls.state_max.AccelX[corner] = np.transpose([x0 + x1*ns])

    def lim_accel(self, ls, state):
        k = ls.trackmap.curvature[ls.counter]
        cp = ls.counter in ls.critical_points
        ay = np.abs(state.speed**2*k)

        ay_max = self.lim_ay(state.speed)
        if (ay <= ay_max) | cp:
            if cp:
                ay_norm = np.array([[1.0]])
            else:
                ay_norm = ay/ay_max
                
            if ls.dir == 1:
                ax = self.lim_f(np.concatenate([state.speed, ay_norm],axis=1))
            else:
                ax = self.lim_r(np.concatenate([state.speed, ay_norm],axis=1))

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
