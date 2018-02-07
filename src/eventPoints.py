from LSvehicleOneDimLookup_2 import vehicleOneDimLookup_2 as vehicle_ODL_2
from LSvehicleTwoDimLookup_2 import vehicleTwoDimLookup_2 as vehicle_TDL_2
from Create_TrackMap_2D import Create_TrackMap_2D
from _pytest.assertion.util import basestring
from track import Track
import lapsim as lts
import Acceleration
import numpy as np
import platform
import math
import os

      
class Event:
    def __init__(self, EventName, Year, StartValue, Counter, revision, Vehicles = [], Tracks = []):
       
        self.EventName = EventName
        self.Year = Year
        self.Counter = Counter
        self.Vehicles = Vehicles
        self.Tracks = Tracks
        self.StartValue = StartValue
        self.revision = revision
    
    def SimulateEvent(self):    
        #Initialization of module
        Score = Scoring(self.EventName, self.Year)
        
        #Check platform and open file for saving calculated data     
        cwd = os.getcwd()
        if('Windows' in platform.platform()):
            file = cwd + '\Results.txt'
        else:
            cwd = cwd.replace('\\', '/')
            file = cwd + '/Results.txt'
        
        if(self.Counter == 1): #if Counter == 1 the file gets opened and the old data will get overwritten
            f = open(file, 'w')
            f.write('Event&Year|Track|Car|Parameter|Event|Scored Time in s|Scored EnergyConsumption in kWh|Scores|\n')
        else:   #for all other values of Counter the data will get appended to the old ones
            f = open(file, 'a')

        #Points = []
        
        ds = 0.5  #length of each track segment

        #Go through Tracks
        for counterTracks in self.Tracks:
            #Go through Vehicles            
            for counterVehicles in self.Vehicles:
                #write basic information into result file
                f.write(self.EventName + ' ' + str(self.Year) + '|')
                f.write(counterTracks + '|')
                f.write(str(counterVehicles.CarName) + '|')
                f.write('%d|' %(self.StartValue))

                if('AutoX' in counterTracks):
                    cwd = os.getcwd()   #open file with
                    if ('Windows' in platform.platform()):
                        file = cwd + '\\CSV\\' 
                        #VehicleParameters.xlsx'
                    else:
                        cwd = cwd.replace('\\', '/')
                        file = cwd + '/CSV/'
                    cfile = open(file + counterTracks + '.csv', 'r')
                    
                    curvature = []
                    #Load Curvature from file into list and make it to an array
                    for row in cfile:
                        new = np.array(row.split(','))
                        value1 = float(new[0])
                        curvature.append(value1)
                    curvature = np.array(curvature)
                    
                    track = Track(curvature, ds)
                    # Initialize Lap Simulation
                    LS = lts.LapSim(counterVehicles, track)
                    LS.max_laps = 2
                    # Run Lap Simulation
                    LS.speed_profile()
                elif('Endurance' in counterTracks):
                    cwd = os.getcwd()
                    if ('Windows' in platform.platform()):
                        file = cwd + '\\CSV\\' 
                        # VehicleParameters.xlsx
                    else:
                        cwd = cwd.replace('\\', '/')
                        file = cwd + '/CSV/'
                    cfile = open(file + counterTracks + '.csv', 'r')
                    
                    curvature = []
                    #Load Curvature from file into list and make it to an array
                    for row in cfile:
                        new = np.array(row.split(','))
                        value1 = float(new[0])
                        curvature.append(value1)
                    curvature = np.array(curvature)
                    
                    track = Track(curvature, ds)
                    # Initialize Lap Simulation
                    LS = lts.LapSim(counterVehicles, track)
                    LS.max_laps = 2
                    # Run Lap Simulation
                    LS.speed_profile()
                elif('Efficiency' in counterTracks):
                    cwd = os.getcwd()
                    if ('Windows' in platform.platform()):
                        file = cwd + '\\CSV\\' #VehicleParameters.xlsx'
                    else:
                        cwd = cwd.replace('\\', '/')
                        file = cwd + '/CSV/'
                    cfile = open(file + counterTracks + '.csv', 'r')
                    
                    curvature = []
                    #Load Curvature from file into List and make it to an Array
                    for row in cfile:
                        new = np.array(row.split(','))
                        value1 = float(new[0])
                        curvature.append(value1)
                    curvature = np.array(curvature)
                    
                    track = Track(curvature, ds)
                    # Initialize Lap Simulation
                    LS = lts.LapSim(counterVehicles, track)
                    LS.max_laps = 2
                    # Run Lap Simulation
                    LS.speed_profile()
                elif('Skidpad' in counterTracks):
                    curvature = []
                    FzgWidth = 1.3   #Average of all 4 in 2015 and 2016 (look datasheet GDrive) in m
                    Radius = FzgWidth/2+15.25/2
                    SkidpadCurvature = 1/Radius  #k=1/R
                    i = 1
                    range = 2*math.pi*Radius
                    while i <= round(range/ds):
                        curvature.append(SkidpadCurvature)
                        i += 1
                    curvature = np.array(curvature)
                    
                    track = Track(curvature, ds)
                    # Initialize Lap Simulation
                    LS = lts.LapSim(counterVehicles, track)
                    LS.max_laps = 2
                    # Run Lap Simulation
                    LS.speed_profile()

                #Calculate Event Points
                if('Skidpad' in counterTracks):
                    Tyour = LS.lapTime
                    Tmin = 4.920
                    if(Tmin > Tyour):   #set Tyour as Tmin if it is faster than fix Tmin
                        Tmin = Tyour
                    SkidpadScoring = Score.Calc_Skidpad(Tmin, Tyour)
                    if(isinstance(SkidpadScoring, basestring) == True): #if points are a string set points on 0
                        SkidpadScoring = 0
                        #Points.append('Skidpad: %s s, Score: %d' %(Tyour, SkidpadScoring))
                        f.write('Skidpad|%f|-|%d|\n' %(Tyour, SkidpadScoring))
                    elif(isinstance(SkidpadScoring, basestring) == False):  #if points are not a string, go on
                        #Points.append('Skidpad: %s s, Score: %d' %(Tyour, SkidpadScoring))
                        f.write('Skidpad|%f|-|%d|\n' %(Tyour, SkidpadScoring))
                    print('Skidpad ' + str(self.Counter) + ' of ' + str(self.revision) + ' completed.')
                elif('Accel' in counterTracks):
                    Accel = Acceleration.Acceleration(counterVehicles)  #initialize class for accel calculation
                    Tyour = Accel.AccelTime()          
                    #Tyour = LS.lapTime
                    Tmin = 3.109
                    if(Tmin > Tyour):   #set Tyour as Tmin if it is faster than fix Tmin
                        Tmin = Tyour
                    AccelScoring = Score.Calc_Acceleration(Tmin, Tyour)
                    if(isinstance(AccelScoring, basestring) == True):   #if points are a string set points on 0
                        AccelScoring = 0
                        #Points.append('Acceleration: %s s, Score: %d' %(Tyour, AccelScoring))
                        f.write('Acceleration|%f|-|%d|\n' %(Tyour, AccelScoring))
                    elif(isinstance(AccelScoring, basestring) == False):    #if points are not a string, go on
                        #Points.append('Acceleration: %s s, Score: %d' %(Tyour, AccelScoring))
                        f.write('Acceleration|%f|-|%d|\n' %(Tyour, AccelScoring))
                    print('Acceleration ' + str(self.Counter) + ' of ' + str(self.revision) + ' completed.')
                elif('AutoX' in counterTracks):
                    Tyour = LS.lapTime
                    Tmin = 56.083
                    if(Tmin > Tyour):
                        Tmin = Tyour
                    AutoXScoring = Score.Calc_AutoX(Tmin, Tyour)
                    if(isinstance(AutoXScoring, basestring) == True):   #if points are a string set points on 0
                        AutoXScoring = 0
                        #Points.append('AutoX: %s s, Score: %d' %(Tyour, AutoXScoring))
                        f.write('AutoX|%f|-|%d|\n' %(Tyour/60, AutoXScoring))
                    elif(isinstance(AutoXScoring, basestring) == False):    #if points are not a string, go on
                        #Points.append('AutoX: %s s, Score: %d' %(Tyour, AutoXScoring))
                        f.write('AutoX|%f|-|%d|\n' %(Tyour/60, AutoXScoring))
                    print('AutoX ' + str(self.Counter) + ' of ' + str(self.revision) + ' completed.')
                elif('Endurance' in counterTracks):                  
                    if(self.EventName == 'FSG'):    #calculate Tyour depending on the event
                        Tyour = LS.lapTime*18
                    elif(self.EventName == 'FSA'):
                        if(self.Year == 2016):
                            Tyour = LS.lapTime*20
                        elif(self.Year == 2015):
                            Tyour = LS.lapTime*22
                    elif(self.EventName == 'FSAE'):
                        if(self.Year == 2016):
                            Tyour = LS.lapTime*20
                        elif(self.Year == 2015):
                            Tyour = LS.lapTime*22
                    Tmin = 1363.556
                    if(Tmin > Tyour):   #set Tyour as Tmin if it is faster than fix Tmin
                        Tmin = Tyour
                    EnduranceScoring = Score.Calc_Endurance(Tmin, Tyour)
                    if(isinstance(EnduranceScoring, basestring) == True):   #if points are a string set points on 0
                        EnduranceScoring = 0
                        #Points.append('Endurance: %s s, Score: %d' %(Tyour, EnduranceScoring))
                        f.write('Endurance|%f|-|%d|\n' %(Tyour/60, EnduranceScoring))
                    elif(isinstance(EnduranceScoring, basestring) == False):    #if points are not a string, go on
                        #Points.append('Endurance: %s s, Score: %d' %(Tyour, EnduranceScoring))
                        f.write('Endurance|%f|-|%d|\n' %(Tyour/60, EnduranceScoring))
                    print('Endurance ' + str(self.Counter) + ' of ' + str(self.revision) + ' completed.')    
                elif('Efficiency' in counterTracks):
                    if(self.EventName == 'FSG'):    #calculate Tyour depending on the event
                        Tyour = LS.lapTime*18
                        EyourTotal = LS.UsedEnergy/1000/3600*18
                    elif(self.EventName == 'FSA'):
                        if(self.Year == 2016):
                            Tyour = LS.lapTime*20
                            EyourTotal = LS.UsedEnergy/1000/3600*20
                        elif(self.Year == 2015):
                            Tyour = LS.lapTime*22
                            EyourTotal = LS.UsedEnergy/1000/3600*22
                    elif(self.EventName == 'FSAE'):
                        if(self.Year == 2016):
                            Tyour = LS.lapTime*20
                            EyourTotal = LS.UsedEnergy/1000/3600*20
                        elif(self.Year == 2015):
                            Tyour = LS.lapTime*22
                            EyourTotal = LS.UsedEnergy/1000/3600*22
                    Tmin = 1363.556
                    if(Tmin > Tyour):   #set Tyour as Tmin if it is faster than fix Tmin
                        Tmin = Tyour
                    Emin = 0.242
                    Eff_fac_min = 0.1
                    Eff_fac_max = 0.89
                    
                    #Energy consumption per lap
                    Eyour = LS.UsedEnergy/1000/3600 #divide with 1000 and 3600 for unity [kWh]
                    if(Emin > Eyour):   #set Eyour as Emin if it is smaller than fix Emin
                        Emin = Eyour
                    
                    #Eyour = 0.378   # per lap
                    EfficiencyScoring = Score.Calc_Efficiency(Tmin, Emin, Eff_fac_min, Eff_fac_max, Tyour, Eyour)
                    if(isinstance(EfficiencyScoring, basestring) == True):  #if points are a string set points on 0
                        EfficiencyScoring = 0
                        #Points.append('Efficiency: %s s, Energy: %f kWh, Score: %d' %(Tyour, EyourTotal, EfficiencyScoring))
                        f.write('Efficiency|%f|%f|%d|\n' %(Tyour/60, EyourTotal, EfficiencyScoring))
                    elif(isinstance(EfficiencyScoring, basestring) == False):   #if points are not a string, go on
                        #Points.append('Efficiency: %s s, Energy: %f kWh, Score: %d' %(Tyour, EyourTotal, EfficiencyScoring))
                        f.write('Efficiency|%f|%f|%d|\n' %(Tyour/60, EyourTotal, EfficiencyScoring))
                    print('Efficiency ' + str(self.Counter) + ' of ' + str(self.revision) + ' completed.')
        
        # #should delete console, but it's not working because Python IDLE don't support console cleaning
        # if (os.name == 'nt'):
        #     os.system('cls')
        # else:
        #     os.system('clear')

        #Calculate all points of each event
        Overall = SkidpadScoring + AccelScoring + EnduranceScoring + AutoXScoring + EfficiencyScoring
        #Points.append('Overall Score: %d' %(Overall))
        f.write('Overall Points|-|-|%d|-|-|-|%d|\n' %(self.StartValue, Overall))
        #print(Points)
        
        
class Scoring:
    def __init__(self, EventName, Year):  
        
        self.EventName = EventName
        self.Year = Year
        
        #Determine constants for each event and year
        if (self.EventName == 'FSG' or 'FSS'): #Points for Germany and Spain
            if (self.Year == 2015):
                self.SkidpadMax = 71.5
                self.SkidpadMin = 3.5
                self.AccelMax = 71.5
                self.AccelMin = 3.5
                self.AutoXMax = 95.5
                self.AutoXMin = 4.5
                self.EnduranceMax = 300
                self.EnduranceMin = 25
                self.EfficiencyMax = 100  
                             
            elif (self.Year == 2016):
                self.SkidpadMax = 71.5
                self.SkidpadMin = 3.5
                self.AccelMax = 71.5
                self.AccelMin = 3.5
                self.AutoXMax = 95.5
                self.AutoXMin = 4.5
                self.EnduranceMax = 300
                self.EnduranceMin = 25
                self.EfficiencyMax = 100
   
            elif (self.Year == 2017):            
                self.SkidpadMax = 71.5
                self.SkidpadMin = 3.5
                self.AccelMax = 71.5
                self.AccelMin = 3.5
                self.AutoXMax = 95.5
                self.AutoXMin = 4.5;
                self.EnduranceMax = 300
                self.EnduranceMin = 25
                self.EfficiencyMax = 100

            else:                
                self.SkidpadMax = 71.5
                self.SkidpadMin = 3.5
                self.AccelMax = 75
                self.AutoXMax = 95.5
                self.AutoXMin = 4.5
                self.EnduranceMax = 300
                self.EnduranceMin = 25
                self.EfficiencyMax = 100

    
        elif (self.EventName == 'FSA'): #Points for Austria
            if (self.Year == 2015):
                self.SkidpadMax = 71.5
                self.SkidpadMin = 3.5
                self.AccelMax = 71.5
                self.AccelMin = 3.5
                self.AutoXMax = 95.5
                self.AutoXMin = 4.5
                self.EnduranceMax = 300
                self.EnduranceMin = 25
                self.EfficiencyMax = 100
               
            elif (self.Year == 2016):
                self.SkidpadMax = 71.5
                self.SkidpadMin = 3.5
                self.AccelMax = 75
                self.AutoXMax = 95.5
                self.AutoXMin = 4.5
                self.EnduranceMax = 300
                self.EnduranceMin = 25
                self.EfficiencyMax = 100
 
            elif (self.Year == 2017):            
                self.SkidpadMax = 71.5
                self.SkidpadMin = 3.5
                self.AccelMax = 71.5
                self.AccelMin = 3.5
                self.AutoXMax = 95.5
                self.AutoXMin = 4.5
                self.EnduranceMax = 300
                self.EnduranceMin = 25
                self.EfficiencyMax = 100
                
            else:
                self.SkidpadMax = 71.5
                self.SkidpadMin = 3.5
                self.AccelMax = 75
                self.AutoXMax = 95.5
                self.AutoXMin = 4.5
                self.EnduranceMax = 300
                self.EnduranceMin = 25
                self.EfficiencyMax = 100

                
        elif (self.EventName == 'FSAE' or 'FSI'): #Points for America and Italy
            if (self.Year == 2015):
                self.SkidpadMax = 47.5
                self.SkidpadMin = 2.5
                self.AccelMax = 71.5
                self.AccelMin = 3.5
                self.AutoXMax = 142.5
                self.AutoXMin = 7.5
                self.EnduranceMax = 250   #Tyour <= Tmax --> Formel, Tyour > Tmax --> 0
                self.EnduranceMin = 50
                self.EfficiencyMax = 100
                  
            elif (self.Year == 2016):
                self.SkidpadMax = 47.5
                self.SkidpadMin = 2.5
                self.AccelMax = 71.5
                self.AccelMin = 3.5
                self.AutoXMax = 142.5
                self.AutoXMin = 7.5
                self.EnduranceMax = 250   #Tyour <= Tmax --> Formel, Tyour > Tmax --> 0
                self.EnduranceMin = 50
                self.EfficiencyMax = 100
  
            elif (self.Year == 2017):            
                self.SkidpadMax = 71.5
                self.SkidpadMin = 3.5
                self.AccelMax = 95.5
                self.AccelMin = 4.5
                self.AutoXMax = 118.5
                self.AutoXMin = 6.5
                self.EnduranceMax = 200   #Tyour <= Tmax --> Formel, Tyour > Tmax --> 25
                self.EnduranceMin = 25
                self.EfficiencyMax = 100
                
            else:
                self.SkidpadMax = 47.5
                self.SkidpadMin = 2.5
                self.AccelMax = 71.5
                self.AccelMin = 3.5
                self.AutoXMax = 142.5
                self.AutoXMin = 7.5
                self.EnduranceMax = 250   #Tyour <= Tmax --> Formel, Tyour > Tmax --> 0
                self.EnduranceMin = 50
                self.EfficiencyMax = 100
                
    #Calculation for Acceleration
    def Calc_Acceleration(self, Tmin, Tyour):    
        #Check Event and Year
        if((self.EventName == 'FSG' or 'FSA' or 'FSS') and (self.Year == 2017)):
            Tmax = 1.5 * Tmin
            #Calculate Points
            if(Tyour < Tmax):
                AccelPoints = np.around(self.AccelMax*(((Tmax/Tyour)-1)/0.5)+self.AccelMin, 3)
                if(AccelPoints > 75):
                    AccelPoints = 'Error - Value to high'
                else:
                    AccelPoints = AccelPoints
            else:
                AccelPoints = self.AccelMin
            return AccelPoints
        elif((self.EventName == 'FSG' or 'FSA' or 'FSS') and (self.Year == 2015 or 2016)):  
            Tmax = 1.5 * Tmin
            if(Tyour < Tmax):
                AccelPoints = np.around(self.AccelMax*((Tmax/Tyour)-1)/((Tmax/Tmin)-1)+self.AccelMin, 3)
                if(AccelPoints > 75):
                    AccelPoints = 'Error - Value to high'
                else:
                    AccelPoints = AccelPoints
            else:
                AccelPoints = self.AccelMin
            return AccelPoints
        elif((self.EventName == 'FSAE' or 'FSI') and (self.Year == 2017)):
            Tmax = 1.5 * Tmin
            if(Tyour < Tmax):
                AccelPoints = np.around(self.AccelMax*((Tmax/Tyour)-1)/((Tmax/Tmin)-1)+self.AccelMin, 3)
                if(AccelPoints > 100):
                    AccelPoints = 'Error - Value to high'
                else:    
                    AccelPoints = AccelPoints
            else:
                AccelPoints = self.AccelMin
            return AccelPoints
        elif((self.EventName == 'FSAE' or 'FSI') and (self.Year == 2015 or 2016)):
            Tmax = 1.5 * Tmin
            if(Tyour < Tmax):
                AccelPoints = np.around(self.AccelMax*((Tmax/Tyour)-1)/((Tmax/Tmin)-1)+self.AccelMin, 3)
                if(AccelPoints > 75):
                    AccelPoints = 'Error - Value to high'
                else:
                    AccelPoints = AccelPoints
            else:
                AccelPoints = self.AccelMin
            return AccelPoints

    #Calculation for Skidpad
    def Calc_Skidpad(self, Tmin, Tyour):
        #Check Event and Year
        if((self.EventName == 'FSG' or 'FSA' or 'FSS') and (self.Year == 2017)):
            Tmax = 1.25 * Tmin
            if(Tyour < Tmax):
                SkidpadPoints = np.around(self.SkdipadMax*((np.square(Tmax/Tyour)-1)/0.5625)+self.SkidpadMin, 3)
                if(SkidPoints > 75):
                    SkidpadPoints = 'Error - Value to high'
                else:
                    SkidpadPoints = SkidpadPoints
            else:
                SkidpadPoints = self.SkidpadMin
            return SkidpadPoints
        elif((self.EventName == 'FSG' or 'FSA' or 'FSS') and (self.Year == 2015 or 2016)):
            Tmax = 1.25 * Tmin
            if(Tyour < Tmax):
                SkidpadPoints = np.around(self.SkidpadMax*((np.square(Tmax/Tyour)-1)/(np.square(Tmax/Tmin)-1))+self.SkidpadMin, 3)
                if(SkidpadPoints > 75):
                    SkidpadPoints = 'Error - Value to high'
                else:
                    SkidpadPoints = SkidpadPoints
            else:
                SkidpadPoints = self.SkidpadMin
            return SkidpadPoints
        elif((self.EventName == 'FSAE' or 'FSI') and (self.Year == 2017)):
            Tmax = 1.25 * Tmin
            if(Tyour < Tmax):
                SkidpadPoints = np.around(self.SkidpadMax*((np.square(Tmax/Tyour)-1)/(np.square(Tmax/Tmin)-1))+self.SkidpadMin, 3)
                if(SkidpadPoints > 75):
                    SkidpadPoints = 'Error - Value to high'
                else:
                    SkidpadPoints = SkidpadPoints
            else:
                SkidpadPoints = self.SkidpadMin
            return SkidpadPoints
        elif((self.EventName == 'FSAE' or 'FSI') and (self.Year == 2015 or 2016)):
            Tmax = 1.25 * Tmin
            if(Tyour < Tmax):
                SkidpadPoints = np.around(self.SkidpadMax*((np.square(Tmax/Tyour)-1)/(np.square(Tmax/Tmin)-1))+self.SkidpadMin, 3)
                if(SkidpadPoints > 50):
                    SkidpadPoints = 'Error - Value to high'
                else:
                    SkidpadPoints = SkidpadPoints
            else:
                SkidpadPoints = self.SkidpadMin
            return SkidpadPoints
        
    #Calculation for Autocross 
    def Calc_AutoX(self, Tmin, Tyour):
        #Check Event and Year
        if((self.EventName == 'FSG' or 'FSA' or 'FSS') and (self.Year == 2017)):
            Tmax = 1.25 * Tmin
            if(Tyour < Tmax):
                AutoXPoints = np.around((self.AutoXMax*((Tmax/Tyour)-1)/0.25)+self.AutoXMin, 3)
                if(AutoXPoints > 100):
                    AutoXPoints = 'Error - Value to high'
                else:
                    AutoXPoints = AutoXPoints
            else:
                AutoXPoints = self.AutoXMin
            return AutoXPoints
        elif((self.EventName == 'FSG' or 'FSA' or 'FSS') and (self.Year == 2015 or 2016)):
            Tmax = 1.25 * Tmin
            if(Tyour < Tmax):
                AutoXPoints = np.around((self.AutoXMax*((Tmax/Tyour)-1)/((Tmax/Tmin)-1)+self.AutoXMin), 3)
                if(AutoXPoints > 100):
                    AutoXPoints = 'Error - Value to high'
                else:
                    AutoXPoints = AutoXPoints
            else:
                AutoXPoints = self.AutoXMin  
            return AutoXPoints
        elif((self.EventName == 'FSAE' or 'FSI') and (self.Year == 2017)):
            Tmax = 1.45 * Tmin
            if(Tyour < Tmax):
                AutoXPoints = np.around((self.AutoXMax*((Tmax/Tyour)-1)/((Tmax/Tmin)-1)+self.AutoXMin), 3)
                if(AutoXPoints > 125):
                    AutoXPoints = 'Error - Value to high'
                else:
                    AutoXPoints = AutoXPoints
            else:
                AutoXPoints = self.AutoXMin
            return AutoXPoints
        elif((self.EventName == 'FSAE' or 'FSI') and (self.Year == 2015 or 2016)):
            Tmax = 1.45 * Tmin
            if(Tyour < Tmax):
                AutoXPoints = np.around((self.AutoXMax*((Tmax/Tyour)-1)/((Tmax/Tmin)-1)+self.AutoXMin), 3)
                if(AutoXPoints > 150):
                    AutoXPoints = 'Error - Value to high'
                else:
                    AutoXPoints = AutoXPoints
            else:
                AutoXPoints = self.AutoXMin
            return AutoXPoints
        
    #Calculation for Endurance
    def Calc_Endurance(self, Tmin, Tyour):
        #Check Event and Year
        if((self.EventName == 'FSG' or 'FSA' or 'FSS') and (self.Year == 2017)):
            Tmax= 4/3 * Tmin
            if(Tyour < Tmax):
                EndurancePoints = np.around((self.EnduranceMax*((Tmax/Tyour)-1)/0.333)+self.EnduranceMin, 3)
                if(EndurancePoints > 325):
                    EndurancePoints = 'Error - Value to high'
                else:
                    EndurancePoints = EndurancePoints
            else:
                EndurancePoints = self.EnduranceMin
            return EndurancePoints
        elif((self.EventName == 'FSG' or 'FSA' or 'FSS') and (self.Year == 2015 or 2016)):
            Tmax = 4/3 * Tmin
            if(Tyour < Tmax):
                EndurancePoints = np.around((self.EnduranceMax*((Tmax/Tyour)-1)/((Tmax/Tmin)-1) + self.EnduranceMin), 3)
                if(EndurancePoints > 325):
                    EndurancePoints = 'Error - Value to high'
                else:
                    EndurancePoints = EndurancePoints
            else:
                EndurancePoints = self.EnduranceMin
            return EndurancePoints   
        elif((self.EventName == 'FSAE' or 'FSI') and (self.Year == 2017)):
            Tmax = 1.45 * Tmin
            if(Tyour <= Tmax):
                EndurancePoints = np.around((self.EnduranceMax*((Tmax/Tyour)-1)/((Tmax/Tmin)-1) + self.EnduranceMin), 3)
                if(EndurancePoints > 225):
                    EndurancePoints = 'Error - Value to high'
                else:
                    EndurancePoints = EndurancePoints
            else:
                EndurancePoints = 25
            return EndurancePoints
        elif((self.EventName == 'FSAE' or 'FSI') and (self.Year == 2015 or 2016)):
            Tmax = 1.45 * Tmin
            if(Tyour <= Tmax):
                EndurancePoints = np.around((self.EnduranceMax*((Tmax/Tyour)-1)/((Tmax/Tmin)-1) + self.EnduranceMin), 3)
                if(EndurancePoints > 300):
                    EndurancePoints = 'Error - Value to high'
                else:
                    EndurancePoints = EndurancePoints
            else:
                EndurancePoints = 0
            return EndurancePoints
    
    #Calculation for Efficiency (right now just for electrical car)
    def Calc_Efficiency(self, Tmin, Emin, Eff_fac_min, Eff_fac_max, Tyour, Eyour):
        #Check Event and Year
        if((self.EventName == 'FSG' or 'FSA' or 'FSS') and (self.Year == 2017)):
            Tmax = 1.333*Tmin
            #Check Value of Eff_fac_min
            if(Eff_fac_min >= 0.1):
                if(Tyour <= Tmax):
                    Eff_fac_your = ((Tmin*np.square(Emin))/(Tyour*np.square(Eyour)))
                    EfficiencyPoints = np.around((self.EfficiencyMax*((Eff_fac_min/Eff_fac_your)-1)/(Eff_fac_min/Eff_fac_max)-1), 3)
                    if(EfficiencyPoints > 100):
                        EfficiencyPoints = 'Error - Value to high'
                    else:
                        EfficiencyPoints = EfficiencyPoints
                else:
                    EfficiencyPoints = 0
                return EfficiencyPoints
            else:
                print('Error - Value for minimal efficiency factor is bigger than 0.1')
        elif((self.EventName == 'FSG' or 'FSA' or 'FSS') and (self.Year == 2015 or 2016)):
            Tmax = 1.333*Tmin
            if(Eff_fac_min == 0.1):
                if(Tyour <= Tmax):
                    Eff_fac_your = (Tmin/Tyour)*np.square((Emin/Eyour))
                    EfficiencyPoints = np.around((self.EfficiencyMax*((Eff_fac_min/Eff_fac_your)-1)/((Eff_fac_min/Eff_fac_max)-1)), 3)
                    if(EfficiencyPoints > 100):
                        EfficiencyPoints = 'Error - Value to high'
                    else:
                        EfficiencyPoints = EfficiencyPoints
                else:
                    EfficiencyPoints = 0
                return EfficiencyPoints
            else:
                print('Error - Value for minimal efficiency factor is not 0.1')
                