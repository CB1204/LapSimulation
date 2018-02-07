import numpy as np
from simpleTire import Tire
from simpleAero import Aero
from sliceable import Sliceable


class vehicleAeroMassTire:
    def __init__(self,
                 mass=350,
                 tire=Tire(),
                 aero=Aero(),
                 upper_max_speed=30,
                 min_curvature = 1e-2,
                 gravity = 9.81):
        self.mass = mass
        self.tire = tire
        self.aero = aero
        self.upper_max_speed = upper_max_speed
        self.min_curvature = min_curvature
        self.gravity = gravity

    def create_state(self, ls):
        n = ls.trackmap.curvature.shape[0]
        return State(n, maxspeed=self.upper_max_speed)

    def max_speed_calc(self, ls):

        k = np.fabs(ls.trackmap.curvature)
        corner = k > self.min_curvature

        a = (self.aero.Cdft**2)*self.tire.pdy2/self.tire.fzn

        if a != 0:
            b = self.aero.Cdft*(self.tire.pdy1+self.tire.pdy2*((2*self.mass*self.gravity-self.tire.fzn)/self.tire.fzn))-k[corner]*self.mass
            c = self.mass*self.gravity*(self.tire.pdy1+self.tire.pdy2*((self.mass*self.gravity-self.tire.fzn)/self.tire.fzn))
            max_speed = np.sqrt(np.maximum((-b + np.sqrt(b**2 - 4*a*c))/(2*a),(-b - np.sqrt(b**2 - 4*a*c))/(2*a)))
        else:
            max_speed = np.sqrt(self.tire.pdy1 * self.gravity / (k[corner] - self.tire.pdy1*self.aero.Cdft/self.mass))

        ls.state_max.speed[corner] = np.transpose([max_speed])
        ls.state_max.AccelX[corner] = -self.aero.Cd * ls.state_max.speed[corner]**2 / self.mass

    def lim_accel(self, ls, state):
        va = state.speed
        k = ls.trackmap.curvature[[ls.counter]]
        cp = ls.counter in ls.critical_points

        Fz = self.mass * self.gravity + self.aero.Cdft * va**2
        fzn = (Fz - self.tire.fzn)/self.tire.fzn
        muy = self.tire.pdy1 + self.tire.pdy2 * fzn
        mux = self.tire.pdx1 + self.tire.pdx2 * fzn
        fx_aero = -self.aero.Cd * va**2

        Fzn = Fz / self.mass
        ay_max = muy * Fzn
        ay = np.abs(va**2*k)

        if (ay <= ay_max) | cp:
            if cp:
                ay_norm = 1.0
            else:
                ay_norm = ay/ay_max

            if ls.dir == 1:
                ax = mux * Fzn * (1 - ay_norm) + fx_aero / self.mass
                ax = np.minimum((30e3 / va + fx_aero) / self.mass, ax)
            else:
                ax = -mux * Fzn * (1 - ay_norm) + fx_aero / self.mass

            ls.run = True

        else:
            ax = 0
            ls.run = False

        state.speed = np.sqrt(va**2 + 2 * ax * ls.trackmap.ds * ls.dir)
        state.AccelX = ax
        return state


class State(Sliceable):
    def __init__(self, n, maxspeed=100):
        self.speed = np.ones((n, 1)) * maxspeed
        self.AccelX = np.zeros((n, 1))
