class Engine:
    def __init__(self, power=30e3):
        self.power = power

    def torque(self, speed, throttle):
        return (self.power / speed) * throttle
