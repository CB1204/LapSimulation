import numpy as np


class Aero:
    def __init__(self,reference_down_force = np.array([ 1000,  1000 ]), reference_drag = 500, reference_speed = 20):
        self.reference_down_force = reference_down_force
        self.reference_drag = reference_drag
        self.reference_speed = reference_speed
        self.Cdft = np.sum(self.reference_down_force) / (self.reference_speed**2)
        self.Cdf = self.reference_down_force / (self.reference_speed**2)
        self.Cdr = self.reference_down_force / (self.reference_speed**2)
        self.Cd = self.reference_drag / (self.reference_speed**2)

    def down_force(self,state):
        return self.reference_down_force * (state.speed/self.reference_speed)**2

    def drage(self,state):
        return self.reference_drag * (state.speed/self.reference_speed)**2