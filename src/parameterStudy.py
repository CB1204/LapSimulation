from LSvehicleOneDimLookup_2 import vehicleOneDimLookup_2 as vehicle_ODL_2
from LSvehicleTwoDimLookup_2 import vehicleTwoDimLookup_2 as vehicle_TDL_2
from Create_TrackMap_2D import Create_TrackMap_2D
from dask.array.core import asarray
from eventPoints import Scoring
from eventPoints import Event
from track import Track
from Plots import Plots
import pandas as pandas
import lapsim as lts
import pylab as pl
import numpy as np
import platform
import openpyxl
import math
import os

class ParamStudy:
    def __init__(self, EventName, Year, Parameter, Stepsize, MinValue, MaxValue, StartVehicle = []):
        
        self.EventName = EventName
        self.Year = Year
        self.Parameter = Parameter
        self.Stepsize = Stepsize
        self.StartVehicle = StartVehicle
        self.MinValue = MinValue
        self.MaxValue = MaxValue
        self.StartValue = 0
        self.Counter = 1
        self.Pmax = 80000   #maximal power of the car, is variable

    def SimulateParamStudy(self):
        #Load Vehicle Parameters from file
        cwd = os.getcwd()
        if('Windows' in platform.platform()):
            file = cwd + '\CSV\VehicleParameters.xlsx'
        else:
            cwd = cwd.replace('\\', '/')
            file = cwd + '/CSV/VehicleParameters.xlsx'
            
        wb = openpyxl.load_workbook(file)
        sheet1 = wb.get_sheet_by_name('FSG15e2D')
        sheet2 = wb.get_sheet_by_name('FSG15e1D')
        
        if ('FSG15e2D' in self.StartVehicle):
            FSG15e2D = vehicle_TDL_2(sheet1['A1'].value, sheet1['A2'].value, sheet1['A3'].value, sheet1['A4'].value, sheet1['A5'].value, sheet1['A6'].value, sheet1['A7'].value, sheet1['A8'].value, sheet1['A9'].value, sheet1['A10'].value, sheet1['A11'].value, sheet1['A12'].value, sheet1['A13'].value, sheet1['A14'].value, 'FSG15e2D', self.Pmax)
            self.StartVehicle = FSG15e2D    #initialize two dim vehicle

            #check which parameter should be changed
            if(self.Parameter == 'C_F'):
                sheet1['A1'].value = self.MinValue  #get value from file and save it in variable
                self.StartValue = sheet1['A1'].value    #set StartValue on the value from the file
                xlabel = 'C_F [N/rad]'   #set x-axis of plot to variable
            elif(self.Parameter == 'C_R'):
                sheet1['A2'].value = self.MinValue
                self.StartValue = sheet1['A2'].value
                xlabel = 'C_R [N/rad]'
            elif(self.Parameter == 'm'):
                sheet1['A3'].value = self.MinValue
                self.StartValue = sheet1['A3'].value
                xlabel = 'Mass [kg]'
            elif(self.Parameter == 'CoG_X'):
                sheet1['A4'].value = self.MinValue
                self.StartValue = sheet1['A4'].value
                xlabel = 'CoG_X'
            elif(self.Parameter == 'mu'):
                sheet1['A5'].value = self.MinValue
                self.StartValue = sheet1['A5'].value
                xlabel = 'mu'
            elif(self.Parameter == 'alpha'):
                sheet1['A6'].value = self.MinValue
                self.StartValue = sheet1['A6'].value
                xlabel = 'alpha [deg]'
            elif(self.Parameter == 'CoP_X'):
                sheet1['A7'].value = self.MinValue
                self.StartValue = sheet1['A7'].value
                xlabel = 'CoP_X'
            elif(self.Parameter == 'C_la'):
                sheet1['A8'].value = self.MinValue
                self.StartValue = sheet1['A8'].value
                xlabel = 'C_la'
            elif(self.Parameter == 'rho'):
                sheet1['A9'].value = self.MinValue
                self.StartValue = sheet1['A9'].value
                xlabel = 'rho'
            elif(self.Parameter == 'DriveType'):
                sheet1['A10'].value = self.MinValue
                self.StartValue = sheet1['A10'].value
                xlabel = 'DriveType [4WD]'
            elif(self.Parameter == 'gearRatio'):
                sheet1['A11'].value = self.MinValue
                self.StartValue = sheet1['A11'].value
                xlabel = 'gearRatio'
            elif(self.Parameter == 'tireRadius'):
                sheet1['A12'].value = self.MinValue
                self.StartValue = sheet1['A12'].value
                xlabel = 'tireRadius [m]'
            elif(self.Parameter == 'fr'):
                sheet1['A13'].value = self.MinValue
                self.StartValue = sheet1['A13'].value
                xlabel = 'fr'
            elif(self.Parameter == 'Lift2Drag'):
                sheet1['A14'].value = self.MinValue
                self.StartValue = sheet1['A14'].value
                xlabel = 'Lift2Drag'
    
            while (self.StartValue <= self.MaxValue):   #loop for increase the parameter value
                if(self.Parameter == 'C_F'):
                    sheet1['A1'].value = self.StartValue    #set value in file on start value
                    #initialize vehicle with new value
                    FSG15e2D = vehicle_TDL_2(sheet1['A1'].value, sheet1['A2'].value, sheet1['A3'].value, sheet1['A4'].value, sheet1['A5'].value, sheet1['A6'].value, sheet1['A7'].value, sheet1['A8'].value, sheet1['A9'].value, sheet1['A10'].value, sheet1['A11'].value, sheet1['A12'].value, sheet1['A13'].value, sheet1['A14'].value, 'FSG15e2D', self.Pmax)
                elif(self.Parameter == 'C_R'):
                    sheet1['A2'].value = self.StartValue
                    FSG15e2D = vehicle_TDL_2(sheet1['A1'].value, sheet1['A2'].value, sheet1['A3'].value, sheet1['A4'].value, sheet1['A5'].value, sheet1['A6'].value, sheet1['A7'].value, sheet1['A8'].value, sheet1['A9'].value, sheet1['A10'].value, sheet1['A11'].value, sheet1['A12'].value, sheet1['A13'].value, sheet1['A14'].value, 'FSG15e2D', self.Pmax)
                elif(self.Parameter == 'm'):
                    sheet1['A3'].value = self.StartValue
                    FSG15e2D = vehicle_TDL_2(sheet1['A1'].value, sheet1['A2'].value, sheet1['A3'].value, sheet1['A4'].value, sheet1['A5'].value, sheet1['A6'].value, sheet1['A7'].value, sheet1['A8'].value, sheet1['A9'].value, sheet1['A10'].value, sheet1['A11'].value, sheet1['A12'].value, sheet1['A13'].value, sheet1['A14'].value, 'FSG15e2D', self.Pmax) 
                elif(self.Parameter == 'CoG_X'):
                    sheet1['A4'].value = self.StartValue
                    FSG15e2D = vehicle_TDL_2(sheet1['A1'].value, sheet1['A2'].value, sheet1['A3'].value, sheet1['A4'].value, sheet1['A5'].value, sheet1['A6'].value, sheet1['A7'].value, sheet1['A8'].value, sheet1['A9'].value, sheet1['A10'].value, sheet1['A11'].value, sheet1['A12'].value, sheet1['A13'].value, sheet1['A14'].value, 'FSG15e2D', self.Pmax)
                elif(self.Parameter == 'mu'):
                    sheet1['A5'].value = self.StartValue
                    FSG15e2D = vehicle_TDL_2(sheet1['A1'].value, sheet1['A2'].value, sheet1['A3'].value, sheet1['A4'].value, sheet1['A5'].value, sheet1['A6'].value, sheet1['A7'].value, sheet1['A8'].value, sheet1['A9'].value, sheet1['A10'].value, sheet1['A11'].value, sheet1['A12'].value, sheet1['A13'].value, sheet1['A14'].value, 'FSG15e2D', self.Pmax)
                elif(self.Parameter == 'alpha'):
                    sheet1['A6'].value = self.StartValue
                    FSG15e2D = vehicle_TDL_2(sheet1['A1'].value, sheet1['A2'].value, sheet1['A3'].value, sheet1['A4'].value, sheet1['A5'].value, sheet1['A6'].value, sheet1['A7'].value, sheet1['A8'].value, sheet1['A9'].value, sheet1['A10'].value, sheet1['A11'].value, sheet1['A12'].value, sheet1['A13'].value, sheet1['A14'].value, 'FSG15e2D', self.Pmax)
                elif(self.Parameter == 'CoP_X'):
                    sheet1['A7'].value = self.StartValue
                    FSG15e2D = vehicle_TDL_2(sheet1['A1'].value, sheet1['A2'].value, sheet1['A3'].value, sheet1['A4'].value, sheet1['A5'].value, sheet1['A6'].value, sheet1['A7'].value, sheet1['A8'].value, sheet1['A9'].value, sheet1['A10'].value, sheet1['A11'].value, sheet1['A12'].value, sheet1['A13'].value, sheet1['A14'].value, 'FSG15e2D', self.Pmax)
                elif(self.Parameter == 'C_la'):
                    sheet1['A8'].value = self.StartValue
                    FSG15e2D = vehicle_TDL_2(sheet1['A1'].value, sheet1['A2'].value, sheet1['A3'].value, sheet1['A4'].value, sheet1['A5'].value, sheet1['A6'].value, sheet1['A7'].value, sheet1['A8'].value, sheet1['A9'].value, sheet1['A10'].value, sheet1['A11'].value, sheet1['A12'].value, sheet1['A13'].value, sheet1['A14'].value, 'FSG15e2D', self.Pmax)
                elif(self.Parameter == 'rho'):
                    sheet1['A9'].value = self.StartValue
                    FSG15e2D = vehicle_TDL_2(sheet1['A1'].value, sheet1['A2'].value, sheet1['A3'].value, sheet1['A4'].value, sheet1['A5'].value, sheet1['A6'].value, sheet1['A7'].value, sheet1['A8'].value, sheet1['A9'].value, sheet1['A10'].value, sheet1['A11'].value, sheet1['A12'].value, sheet1['A13'].value, sheet1['A14'].value, 'FSG15e2D', self.Pmax)
                elif(self.Parameter == 'DriveType'):
                    sheet1['A10'].value = self.StartValue
                    FSG15e2D = vehicle_TDL_2(sheet1['A1'].value, sheet1['A2'].value, sheet1['A3'].value, sheet1['A4'].value, sheet1['A5'].value, sheet1['A6'].value, sheet1['A7'].value, sheet1['A8'].value, sheet1['A9'].value, sheet1['A10'].value, sheet1['A11'].value, sheet1['A12'].value, sheet1['A13'].value, sheet1['A14'].value, 'FSG15e2D', self.Pmax)
                elif(self.Parameter == 'gearRatio'):
                    sheet1['A11'].value = self.StartValue
                    FSG15e2D = vehicle_TDL_2(sheet1['A1'].value, sheet1['A2'].value, sheet1['A3'].value, sheet1['A4'].value, sheet1['A5'].value, sheet1['A6'].value, sheet1['A7'].value, sheet1['A8'].value, sheet1['A9'].value, sheet1['A10'].value, sheet1['A11'].value, sheet1['A12'].value, sheet1['A13'].value, sheet1['A14'].value, 'FSG15e2D', self.Pmax)
                elif(self.Parameter == 'tireRadius'):
                    sheet1['A12'].value = self.StartValue
                    FSG15e2D = vehicle_TDL_2(sheet1['A1'].value, sheet1['A2'].value, sheet1['A3'].value, sheet1['A4'].value, sheet1['A5'].value, sheet1['A6'].value, sheet1['A7'].value, sheet1['A8'].value, sheet1['A9'].value, sheet1['A10'].value, sheet1['A11'].value, sheet1['A12'].value, sheet1['A13'].value, sheet1['A14'].value, 'FSG15e2D', self.Pmax)
                elif(self.Parameter == 'fr'):
                    sheet1['A13'].value = self.StartValue
                    FSG15e2D = vehicle_TDL_2(sheet1['A1'].value, sheet1['A2'].value, sheet1['A3'].value, sheet1['A4'].value, sheet1['A5'].value, sheet1['A6'].value, sheet1['A7'].value, sheet1['A8'].value, sheet1['A9'].value, sheet1['A10'].value, sheet1['A11'].value, sheet1['A12'].value, sheet1['A13'].value, sheet1['A14'].value, 'FSG15e2D', self.Pmax)
                elif(self.Parameter == 'Lift2Drag'):
                    sheet1['A14'].value = self.StartValue
                    FSG15e2D = vehicle_TDL_2(sheet1['A1'].value, sheet1['A2'].value, sheet1['A3'].value, sheet1['A4'].value, sheet1['A5'].value, sheet1['A6'].value, sheet1['A7'].value, sheet1['A8'].value, sheet1['A9'].value, sheet1['A10'].value, sheet1['A11'].value, sheet1['A12'].value, sheet1['A13'].value, sheet1['A14'].value, 'FSG15e2D', self.Pmax)            
                self.StartVehicle = FSG15e2D    #set start vehicle
                revision = int((self.MaxValue-self.MinValue)/self.Stepsize+1)   #number of calculations to do
                #initialize event with tracks and vehicle
                SimEvent = Event(self.EventName, self.Year, self.StartValue, self.Counter, revision, [self.StartVehicle], ['Endurance_FSA15_Curvature', 'AutoX_FSA15_Curvature', 'Skidpad', 'Acceleration', 'Efficiency_FSA15_Curvature'])
                SimEvent.SimulateEvent()    #call function to simulate the event
                self.Counter += 1   #counter for result file (look module event points)
                self.StartValue += self.Stepsize    #increase the start value with stepsize
          
        elif(self.StartVehicle == 'FSG15e1D'):
            FSG15e1D = vehicle_ODL_2(sheet2['A1'].value, sheet2['A2'].value, sheet2['A3'].value, sheet2['A4'].value, sheet2['A5'].value, sheet2['A6'].value, sheet2['A7'].value, 'FSG15e1D', self.Pmax)
            self.StartVehicle = FSG15e1D    #initialize one dim vehicle
            
            #check which parameter should be changed
            if(self.Parameter == 'C_F'):    
                sheet2['A1'].value = self.MinValue  #get value from file and save it in variable
                self.StartValue = sheet2['A1'].value    #set StartValue on the value from the file
                xlabel = 'C_F [N/rad]'   #set x-axis of plot to variable
            elif(self.Parameter == 'C_R'):
                sheet2['A2'].value = self.MinValue
                self.StartValue = sheet2['A2'].value
                xlabel = 'C_R [N/rad]'
            elif(self.Parameter == 'm'):
                sheet2['A3'].value = self.MinValue
                self.StartValue = sheet2['A3'].value
                xlabel = 'Mass [kg]'
            elif(self.Parameter == 'CoG_X'):
                sheet2['A4'].value = self.MinValue
                self.StartValue = sheet2['A4'].value
                xlabel = 'CoG_X'
            elif(self.Parameter == 'mu'):
                sheet2['A5'].value = self.MinValue
                self.StartValue = sheet2['A5'].value
                xlabel = 'mu'
            elif(self.Parameter == 'alpha'):
                sheet2['A6'].value = self.MinValue
                self.StartValue = sheet2['A6'].value
                xlabel = 'alpha [deg]'
            elif(self.Parameter == 'DriveType'):
                sheet2['A7'].value = self.MinValue
                self.StartValue = sheet2['A7'].value
                xlabel = 'DriveType [2WD]'

            while (self.StartValue <= self.MaxValue):   #loop for increase the parameter value
                if(self.Parameter == 'C_F'):
                    sheet2['A1'].value = self.StartValue    #set value in file on start value
                    #initialize vehicle with new value
                    FSG15e1D = vehicle_ODL_2(sheet2['A1'].value, sheet2['A2'].value, sheet2['A3'].value, sheet2['A4'].value, sheet2['A5'].value, sheet2['A6'].value, sheet2['A7'].value, 'FSG15e1D', self.Pmax)
                elif(self.Parameter == 'C_R'):
                    sheet2['A2'].value = self.StartValue
                    FSG15e1D = vehicle_ODL_2(sheet2['A1'].value, sheet2['A2'].value, sheet2['A3'].value, sheet2['A4'].value, sheet2['A5'].value, sheet2['A6'].value, sheet2['A7'].value, 'FSG15e1D', self.Pmax)
                elif(self.Parameter == 'm'):
                    sheet2['A3'].value = self.StartValue
                    FSG15e1D = vehicle_ODL_2(sheet2['A1'].value, sheet2['A2'].value, sheet2['A3'].value, sheet2['A4'].value, sheet2['A5'].value, sheet2['A6'].value, sheet2['A7'].value, 'FSG15e1D', self.Pmax) 
                elif(self.Parameter == 'CoG_X'):
                    sheet2['A4'].value = self.StartValue
                    FSG15e1D = vehicle_ODL_2(sheet2['A1'].value, sheet2['A2'].value, sheet2['A3'].value, sheet2['A4'].value, sheet2['A5'].value, sheet2['A6'].value, sheet2['A7'].value, 'FSG15e1D', self.Pmax)
                elif(self.Parameter == 'mu'):
                    sheet2['A5'].value = self.StartValue
                    FSG15e1D = vehicle_ODL_2(sheet2['A1'].value, sheet2['A2'].value, sheet2['A3'].value, sheet2['A4'].value, sheet2['A5'].value, sheet2['A6'].value, sheet2['A7'].value, 'FSG15e1D', self.Pmax)
                elif(self.Parameter == 'alpha'):
                    sheet2['A6'].value = self.StartValue
                    FSG15e1D = vehicle_ODL_2(sheet2['A1'].value, sheet2['A2'].value, sheet2['A3'].value, sheet2['A4'].value, sheet2['A5'].value, sheet2['A6'].value, sheet2['A7'].value, 'FSG15e1D', self.Pmax)
                elif(self.Parameter == 'DriveType'):
                    sheet2['A7'].value = self.StartValue
                    FSG15e1D = vehicle_ODL_2(sheet2['A1'].value, sheet2['A2'].value, sheet2['A3'].value, sheet2['A4'].value, sheet2['A5'].value, sheet2['A6'].value, sheet2['A7'].value, 'FSG15e1D', self.Pmax)
                self.StartVehicle = FSG15e1D    #set start vehicle
                #initialize event with tracks and vehicle
                SimEvent = Event(self.EventName, self.Year, self.StartValue, self.Counter, [self.StartVehicle], ['Endurance_FSA15_Curvature', 'AutoX_FSA15_Curvature', 'Skidpad', 'Acceleration', 'Efficiency_FSA15_Curvature'])
                SimEvent.SimulateEvent()    #call function to simulate the event
                self.Counter += 1   #counter for result file (look module event points)
                self.StartValue += self.Stepsize    #increase the start value with stepsize
    
        ResultPlots = Plots('Results.txt', self.MinValue, self.MaxValue, self.StartVehicle, xlabel)
        ResultPlots.ShowPlots()        
