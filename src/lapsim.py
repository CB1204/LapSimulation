from LSvehicleOneDimLookup_2 import vehicleOneDimLookup_2 as vehicle_ODL_2
from LSvehicleTwoDimLookup_2 import vehicleTwoDimLookup_2 as vehicle_TDL_2
from TwoDimLookup_motor import TwoDimLookup_motor as motor_TDL
import numpy as np


class LapSim:
    def __init__(self, vehicle, trackmap):
        self.state_max = None
        self.state_f = None
        self.state_r = None
        self.state = None
        self.critical_points = None
        self.dir = None
        self.run = None
        self.vehicle = vehicle
        self.trackmap = trackmap
        self.counter = None
        self.lapTime = None
        self.direction = None
        self.max_laps = 1
        self.UsedEnergy = None
        self.AccelX = None
        
    def speed_profile(self):
        # Initialize zero states for the lap
        self.state_max = self.vehicle.create_state(self)  # max speed sim
        self.state_f = self.vehicle.create_state(self)  # forward sim
        self.state_r = self.vehicle.create_state(self)  # reverse sim
        self.state = self.vehicle.create_state(self)  # combined forward/reverse
        
        # Max speed calculation
        self.vehicle.max_speed_calc(self)
        self.find_critical_points()

        # speed profile calculation
        for cp in self.critical_points:
            if self.is_good_critical_point(cp):
                # Forward simulation
                self.dir = 1
                self.prop_speed_profile(cp)
                # Backward simulation
                self.dir = -1
                self.prop_speed_profile(cp)
                
        # process results
        self.finalize()
        
    def prop_speed_profile(self, cp):
        # propagates speed profile in the forward or reverse direction depending on self.dir
        self.counter = cp
        self.run = True
        lap = 0

        while self.run & (lap <= self.max_laps):
            #print("lap = %d maxlap = %d" %( lap, self.max_laps))
            #print(cp)
            lap += (self.counter == cp)
            #print('lap %d' %lap)
            if self.dir == 1:
                state = self.state_f[self.counter]
            elif self.dir == -1:
                state = self.state_r[self.counter]

            state = self.vehicle.lim_accel(self, state)
            if self.run & (state.speed < self.vehicle.upper_max_speed):
                self.step(state)
            else:
                self.run = False
            
    def find_critical_points(self):
        maxspeedlong = self.state_max.speed[np.r_[-1, :len(self.state_max.speed), 1]]
        ax = (maxspeedlong[1:] ** 2 - maxspeedlong[:-1] ** 2) / (2 * self.trackmap.ds)#
        
        #calculate the acceleration for x, but cut off one position for an array of [2035]
        AccelXmaxspeedlong = self.state_max.speed[np.r_[-1, :len(self.state_max.speed)-1, 1]]
        self.AccelX = (AccelXmaxspeedlong[1:] ** 2 - AccelXmaxspeedlong[:-1] ** 2) / (2 * self.trackmap.ds)
        # check if each point is...
        gt_pre = self.state_max.AccelX > ax[:-1]  # greater than the previous
        lt_pre = self.state_max.AccelX < ax[:-1]  # less than the previous
        gt_next = self.state_max.AccelX > ax[1:]  # greater than the next
        lt_next = self.state_max.AccelX < ax[1:]  # less than the next

        # A point could be a critical point if its acceleration is:
        # - greater than previous and less than next (common)
        # - less than previous and greater than next (common)
        # - two other odd case are possible each resulting in two adjacent critical points (not common)

        cp = np.where((gt_pre & lt_next) |
                      (lt_pre & gt_next) |
                      ((gt_pre & gt_next) & np.roll((lt_pre & lt_next), -1)) |
                      (np.roll((gt_pre & gt_next), 1) & (lt_pre & lt_next)) |
                      ((lt_pre & lt_next) & np.roll((gt_pre & gt_next), -1)) |
                      (np.roll((lt_pre & lt_next), 1) & (gt_pre & gt_next)))[0]
        #print('CP:' + str(cp))
        # sort critical points from slowest to fastest
        ind = np.argsort(self.state_max.speed[cp, 0])
        #print('IND:' + str(ind))
        self.critical_points = np.array([cp[i] for i in ind])
        
    def is_good_critical_point(self, cp):
        # make sure the critical has not already been "covered" by another
        if (self.state_max.speed[cp] < self.state_f.speed[cp]) & \
           (self.state_max.speed[cp] < self.state_r.speed[cp]):
            self.state_f[cp] = self.state_r[cp] = self.state_max[cp]
            return True

        else:
            return False
        
    def step(self, state):
            self.counter += self.dir  # increment counter
            # write successful step to appropriate state
            self.counter = self.counter % self.state_f.speed.size
            if self.dir == 1:
                self.state_f[self.counter] = state
            if self.dir == -1:
                self.state_r[self.counter] = state

            # wrap around start/finish line (first and last points are identical)
            if self.dir == 1:
                if self.counter == (self.state_f.speed.size - 1):
                    self.counter = 0
                    self.state_f[self.counter] = state

            else:
                if self.counter == 0:
                    self.counter = (self.state_r.speed.size - 1)
                    self.state_r[self.counter] = state
            
    def finalize(self):
        # combine forward and reverse simulations
        speed = np.minimum(self.state_f.speed, self.state_r.speed)
        self.direction = 1 * (self.state_f.speed == speed) - 1 * (self.state_r.speed == speed)
        self.state[self.direction[:, 0] == 1] = self.state_f[self.direction[:, 0] == 1, :]
        self.state[self.direction[:, 0] == -1] = self.state_r[self.direction[:, 0] == -1]
        self.state[self.direction[:, 0] == 0] = self.state_max[self.direction[:, 0] == 0]
        self.lapTime = np.sum(self.trackmap.ds / self.state.speed)
        
        #Energy calculation and power limitation
        dT = self.trackmap.ds / self.state.speed
        DrivingResistances = self.vehicle.DrivingRes    #get driving resistances of the vehicle
        Force = self.vehicle.m*self.AccelX              #calculate the force of the vehicle
        Power = (Force + DrivingResistances)*self.state.speed   #calculate power
        
        if(Power.any() > self.vehicle.Pmax):    #consider the power limitation --> ueberarbeiten hier nur bei energy --> falsche stelle in accelX
            Power = self.vehicle.Pmax
        else:
            Power = Power

        self.UsedEnergy = sum(Power * dT)   #calculate the used energy
        
