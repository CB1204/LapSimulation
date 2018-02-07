import numpy as np
import csv
from itertools import islice
import matplotlib.pyplot as plt
from geo2ned import NED as NED
from scipy import interpolate as IP
from Curvature import curvature_splines
from scipy import signal as sig
import os
import platform

class Create_TrackMap_2D:
        
    def Create_TrackMap_2D(self, plotsOnOff):     
        FileName = 'Endurance_FSA2015_GPS.csv'
        # FileName = 'Endurance_FSG2015_GPS.csv'
        # FileName = 'AutoX_TimFritz_FSA2015_GPS.csv'
        # FileName = 'Endurance_AirfieldLeipheim_GPS.csv'
        # FileName = 'Skidpad_FSG2015_GPS.csv'
        # FileName = 'AsymmetricOval.csv'

        #FileName = 'AutoX_FSA2016.csv'
        #FileName = 'AutoX_FSG2015.csv'
        #FileName = 'AutoX_FSG2016.csv'
        
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
         
        Timestamp, GPS_Latitude, GPS_Longitude, GPS_Altitude, GPS_Sats_Used = [], [], [], [], [] # define variables
  
        data = csv.reader(open(file,'r'))     # open and read CSV file
 
        for row in islice(data,17, None):     # Put data into list; start with row 18 (because of header)
            try:
                Timestamp.append(row[0])
                GPS_Latitude.append(row[1])
                GPS_Longitude.append(row[2])
                GPS_Altitude.append(row[3])
                GPS_Sats_Used.append(row[4])
            except IndexError:
                pass
 
          
        for i in range(len(Timestamp)):                                 # e.g. "1,12" string into 1.12 float
            Timestamp[i] = Timestamp[i].replace(",",".")
            try:
                Timestamp[i] = float(Timestamp[i])
            except ValueError:
                Timestamp[i] = 0   
 
        for i in range(len(GPS_Longitude)):                             # e.g. "1,12" string into 1.12 float
            GPS_Longitude[i] = GPS_Longitude[i].replace(",",".")
            try:
                GPS_Longitude[i] = float(GPS_Longitude[i])
            except ValueError:
                GPS_Longitude[i] = 0 
             
        for i in range(len(GPS_Latitude)):                              # e.g. "1,12" string into 1.12 float
            GPS_Latitude[i] = GPS_Latitude[i].replace(",",".")
            try:
                GPS_Latitude[i] = float(GPS_Latitude[i])
            except ValueError:
                GPS_Latitude[i] = 0 
             
        for i in range(len(GPS_Altitude)):                              # e.g. "1,12" string into 1.12 float
            GPS_Altitude[i] = GPS_Altitude[i].replace(",",".")
            try:
                GPS_Altitude[i] = float(GPS_Altitude[i])
            except ValueError:
                GPS_Altitude[i] = 0 
             
        for i in range(len(GPS_Sats_Used)):                             # e.g. "1,12" string into 1.12 float
            GPS_Sats_Used[i] = GPS_Sats_Used[i].replace(",",".")
            try:
                GPS_Sats_Used[i] = float(GPS_Sats_Used[i])
            except ValueError:
                GPS_Sats_Used[i] = 0 
 
 
## Define variables for different events
        
        if FileName =='Endurance_FSA2015_GPS.csv' or 'Endurance_FSA2016.csv':                  
            Min_UsedSats = 6
            Max_Distance_deg = 0.01
            dist_step = 0.5
         
            NumRounds_perDriver = 11
            NumDriverChanges = 1
         
            MaxDistance_StartEnd_m = 10
         
            MinRound_length_m = 150
            MinDistance_DriverChange_m = 10
         
            MaxDiff_RoundDistance_m = 10
         
            SplineCoeff_x = 600
            SplineCoeff_y = 600
            
            
        elif FileName =='AsymmetricOval.csv':
            Min_UsedSats = 6
            Max_Distance_deg = 0.01
            dist_step = 0.5
        
            NumRounds_perDriver = 8
            NumDriverChanges = 0
        
            MaxDistance_StartEnd_m = 5
        
            MinRound_length_m = 150
            MinDistance_DriverChange_m = 10
        
            MaxDiff_RoundDistance_m = 10
        
            SplineCoeff_x = 200
            SplineCoeff_y = 450
     
     
        elif FileName =='Endurance_FSG2015_GPS.csv':
            Min_UsedSats = 6
            Max_Distance_deg = 0.01
            dist_step = 0.5
         
            NumRounds_perDriver = 9
            NumDriverChanges = 1
     
            MaxDistance_StartEnd_m = 5
         
            MinRound_length_m = 200
            MinDistance_DriverChange_m = 10
         
            MaxDiff_RoundDistance_m = 10
     
            SplineCoeff_x = 290
            SplineCoeff_y = 280
         
         
        elif FileName == 'AutoX_TimFritz_FSA2015_GPS.csv' or 'AutoX_FSA2016.csv' or 'AutoX_FSG2015.csv' or 'AutoX_FSG2016.csv':
            Min_UsedSats = 6
            Max_Distance_deg = 0.01
            dist_step = 0.5
         
            NumRounds_perDriver = 1
            NumDriverChanges = 1
         
            MaxDistance_StartEnd_m = 5
         
            MinRound_length_m = 200
            MinDistance_DriverChange_m = 10
         
            MaxDiff_RoundDistance_m = 10
         
            SplineCoeff_x = 400
            SplineCoeff_y = 400
            
        elif FileName =='Skidpad_FSG2015_GPS.csv':                  
            Min_UsedSats = 6
            Max_Distance_deg = 0.01
            dist_step = 0.5
         
            NumRounds_perDriver = 2
            NumDriverChanges = 0
         
            MaxDistance_StartEnd_m = 5
         
            MinRound_length_m = 50
            MinDistance_DriverChange_m = 10
         
            MaxDiff_RoundDistance_m = 10
         
            SplineCoeff_x = 600
            SplineCoeff_y = 600
         
         
        elif FileName == 'Endurance_AirfieldLeipheim_GPS.csv':
            Min_UsedSats = 6
            Max_Distance_deg = 0.01
            dist_step = 0.5
         
            NumRounds_perDriver = 29
            NumDriverChanges = 1
         
            MaxDistance_StartEnd_m = 15
         
            MinRound_length_m = 100
            MinDistance_DriverChange_m = 10
         
            MaxDiff_RoundDistance_m = 20
         
            SplineCoeff_x = 150
            SplineCoeff_y = 150
  
             
## get deltaT
  
        dT = Timestamp[1] - Timestamp[0]

## Remove Signal, which has 
  
        Index_delete = np.nonzero((np.abs(GPS_Longitude - np.median(GPS_Longitude)) > Max_Distance_deg)|
                                  (np.abs(GPS_Latitude - np.median(GPS_Latitude)) > Max_Distance_deg)|
                                  (np.abs(GPS_Latitude) == 0)| 
                                  (np.abs(GPS_Longitude) == 0)| 
                                  (np.abs(GPS_Sats_Used) < Min_UsedSats))
  
        Index_delete = Index_delete[0]
          
        GPS_Longitude_Val = GPS_Longitude
        GPS_Latitude_Val = GPS_Latitude
        GPS_Altitude_Val = GPS_Altitude
          
        for offset, index in enumerate(Index_delete):
            index -= offset
            del Timestamp[index]
            del GPS_Longitude_Val[index]
            del GPS_Latitude_Val[index]
            del GPS_Altitude_Val[index]
 
        Timestamp = np.asarray(Timestamp)

## Transform LLH Coordinates to NED (North-East-Down)
 
        xCoordinates = []
        yCoordinates = []
        i = 0
          
        ned = NED(np.mean(GPS_Latitude_Val), np.mean(GPS_Longitude_Val), np.mean(GPS_Altitude_Val)) # Create reference plane
          
        for i in range(0, len(GPS_Longitude_Val)):
            coordinate = [GPS_Latitude_Val[i], GPS_Longitude_Val[i], GPS_Altitude_Val[i]]
            xCoordinates.append(ned.geodetic2ned(coordinate)[0])
            yCoordinates.append(ned.geodetic2ned(coordinate)[1])
            i = i+1
              
        xCoordinates = xCoordinates - np.min(xCoordinates)
        yCoordinates = yCoordinates - np.min(yCoordinates)
#         
        plt.plot(yCoordinates, xCoordinates)
        plt.grid(True)
        plt.show()       
        
          
## Get Start and End of Track  
        
        Distance = np.cumsum(((xCoordinates[1:] - xCoordinates[0:-1])**2 + (yCoordinates[1:] - yCoordinates[0:-1])**2)**0.5) 

          
        Endpoints_ovr = [] 
#         EndpointsKoord_x_ovr = []
#         EndpointsKoord_y_ovr = []
#         EndpointsKoord_Mean_x_ovr = []
#         EndpointsKoord_Mean_y_ovr = []
        EndpointsSpread_ovr = []
        EndpointsIndex_ovr = []
     
        counter = 0
        EndVal_counter = len(Timestamp) - 1
        possibleEndpoints = []
              
        while counter <= EndVal_counter:             
                   
            Startpoint_xKoord = xCoordinates[counter]
            Startpoint_yKoord = yCoordinates[counter]

            possibleEndpoints = np.asarray(np.nonzero(((np.subtract(Distance[counter : ], Distance[counter])) >= MinRound_length_m) 
                                                      & ((((np.subtract(xCoordinates[counter + 1: ], Startpoint_xKoord))**2 + (np.subtract(yCoordinates[counter + 1: ], Startpoint_yKoord))**2)**0.5) <= MaxDistance_StartEnd_m))) + counter - 1                      
            possibleEndpoints =  np.ndarray.flatten(possibleEndpoints)
        
            
            # Sort in possible Endpoints
            distanceEndpoints = np.absolute(np.tile(Distance[possibleEndpoints], (len(possibleEndpoints), 1)) - np.transpose(np.tile(Distance[possibleEndpoints], (len(possibleEndpoints), 1))))

            Endpoints = [] 
            EndpointsMean = []
            EndpointsKoord_x = [] 
            EndpointsKoord_y = [] 
            EndpointsKoord_Mean_x = [] 
            EndpointsKoord_Mean_y = []
                 
            counterEndpoints = np.arange(0, len(possibleEndpoints))
            
            if len(possibleEndpoints) >= (NumRounds_perDriver * (NumDriverChanges + 1) + NumDriverChanges):
                while (len(counterEndpoints) > 0):

                    sameEndpoints = np.nonzero(distanceEndpoints[counterEndpoints[0], counterEndpoints] < MinDistance_DriverChange_m)

                    Endpoints.append(possibleEndpoints[sameEndpoints + counterEndpoints[0]])                         
                    
                    EndpointsMean.append(np.round(np.mean(Endpoints[-1])))
                     
                    EndpointsKoord_x.append(xCoordinates[Endpoints[-1]])     
                    EndpointsKoord_y.append(yCoordinates[Endpoints[-1]])
 
                    EndpointsKoord_Mean_x.append(np.mean(EndpointsKoord_x[-1]))
                    EndpointsKoord_Mean_y.append(np.mean(EndpointsKoord_y[-1]))
                     
                    counterEndpoints = np.delete(counterEndpoints, sameEndpoints)
                
  
                EndpointsSpread = np.var(EndpointsKoord_Mean_x, ddof=1) + np.var(EndpointsKoord_Mean_y, ddof=1)

                if len(Endpoints) == (NumRounds_perDriver * (NumDriverChanges + 1) + NumDriverChanges):
                    
                    Endpoints_ovr.append(Endpoints)
#                     EndpointsKoord_x_ovr.append(EndpointsKoord_x)
#                     EndpointsKoord_y_ovr.append(EndpointsKoord_y)
#                     EndpointsKoord_Mean_x_ovr.append(EndpointsKoord_Mean_x)
#                     EndpointsKoord_Mean_y_ovr.append(EndpointsKoord_Mean_y)
                    EndpointsSpread_ovr.append(EndpointsSpread)
                    
                    EPs = np.append(counter, EndpointsMean)
                    EndpointsIndex_ovr.append(EPs)

                    if (len(Endpoints_ovr)) == 1:
                        EndVal_counter = np.min([counter + 2000, len(Timestamp) - 1])

            counter = counter +1
    
        BestEndpointFit_Index = np.argmin(EndpointsSpread_ovr)
        BestEndpointsIndex = EndpointsIndex_ovr[BestEndpointFit_Index]       
        
## Create Rounds
   
        RoundsCounter = np.arange(1,(NumRounds_perDriver * (NumDriverChanges + 1) + NumDriverChanges + 1))
        RoundsDriverChange = np.arange(NumRounds_perDriver + 1, NumRounds_perDriver * (NumDriverChanges + 1) + NumDriverChanges, NumRounds_perDriver)
        RoundsDriverChange = RoundsDriverChange + np.cumsum(np.ones(len(RoundsDriverChange))) - 1
        RoundsCounter = np.delete(RoundsCounter, RoundsDriverChange - 1)
    
        NumRounds = len(RoundsCounter)
        diffIndex = BestEndpointsIndex[1:] - BestEndpointsIndex[0:-1]
        maxSize = np.max(diffIndex[RoundsCounter -1])
          
        xKoord_rounds = np.zeros([maxSize, NumRounds])
        yKoord_rounds = np.zeros([maxSize, NumRounds])
        Distance_rounds = np.zeros([maxSize, NumRounds])
        Timestamp_rounds = np.zeros([maxSize, NumRounds])
        
 
## Interpolate Rounds to maxSize
        
        counter_Rounds = 0        
        while counter_Rounds <= NumRounds -1:
                
            Timestamp_rounds[: , counter_Rounds] = np.linspace(Timestamp[BestEndpointsIndex[RoundsCounter[counter_Rounds] -1] -1], Timestamp[BestEndpointsIndex[RoundsCounter[counter_Rounds]] -1], maxSize)
            
            xKoord_rounds[: , counter_Rounds] = np.interp(Timestamp_rounds[:, counter_Rounds], 
                                                          Timestamp[BestEndpointsIndex[RoundsCounter[counter_Rounds] -1] -1 : BestEndpointsIndex[RoundsCounter[counter_Rounds]] -1], 
                                                          xCoordinates[BestEndpointsIndex[RoundsCounter[counter_Rounds] -1] -1 : BestEndpointsIndex[RoundsCounter[counter_Rounds]] -1])
            yKoord_rounds[: , counter_Rounds] = np.interp(Timestamp_rounds[:, counter_Rounds],
                                                          Timestamp[BestEndpointsIndex[RoundsCounter[counter_Rounds] -1] -1 : BestEndpointsIndex[RoundsCounter[counter_Rounds]] -1], 
                                                          yCoordinates[BestEndpointsIndex[RoundsCounter[counter_Rounds] -1] -1 : BestEndpointsIndex[RoundsCounter[counter_Rounds]] -1])                                                                      
           
            Distance_rounds[: , counter_Rounds] = np.append(0, np.cumsum(((xKoord_rounds[ 1:, counter_Rounds] - xKoord_rounds[0:-1, counter_Rounds])**2 + (yKoord_rounds[ 1: , counter_Rounds] - yKoord_rounds[0:-1, counter_Rounds])**2)**0.5))

            counter_Rounds += 1  
        
     
## Create Spline

        UsedRounds = np.nonzero(np.absolute(np.median(Distance_rounds[-1,:]) - Distance_rounds[-1, :]) < MaxDiff_RoundDistance_m)
        
        # Overlay all rounds over distance
        Distance_rounds_used = Distance_rounds[: , UsedRounds]
        Distance_sort = np.sort(Distance_rounds_used, axis=None)
        SortIndex = np.argsort(Distance_rounds_used, axis=None)
          
        xKoord_ovr = np.ndarray.flatten(xKoord_rounds[:, UsedRounds])
        xKoord_ovr = xKoord_ovr[SortIndex]
           
        yKoord_ovr = np.ndarray.flatten(yKoord_rounds[:, UsedRounds])
        yKoord_ovr = yKoord_ovr[SortIndex]
        
        #Build mean values
        count_1 = 1
        count_2 = 0
 
        x_mean_Matrix = []
        y_mean_Matrix = []
        Distance_sort_mean_Matrix = []
         
        while count_1 <= NumRounds:
      
            x_mean_Matrix.append(xKoord_ovr[count_2:len(xKoord_ovr) - NumRounds + count_2 + 1])
            y_mean_Matrix.append(yKoord_ovr[count_2:len(yKoord_ovr) - NumRounds + count_2 + 1])
             
            Distance_sort_mean_Matrix.append(Distance_sort[count_2:len(Distance_sort) - NumRounds + count_2 + 1])
      
            count_1 = count_1 + 1
            count_2 = count_2 + 1
         
        xKoord_ovr_mean = np.mean(x_mean_Matrix, axis=0)
        yKoord_ovr_mean = np.mean(y_mean_Matrix, axis=0)
        Distance_sort_mean = np.mean(Distance_sort_mean_Matrix, axis=0)
 
         
        #create spline
        pp_xKoord = IP.UnivariateSpline(Distance_sort_mean, xKoord_ovr_mean, s = SplineCoeff_x)  
        pp_yKoord = IP.UnivariateSpline(Distance_sort_mean, yKoord_ovr_mean, s = SplineCoeff_y)  
          
        Dist_Steps = np.arange(0, np.max(Distance_sort), dist_step)
 
         
        xKoord_Track = pp_xKoord(Dist_Steps)
        yKoord_Track = pp_yKoord(Dist_Steps)
        
        # ALternative Spline
#         xKoord_Track = sig.savgol_filter(xKoord_ovr, 31, 3)
#         yKoord_Track = sig.savgol_filter(yKoord_ovr, 31, 3)
# 
#          
        Distance_Track = np.cumsum(((xKoord_Track[1:] - xKoord_Track[0:-1])**2 + (yKoord_Track[1:] - yKoord_Track[0:-1])**2)**0.5)
#         
#         Dist_Steps = np.linspace(0, np.max(Distance_sort), len(xKoord_Track))
        
        
        if plotsOnOff == True:
            f, axarr = plt.subplots(2, sharex=True)
            axarr[0].plot(Distance_sort, xKoord_ovr, 'g', linewidth = 0.5, label = 'xKoord_ovr')
            axarr[0].plot(Dist_Steps, xKoord_Track, 'r', linewidth = 1, label = 'xKoord_Track')
            axarr[0].plot(Distance_sort_mean, xKoord_ovr_mean, 'b', linewidth = 0.75, label = 'xKoord_ovr_mean')
            axarr[0].set_title('x Coordinates vs. Distance')
            axarr[0].set_xlabel('Distance [m]')
            axarr[0].set_ylabel('x Coordinate [m]')
            axarr[0].grid(True)
            axarr[0].legend(shadow=True, fancybox=True)
        
            axarr[1].plot(Distance_sort, yKoord_ovr, 'g', linewidth = 0.5, label = 'yKoord_ovr')
            axarr[1].plot(Dist_Steps, yKoord_Track, 'r', linewidth = 1, label = 'yKoord_Track')
            axarr[1].plot(Distance_sort_mean, yKoord_ovr_mean, 'b', linewidth = 0.75, label = 'yKoord_ovr_mean')
            axarr[1].set_xlabel('Distance [m]')
            axarr[1].set_ylabel('y Coordinate [m]')
            axarr[1].grid(True)
            axarr[1].legend(shadow=True, fancybox=True)
            plt.show()
        
        
## Calculate curvature

#         xp =  np.gradient(xKoord_Track)
#         xpp = np.gradient(xp)
#         yp = np.gradient(yKoord_Track)
#         ypp = np.gradient(yp)
#         kappa = (xp*ypp - xpp*yp) / ((xp**2 + yp**2)**(3/2))
        
        xKoord_Track[-1] = xKoord_Track[0]
        yKoord_Track[-1] = yKoord_Track[0]
        
        kappa = curvature_splines(xKoord_Track, yKoord_Track)
        kappa[-1] = kappa[0]
        radius = np.divide(1, kappa)        
        
        if plotsOnOff == True:
            f, axarr = plt.subplots(2, sharex=True)
            axarr[0].plot(Distance_Track, kappa[:-1], label = 'kappa')
            axarr[0].set_title('Curvature vs. Distance')
            axarr[0].set_xlabel('Distance [m]')
            axarr[0].set_ylabel('Curvature [1/m]')
            axarr[0].legend(shadow=True, fancybox=True)
            axarr[0].grid(True)
        
            axarr[1].plot(Distance_Track, radius[:-1], label = 'radius')
            axarr[1].set_title('Radius vs. Distance')
            axarr[1].set_xlabel('Distance [m]')
            axarr[1].set_ylabel('Radius [m]') 
            axarr[1].set_ylim([-750, 750])              
            axarr[1].legend(shadow=True, fancybox=True)
            axarr[1].grid(True)
            plt.show()
        
#         b, a = signal.butter(1,0.0001)                    Does filter make sense??? FLo ?
#         kappa_filt = signal.filtfilt(b,a,kappa)

 
## Plot Results
        
        if plotsOnOff == True:
            plt.figure(2)
            plt.clf()
            plt.plot(yKoord_rounds, xKoord_rounds, linestyle = '--')
            plt.plot(yKoord_Track, xKoord_Track, linewidth = 2.5, color='r', label = 'SplineFit - Round Length: ' + str(int(np.round(Distance_Track[-1]))) +  ' m')
            plt.plot(yKoord_Track[0],xKoord_Track[0], marker = 'o', markersize = 15, markerfacecolor = 'y', markeredgecolor = 'y', linestyle = 'None', label = 'Startpoint')
            plt.grid(True)
            plt.title((FileName.replace('_', ' ')).replace('.csv', ''))
            plt.xlabel('x [m]')
            plt.ylabel('y [m]')
            plt.legend(numpoints=1, shadow=True, fancybox=True)
            plt.show()
        
#         #Open file and write Values into it
#         cwd = os.getcwd()
#         #pfad = cwd + '\CSV\AutoX_FSG15_Curvature.csv'
#         #writer = csv.writer(test_file, 'w')
#         test_file = open(pfad, 'w')
#         LAENGE = len(kappa)-1
#         print("Len(kappa)= %d ", LAENGE)
#         for i in range(0,LAENGE):
#             test_file.write("%s,%s,%s\n" %(kappa[i],xKoord_Track[i], yKoord_Track[i]))
#             
#         test_file.close()
        return kappa, xKoord_Track, yKoord_Track