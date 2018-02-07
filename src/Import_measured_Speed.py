import numpy as np
from scipy.interpolate import interp1d
import csv
from itertools import islice
import matplotlib.pyplot as plt
import os
import platform

class ImportSpeed:
        
    def ImportSpeed(self, displacementIndex):     

        # FileName = 'AutoX_TimFritz_FSA2015_GPS_speed.csv'
        # FileName = 'Endurance_FSG2015_GPS_speed.csv'
        FileName = 'Endurance_FSA2015_GPS_speed.csv'
        
        cwd = os.getcwd()
        if('Windows' in platform.platform()):
            FilePath = cwd + '\CSV\\'
        elif('Mac' in platform.platform()):
            cwd = cwd.replace('\\', '/')
            FilePath = cwd + '/CSV/'
        elif('Linux' in platform.platform()):
            cwd = cwd.replace('\\', '/')
            FilePath = cwd + '/CSV/'
        
        file = FilePath+FileName
#         FilePath = 'C:/Users/AnneTTe/Desktop/LapSimulation/src/CSV/'    #; path with "/" not backslash!
#         file = FilePath+FileName
         
         
        RealTime, RealSpeed, Distance = [], [], []
  
        data = csv.reader(open(file,'r'))     # open and read CSV file
 
        for row in islice(data,17, None):     # Put data into list; start with row 18 (because of header)
            try:
                RealTime.append(row[0])
                Distance.append(row[1])
                RealSpeed.append(row[2])
            except IndexError:
                pass
  
        for i in range(len(RealSpeed)):                                 # e.g. "1,12" string into 1.12 float
            RealSpeed[i] = RealSpeed[i].replace(",",".")
            try:
                RealSpeed[i] = float(RealSpeed[i])
                RealSpeed[i] = RealSpeed[i]/3.6
            except ValueError:
                RealSpeed[i] = 0 
        RealSpeed = RealSpeed[displacementIndex:]
       

        for i in range(len(Distance)):                                 # e.g. "1,12" string into 1.12 float
            Distance[i] = Distance[i].replace(",",".")
            try:
                Distance[i] = float(Distance[i])
                Distance[i] = Distance[i]
            except ValueError:
                Distance[i] = 0 
        
        Distance = Distance[displacementIndex:]
        min_Distance = Distance[0]
        for i in range(len(Distance)):
            Distance[i] = Distance[i] - min_Distance
        
        for i in range(len(RealTime)):                                 # e.g. "1,12" string into 1.12 float
            RealTime[i] = RealTime[i].replace(",",".")
            try:
                RealTime[i] = float(RealTime[i])
                RealTime[i] = RealTime[i]
            except ValueError:
                RealTime[i] = 0 
                
        RealTime = RealTime[displacementIndex:]
        min_RealTime = RealTime[0]
        for i in range(len(RealTime)):
            RealTime[i] = RealTime[i] - min_RealTime
        
        RealSpeed = interp1d(Distance, RealSpeed)
        RealTime = interp1d(Distance, RealTime) 
        
        return RealSpeed, RealTime