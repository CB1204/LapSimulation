from TwoDimLookup_motor import TwoDimLookup_motor as motor_TDL
from GG_ESB import GG_ESB_OneDim
from sliceable import Sliceable
import numpy as np


class vehicleOneDimLookup_2:
    def __init__(self, C_F, C_R, m, CoG_X, mu, alpha, DriveType, CarName, Pmax, upper_max_speed=50):
        self.C_F = C_F  #Cornering stiffnes front [N/rad]
        self.C_R = C_R  #Cornering stiffnes rear [N/rad]
        self.m = m      #Weight [kg]
        self.CoG_X = CoG_X  #Center of gravity (0 at front axis, 1 at rear axis)
        self.mu = mu    #Friciton coefficient between tire gum and street
        self.alpha = alpha  #Slip angle as optimum value [deg]
        self.DriveType = DriveType  #2WD or 4WD
        self.CarName = CarName
        self.Pmax = Pmax
        self.DrivingRes = None
        
        #Values of vehicleTwoDimLookup_2
        self.gearRatio = 12.98
        self.tireRadius = 0.2286
        self.CoP_X = 0.61
        self.C_la = 3.2
        self.rho = 1.22
        self.fr = 0.013
        self.Lift2Drag = 2.05 

        ggMap = GG_ESB_OneDim(C_F, C_R, m, CoG_X, mu, alpha, DriveType)
        
        self.ay_max = ggMap.GG_ESB_ay_Max() 
        self.ax_max = ggMap.GG_ESB_ax_Max()
        
        ##ggMap.Plot_gg(self.ay_max, self.ax_max)  # Plot gg map
        
        self.upper_max_speed = upper_max_speed
        self.min_curvature = self.ay_max / upper_max_speed**2
        
        self.DriveType = DriveType

    def create_state(self, ls):
        n = ls.trackmap.curvature.shape[0]
        return State(n, maxspeed=self.upper_max_speed)

    def max_speed_calc(self, ls):
        k = np.fabs(ls.trackmap.curvature)
        corner = k > self.min_curvature

        ls.state_max.speed[corner] = np.transpose([np.sqrt(self.ay_max/np.fabs(k[corner]))])

    def lim_accel(self, ls, state):
        k = ls.trackmap.curvature[[ls.counter]]
        cp = ls.counter in ls.critical_points
        ay = np.abs(state.speed**2*k)
        if (ay <= self.ay_max) | cp:
            if cp:
                ay = self.ay_max

            if ls.dir == 1:
                ax = ((1-(ay**2 / self.ay_max**2)) * self.ax_max**2)**0.5
            else:
                if self.DriveType == '2WD':
                    ax = (-2) * ((1-(ay**2 / self.ay_max**2)) * self.ax_max**2)**0.5
                if self.DriveType == '4WD':
                    ax = (-1) * ((1-(ay**2 / self.ay_max**2)) * self.ax_max**2)**0.5
            
            ls.run = True

        else:
            ax = 0
            ls.run = False

        state.speed = np.sqrt(state.speed**2 + 2 * ax * ls.trackmap.ds * ls.dir)
        state.AccelX = ax
        
        #Initialize motor
        Motor = motor_TDL(self.gearRatio, self.tireRadius, self.CoG_X, self.m, self.CoP_X, self.C_la, self.rho, self.fr, self.Lift2Drag, self.DriveType)
        self.DrivingRes = Motor.Driving_Resistances(state.speed)    #calculate driving resistances
        
        return state


class State(Sliceable):
    def __init__(self, n, maxspeed=100):
        self.speed = np.ones((n, 1)) * maxspeed
        self.AccelX = np.zeros((n, 1))
