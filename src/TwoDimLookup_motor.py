from scipy import interpolate
from itertools import islice
import numpy as np
import platform
import csv
import os

class TwoDimLookup_motor:
    
    def __init__(self, gearRatio, tireRadius, CoG_X, m, CoP_X, C_la, rho, fr, Lift2Drag, DriveType):
        
        self.gearRatio = gearRatio
        self.tireRadius = tireRadius
        self.CoG_X = CoG_X  #Center of gravity (0 at front axis, 1 at rear axis)
        self.m = m      #Weight [kg]
        self.g = 9.81   #Gravity [m/s²]
        self.CoP_X = CoP_X  #Center of pressure
        self.C_la = C_la    #Coefficient (lift coefficient*front area)
        self.rho = rho
        self.fr = fr
        self.Lift2Drag = Lift2Drag
        self.DriveType = DriveType  #2WD or 4WD

        cwd = os.getcwd()
        if('Windows' in platform.platform()):
            file = cwd + '\CSV\motor_map.csv' 
        else:
            cwd = cwd.replace('\\', '/')
            file = cwd + '/CSV/motor_map.csv'
         
        ## Import csv motor map 
        Revolutions, Torque = [], [] # define variables
  
        data = csv.reader(open(file,'r'))     # open and read CSV file
 
        for row in islice(data, 1, None):     # Put data into list; start with row 18 (because of header)
            try:
                Revolutions.append(row[0])
                Torque.append(row[1])
            except IndexError:
                pass
 
          
        for i in range(len(Revolutions)):                                 # e.g. "1,12" string into 1.12 float
            Revolutions[i] = Revolutions[i].replace(",",".")
            try:
                Revolutions[i] = float(Revolutions[i])
            except ValueError:
                Revolutions[i] = 0   
        Revolutions = np.asarray(Revolutions)
        
        for i in range(len(Torque)):                             # e.g. "1,12" string into 1.12 float
            Torque[i] = Torque[i].replace(",",".")
            try:
                Torque[i] = float(Torque[i])
            except ValueError:
                Torque[i] = 0 
        Torque = np.asarray(Torque)
                
        #Covert engine speed into vehicle speed (m/s)
        vehicle_speed = (np.pi * Revolutions)/(30 * self.gearRatio) * self.tireRadius
        # Convert Torque into longitudinal force
        x_force = (Torque * self.gearRatio)/self.tireRadius

        # Create function for F over v
        self.motorMap = interpolate.interp1d(vehicle_speed, x_force, bounds_error=False, fill_value=0)

        
    def ax_motor(self, speed_values):
        # Calculate motor force for each speed value 
        motor_force = []
        resistance_force = []
        speed = [i[0] for i in speed_values]
            
        for i in range(len(speed)):
            motor_force.append(self.motorMap(speed[i]))
            resistance_force.append(self.Driving_Resistances(speed[i]))        
        
        # 2WD
        if self.DriveType == '2WD':
            ax_motor = 2 * (np.asarray(motor_force) - np.asarray(resistance_force))/ self.m

        # 4WD 
        if self.DriveType == '4WD':
            ax_motor = 4 * (np.asarray(motor_force) - np.asarray(resistance_force))/ self.m
        
        for i in range(len(ax_motor)):
            if ax_motor[i] < 0:
                ax_motor[i] = 0
        
#         # Plots
#         a, axarr = plt.subplots(2, sharex=True)
#         axarr[0].plot(speed, resistance_force, 'g', label = 'Driving resistance')
#         axarr[0].plot(speed, motor_force, 'r', label = 'Motor force at tire')
#         axarr[0].set_title('Speed vs. Force')
#         axarr[0].set_xlabel('Speed [m/s]')
#         axarr[0].set_ylabel('Force [N]')
#         axarr[0].legend(shadow=True, fancybox=True)
#         axarr[0].grid(True)
#          
#         axarr[1].plot(speed, ax_motor, label = 'x - acceleration')
#         axarr[1].set_title('Speed vs. Acceleration')
#         axarr[1].set_xlabel('Speed [m/s]')
#         axarr[1].set_ylabel('Acceleration [m/s^2]')              
#         axarr[1].legend(shadow=True, fancybox=True)
#         axarr[1].grid(True)
#         plt.show()
        
        return ax_motor
        
    def Driving_Resistances(self, speed):
             
        # Mass
        FZ_m_F = (1-self.CoG_X) * self.m * self.g
        FZ_m_R = self.CoG_X * self.m * self.g
        
        #Downforce
        FZ_d_F = (1-self.CoP_X) * self.C_la * 0.5*self.rho * speed**2
        FZ_d_R = (self.CoP_X) * self.C_la * 0.5*self.rho * speed**2       
        
        # FZ ovr 
        FZ_ovr_F = FZ_m_F + FZ_d_F 
        FZ_ovr_R = FZ_m_R + FZ_d_R
        
        FZ_ovr = FZ_ovr_F + FZ_ovr_R
        
        # Friction of Tires
        FR_tire = self.fr * FZ_ovr
        
        #Drag
        FR_aero = self.C_la/self.Lift2Drag * 0.5*self.rho * speed**2
        
        # Sum of driving resistances
        FR_ovr = FR_tire + FR_aero
        
        return FR_ovr
        
        