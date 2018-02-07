from LSvehicleOneDimLookup_2 import vehicleOneDimLookup_2 as vehicle_ODL_2
from LSvehicleTwoDimLookup_2 import vehicleTwoDimLookup_2 as vehicle_TDL_2
from TwoDimLookup_motor import TwoDimLookup_motor as motor_TDL
from scipy import interpolate
import numpy as np


class Acceleration:
    def __init__(self, Vehicle):
        self.Vehicle = Vehicle
        
    def AccelTime(self):
        VehicleSpeed = np.array([np.linspace(0.0001, 60, 200), np.zeros(200)])
        VehicleSpeed = np.transpose(VehicleSpeed).tolist()  #calculate vehicle speed
        
        #initialize vehicle motor
        Motor = motor_TDL(self.Vehicle.gearRatio, self.Vehicle.tireRadius, self.Vehicle.CoG_X, self.Vehicle.m, self.Vehicle.CoP_X, self.Vehicle.C_la, self.Vehicle.rho, self.Vehicle.fr, self.Vehicle.Lift2Drag, self.Vehicle.DriveType)
        ax_Motor = Motor.ax_motor(VehicleSpeed) #calculate acceleration in x
        
        speed = np.linspace(0.0001, 60, 200)
        a = interpolate.interp1d(speed, ax_Motor, bounds_error=False, fill_value=0)

        #set start lists
        v = [0.0001]
        s = [0]
        t = [0]
        delta_t = 0.005
        t_end = 6

        while t[-1] <= t_end:   #calculate acceleration, speed and distance
            a_v = a(v[-1])
            v_t = a_v * delta_t + v[-1]
            s_t = 0.5 * a_v * delta_t**2 + v[-1] * delta_t + s[-1]
            
            v.append(v_t)
            s.append(s_t)
            t.append(t[-1] + delta_t)
        
        index2 = np.nonzero(np.asarray(s) <= 75)
        index_75m = np.max(index2)  #get last value from distance array
        
        return t[index_75m] #get time value for last distance value