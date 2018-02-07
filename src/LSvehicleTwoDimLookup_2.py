from TwoDimLookup_motor import TwoDimLookup_motor as motor_TDL
from scipy.interpolate import RegularGridInterpolator as RGI
from GG_ESB import GG_ESB_TwoDim
from sliceable import Sliceable
#from statsmodels.tsa.kalmanf.kalmanfilter import rho
import numpy as np

class vehicleTwoDimLookup_2:
    def __init__(self, C_F, C_R, m, CoG_X, mu, alpha, CoP_X, C_la, rho, DriveType, gearRatio, tireRadius, fr, Lift2Drag, CarName, Pmax):
        self.C_F = C_F  #Cornering stiffnes front [N/rad]
        self.C_R = C_R  #Cornering stiffnes rear [N/rad]
        self.m = m      #Weight [kg] including driver
        self.CoG_X = CoG_X  #Center of gravity (0 at front axis, 1 at rear axis)
        self.mu = mu        #Friction coefficient between tire gum and street
        self.alpha = alpha  #Slip angle as optimum value [deg]
        self.CoP_X = CoP_X  #Center of pressure
        self.C_la = C_la    #Coefficient (lift coefficient*front area)
        self.rho = rho      #Rho
        self.DriveType = DriveType  #2WD or 4WD
        self.gearRatio = gearRatio
        self.tireRadius = tireRadius
        self.fr = fr        #Friction coefficient
        self.Lift2Drag = Lift2Drag
        self.CarName = CarName
        self.Pmax = Pmax
        self.DrivingRes = None

        # Create GGV Map
        ggVMap = GG_ESB_TwoDim(C_F, C_R, m, CoG_X, mu, alpha, CoP_X, C_la, rho, DriveType, gearRatio, tireRadius, fr, Lift2Drag )
        ax_upper_values, ax_lower_values, ay_values, speed_values = ggVMap.GGV_Map()
        #ggVMap.Plot_ggV(ax_upper_values, ax_lower_values, ay_values, speed_values) # Plot GGV map
        ggVMap.Plot_Long_Speed_Distance()
        
        # ax_max, ax_min
        self.x_u = np.asarray(ax_upper_values)
        self.x_l = np.asarray(ax_lower_values)
        
        # ay
        self.y = np.asarray(ay_values)
        
        # vehicle speed
        self.v = np.asarray(speed_values)
        
        # find spot where ay is at it's max
        ymaxind = np.argmax(self.y[0, :])
        
        # find corresponding ax, ay, v
        self.xmax = self.x_u[:, ymaxind]
        self.ymax = self.y[:, ymaxind]
        self.vmax = self.v[:, ymaxind]

        # find limits when simulating forward and backward
        self.lim_f = RGI([self.v[:, 0], self.y[0, :ymaxind+1]/self.y[0, ymaxind]], self.x_u[:, :ymaxind+1])
        self.lim_r = RGI([self.v[:, 0], self.y[0, :ymaxind+1]/self.y[0, ymaxind]], self.x_l[:, :ymaxind+1])
        # find limit for lateral acceleration based on vehicle parameters
        self.lim_ay = RGI([(self.v[:, ymaxind])], self.y[:, ymaxind])
        
        
        self.upper_max_speed = self.vmax.max()
        self.min_curvature = self.y.max() / self.upper_max_speed**2

    def create_state(self, ls):
        n = ls.trackmap.curvature.shape[0]
        return State(n, maxspeed=self.upper_max_speed)

    def max_speed_calc(self, ls):
        k = np.fabs(ls.trackmap.curvature)
        corner = k > self.min_curvature

        bins = self.ymax/(self.vmax**2)
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

    def lim_accel(self, ls, state): #zeigt, was das Fzg kann
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
                ax = self.lim_f(np.concatenate([state.speed, ay_norm],axis=1))  #forward
            else:
                ax = self.lim_r(np.concatenate([state.speed, ay_norm],axis=1))  #backward

            ls.run = True

        else:   #no CPs
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
