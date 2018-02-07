from TwoDimLookup_motor import TwoDimLookup_motor
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np


### Input Parameters
# C_F = 27000        # Cornering stiffness front / Schräglaufsteifigkeit vorne [N/rad] - Is already for two wheels !
# C_R = 35000        # Cornering stiffness rear / Schräglaufsteifigkeit hinten [N/rad] - Is already for two wheels !
# m = 350            # Mass vehicle + driver [kg]
# CoG_X = 0.65       # Actual position of CG (0 at front axis, 1 at rear axis)
#  
# mu = 1.4           # Friction coefficient 
# alpha = 7.5        # Slip angle [deg]

# DriveType = 2WD or 4WD

# res = resolution = number of data points

class GG_ESB_OneDim:
    def __init__(self, C_F, C_R, m, CoG_X, mu, alpha, DriveType):
        
        self.C_F = C_F
        self.C_R = C_R
        self.m = m
        self.CoG_X = CoG_X
        self.mu = mu
        self.alpha = alpha
        self.DriveType = DriveType
        
        # General constants
        self.deg2rad = np.pi/180
        self.g = 9.81
           
    def GG_ESB_ay_Max(self):

        # calculate ay max 
        FY_F = self.alpha * self.deg2rad * self.C_F         
        FY_R = self.alpha * self.deg2rad * self.C_R         

        FY_ovr = FY_F + FY_R
        
        ay_max = FY_ovr / self.m
        #ay_max = 14
        return ay_max

    def GG_ESB_ax_Max(self):

        # calculate ax max 
        FZ_F = (1-self.CoG_X) * self.m * self.g
        FZ_R = self.CoG_X * self.m * self.g
        
        FX_F = self.mu * FZ_F
        FX_R = self.mu * FZ_R

        if self.DriveType == '2WD':
            FX_ovr = FX_R 
        elif self.DriveType == '4WD':
            FX_ovr = FX_F + FX_R    
        
        
        ax_max = FX_ovr / self.m
        #ax_max = 7
        return ax_max
    
            
    def Plot_gg(self, ay_max, ax_max):    
        
        # Calculate values
        resolution = 1000
        
        ay = np.linspace((-1)*ay_max, ay_max, resolution)
        ax_upper =((1-(ay**2 / ay_max**2)) * ax_max**2)**0.5
        
        if self.DriveType == '2WD':
            ax_lower = (-2) * ax_upper
        if self.DriveType == '4WD':
            ax_lower = (-1) * ax_upper
               
        ay = ay /self.g
        ax_U_inG = np.asarray(ax_upper)/self.g
        ax_L_inG = np.asarray(ax_lower)/self.g
        
        
#         # Plot g-g diagram
#         plt.plot(ay, ax_U_inG , 'b')
#         plt.plot(ay, ax_L_inG, 'b')
#         plt.xlabel('ay [g]' + '\n' + ('ay max: ' + str(np.round(ay_max/self.g,2)) + ' g'), fontsize = 16)
#         plt.ylabel('ax [g]' + '\n' + ('ax max: ' + str(np.round(ax_max/self.g,2)) + ' g'), fontsize = 16)
#         plt.title('g-g diagram', fontsize = 20, y=1.03)
#         plt.grid(True)
#         plt.show()


########################################################
        
class GG_ESB_TwoDim:
    def __init__(self, C_F, C_R, m, CoG_X, mu, alpha, CoP_X, C_la, rho, DriveType, gearRatio, tireRadius, fr, Lift2Drag ):
        
        self.C_F = C_F
        self.C_R = C_R
        self.m = m
        self.CoG_X = CoG_X
        self.mu = mu
        self.alpha = alpha
        self.CoP_X = CoP_X # = 0.61
        self.C_la = C_la # = 3.52 m^2
        self.rho = rho
        
        self.DriveType = DriveType #2WD or 4WD
        
        self.gearRatio = gearRatio
        self.tireRadius = tireRadius
        self.fr = fr
        self.Lift2Drag = Lift2Drag
        
        # General constants
        self.deg2rad = np.pi/180
        self.g = 9.81
    
    def GGV_Map(self):
        
        ax_upper_values = []
        ax_lower_values = []
        ay_values = []
        speed_values =[]
        
        Speed_resolution = 200
        ay_resolution = 500
        # initialize speed
        VehicleSpeed = np.linspace(0.001, 50, Speed_resolution)  #Speed in m/s
        
        #loop through different velocities
        for i in range(len(VehicleSpeed)):
            #find maximum lateral acceleration
            ay_max = self.GG_ESB_ay_Max()
            ay = np.linspace((-1)*ay_max, ay_max, ay_resolution)
            
            ax_max_upper = self.GG_ESB_ax_Max_upper(VehicleSpeed[i])
            ax_up = []
            for j in range(len(ay)):
                ax_up.append(((1-(ay[j]**2 / ay_max**2)) * ax_max_upper**2)**0.5)
            
            ax_max_lower = self.GG_ESB_ax_Max_lower(VehicleSpeed[i]) 
            ax_low = []
            for j in range(len(ay)):
                ax_low.append(-1*((1-(ay[j]**2 / ay_max**2)) * ax_max_lower**2)**0.5)
            
            speed = []
            for j in range(len(ay)):
                speed.append(VehicleSpeed[i])
                
            ax_upper_values.append(ax_up)
            ax_lower_values.append(ax_low)
            ay_values.append(ay)
            speed_values.append(speed)

        
        # Load Motor map
        motor = TwoDimLookup_motor(self.gearRatio, self.tireRadius, self.CoG_X, self.m, self.CoP_X, self.C_la, self.rho, self.fr, self.Lift2Drag, self.DriveType)
        ax_motor = motor.ax_motor(speed_values)
        
        # Replace ax values which are higher than ax_motor 
        for i in range(len(ax_upper_values)):
            for j in range(len (ax_upper_values[i])):
                if ax_upper_values[i][j] >  ax_motor[i]:
                    ax_upper_values[i][j] =  ax_motor[i]   
                       
        return ax_upper_values, ax_lower_values, ay_values, speed_values
           
    def GG_ESB_ay_Max(self):

        # calculate ay max 
        
        FY_F = self.alpha * self.deg2rad * self.C_F
        FY_R = self.alpha * self.deg2rad * self.C_R         

        FY_ovr = FY_F + FY_R        
        
        ay_max = FY_ovr / self.m
        return ay_max


    def GG_ESB_ax_Max_upper(self, VehicleSpeed):

        # calculate ax max 
         
        # Mass
        FZ_m_F = (1-self.CoG_X) * self.m * self.g
        FZ_m_R = self.CoG_X * self.m * self.g
        
        #Downforce
        FZ_d_F = (1-self.CoP_X) * self.C_la * 0.5*self.rho * VehicleSpeed**2
        FZ_d_R = (self.CoP_X) * self.C_la * 0.5*self.rho * VehicleSpeed**2       
        
        # FZ ovr 
        FZ_ovr_F = FZ_m_F + FZ_d_F 
        FZ_ovr_R = FZ_m_R + FZ_d_R
        
        #FX
        FX_F = self.mu * FZ_ovr_F
        FX_R = self.mu * FZ_ovr_R


        if self.DriveType == '2WD':
            FX_ovr = FX_R 
        elif self.DriveType == '4WD':
            FX_ovr = FX_F + FX_R  
        
        ax_max_upper = FX_ovr / self.m
        return ax_max_upper
  
    
    def GG_ESB_ax_Max_lower(self, VehicleSpeed):

        # calculate ax max 
         
        # Mass
        FZ_m_F = (1-self.CoG_X) * self.m * self.g
        FZ_m_R = self.CoG_X * self.m * self.g
        
        #Downforce
        FZ_d_F = (1-self.CoP_X) * self.C_la * 0.5*self.rho * VehicleSpeed**2
        FZ_d_R = (self.CoP_X) * self.C_la * 0.5*self.rho * VehicleSpeed**2       
        
        # FZ ovr
        FZ_ovr_F = FZ_m_F + FZ_d_F 
        FZ_ovr_R = FZ_m_R + FZ_d_R
        
        #FX
        FX_F = self.mu * FZ_ovr_F
        FX_R = self.mu * FZ_ovr_R

        #FX ovr
        FX_ovr = FX_F + FX_R
        
        ax_max_lower = FX_ovr / self.m
        return ax_max_lower
            
    def Plot_ggV(self, ax_upper_values, ax_lower_values, ay_values, speed_values ):    
        
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        surf_upper = ax.plot_surface(ay_values, speed_values, ax_upper_values, color = 'r')
        surf_lower = ax.plot_surface(ay_values, speed_values, ax_lower_values)
        ax.set_xlabel('ay [m/s^2]')
        ax.set_ylabel('speed [m/s]')
        ax.set_zlabel('ax [m/s^2]')
        plt.show()
        
    def Plot_Long_Speed_Distance(self):
        
        # Calculate motor 
        VehicleSpeed = np.array([np.linspace(0.0001, 60, 200), np.zeros(200)])
        VehicleSpeed = np.transpose(VehicleSpeed).tolist()
        
        Motor = TwoDimLookup_motor(self.gearRatio, self.tireRadius, self.CoG_X, self.m, self.CoP_X, self.C_la, self.rho, self.fr, self.Lift2Drag, self.DriveType)
        ax_Motor = Motor.ax_motor(VehicleSpeed)
        
        speed = np.linspace(0.0001, 60, 200)
        a = interpolate.interp1d(speed, ax_Motor, bounds_error=False, fill_value=0)

        #Calculate speed and distance
        v = [0.0001]
        s = [0]
        t = [0]
        delta_t = 0.005 # sec 
        t_end = 6

        while t[-1] <= t_end:
            a_v = a(v[-1])
            v_t = a_v * delta_t + v[-1]
            s_t = 0.5 * a_v * delta_t**2 + v[-1] * delta_t + s[-1]
            
            v.append(v_t)
            s.append(s_t)
            t.append(t[-1] + delta_t)
        
        
        # Find important vehicle parameters
        # From 1 to 100 kph
        index1 = np.nonzero(np.asarray(v) <= 100/3.6)
        index_0to100 = np.max(index1)
        
        # Time for 75 m acceleration
        index2 = np.nonzero(np.asarray(s) <= 75)
        #print(index2)
        index_75m = np.max(index2)
        
        
        # Graphs
 
#         f, axarr = plt.subplots(2, sharex=True)
#         axarr[0].plot(t, v,'b', label = 'Vehicle speed', linewidth = 1.5)
#         axarr[0].plot(t[index_0to100], v[index_0to100], marker = '+', markersize = 15, markeredgewidth  = 2.5, markerfacecolor = 'r', markeredgecolor = 'r', linestyle = 'None', label = 'Time from 0 to 100 kph: ' + str(np.round(t[index_0to100],2)) +  ' s')
#         axarr[0].set_title('Vehicle Speed vs. Time')
#         axarr[0].set_xlabel('Time [s]')
#         axarr[0].set_ylabel('Vehicle speed [m/s]')
#         axarr[0].grid(True)
#         axarr[0].legend(numpoints=1, shadow=True, fancybox=True)
#           
#         axarr[1].plot(t, s, 'g', label = 'Driven Distance', linewidth = 1.5)
#         axarr[1].plot(t[index_75m], s[index_75m], marker = '+', markersize = 15, markeredgewidth  = 2.5, markerfacecolor = 'r', markeredgecolor = 'r', linestyle = 'None', label = 'Time for 75 meters acceleration: ' + str(np.round(t[index_75m],2)) +  ' s')
#         axarr[1].set_title('Driven Distance vs. Time')
#         axarr[1].set_xlabel('Time [s]')
#         axarr[1].set_ylabel('Driven Distance [m]')
#         axarr[1].grid(True)
#         axarr[1].legend(numpoints=1, shadow=True, fancybox=True)
#           
#         plt.show()
        
