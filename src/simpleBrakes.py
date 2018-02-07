import numpy as np


class Brakes:
    def __init__(self, gain=np.array((350, 350, 200, 200))):
        self.gain = gain # max Nm torque

    def torque(self, pedal):
        return pedal * self.gain
