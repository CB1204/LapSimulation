from LSvehicleOneDimLookup_2 import vehicleOneDimLookup_2 as vehicle_ODL_2
from LSvehicleTwoDimLookup import vehicleTwoDimLookup as vehicle_TDL
from LSvehicleTwoDimLookup_2 import vehicleTwoDimLookup_2 as vehicle_TDL_2
from LSvehicleAeroMassTire import vehicleAeroMassTire as vehicle_TMA
from LSvehicleGeneral import vehicleGeneral as vehicle_GEN
from eventPoints import Scoring
from eventPoints import Event
import lapsim as lts
from track import Track as Track
import numpy as np
import matplotlib.pyplot as plt
from Create_TrackMap_2D import Create_TrackMap_2D
from Import_measured_Speed import ImportSpeed as IS
import openpyxl
import os
import math
from parameterStudy import ParamStudy


#  #Define Vehicle (un-comment one vehicle to select it)
# V = vehicle_ODL()  # One dimensional lookup
# V = vehicle_ODL_2(12000, 16000, 255, 0.58, 1, 7, '2WD','xy1')  # One dimensional lookup
# V = vehicle_TDL()  # Two dimensional lookup
# V = vehicle_TDL_2(12000, 16000, 280, 0.63, 1.2, 7, 0.61, 3.2, 1.22, '2WD', 12.98, 0.2286, 0.013, 2.05,'xy2')  # Two dimensional lookup # CLA 15e = 
# V = vehicle_TMA()  # Simple model representing a Tire, a Mass, and Aero forces
# V = vehicle_GEN()  # More general vehicle with four wheels, steering, differential, etc... (takes a lot longer to run!)
# 
# #Define Track
# k = 0.25 # curvature of tightest corner (k = 0.25/m => radius = 1/k = 4m)
# 
# curvature = np.r_[
#     np.zeros(31),
#     np.linspace(0, k, 10),
#     np.linspace(0.9*k, 0, 9),
#     np.linspace(0, k/2, 10),
#     np.linspace(0.9*k/2, 0, 9),
#     np.zeros(31)] # Simple track with two corners and one straight. Not actually a closed track...
# curvature, xKoord_Track, yKoord_Track = Create_TrackMap_2D.Create_TrackMap_2D(0, True)
# ds = 0.5  # length of each track segment
# 
# track = Track(curvature, ds)
# 
#  # Initialize Lap Simulation
# LS = lts.LapSim(V, track)
# LS.max_laps = 2
# 
#  # Run Lap Simulation
#  
# LS.speed_profile()
# 
#  # Present Results
# print('Laptime = ' + str(LS.lapTime) +' s')
# 
# f = np.ones((track.s.shape[0], 1))
# f[LS.direction < 0] = np.nan
# r = np.ones((track.s.shape[0], 1))
# r[LS.direction > 0] = np.nan
# 
# RealSpeed, RealTime = IS.ImportSpeed(0, 880) # Import real speed and real time 880 6
# RealSpeed = RealSpeed(track.s)
# RealTime = RealTime(np.max(track.s))
# print('Realtime = ' + (str(np.around(RealTime))) + ' s')
# 
#  #Calculate fitting
# difference = np.trapz(np.absolute(LS.state.speed[:,0] - RealSpeed) / (np.trapz(np.absolute(LS.state.speed[:,0]) + np.absolute(RealSpeed), track.s)), track.s)
# ovr_fit = (1 - difference)* 100
# print('Fitting = ' + str(ovr_fit) +' %')
#         
#  # plot speeds
# plt.figure(1)
# plt.clf()
# plt.plot(track.s, LS.state.speed, 'r',)
#  # plt.plot(track.s, LS.state_f.speed * f, 'b')
#  # plt.plot(track.s, LS.state_r.speed * r, 'r')
#  # plt.plot(track.s, LS.state_max.speed, 'g')
# plt.plot(track.s, RealSpeed, 'g', linewidth = 2)
#  # plt.plot(track.s[LS.critical_points], LS.state_max.speed[LS.critical_points, 0], 'ko')
#  
# plt.ylim((0, 30))
# plt.xlabel('sLap (m)')
# plt.ylabel('vCar (m/s)')
# plt.grid(True)
# 
# plt.show()
# 
#  # Plot speed over track
# colorMapMin = 0
# colorMapMax = 35
# 
# fig, axarr = plt.subplots(2, sharex=True)
# ax0 = axarr[0].scatter(yKoord_Track, xKoord_Track, s = 80,  c = LS.state.speed, linewidths = 0, vmin=colorMapMin, vmax=colorMapMax )
# axarr[0].set_title('Laptime speed')
# axarr[0].set_xlabel('x [m]')
# axarr[0].set_ylabel('y [m]')
# axarr[0].set_xlim([-2, np.max(yKoord_Track) + 5])  
# axarr[0].grid(True)
# 
# ax1 = axarr[1].scatter(yKoord_Track, xKoord_Track, s = 80, c = RealSpeed, linewidths = 0, vmin=colorMapMin, vmax=colorMapMax )
# axarr[1].set_title('Real speed')
# axarr[1].set_xlabel('x [m]')
# axarr[1].set_ylabel('y [m]')
# axarr[1].set_xlim([-2, np.max(yKoord_Track) + 5])
# axarr[1].grid(True)
# 
# cax = fig.add_axes([0.93, 0.1, 0.02, 0.8])
# fig.colorbar(ax0, cax=cax)
# 
# plt.show()

#Create_TrackMap_2D.Create_TrackMap_2D(0, True)

#Initialzie parameter study and call it
# study = ParamStudy(Track, year, variable, step, minVal, maxVal, parameterSetting)
study1 = ParamStudy('FSA', 2015, 'C_F', 250, 10000, 15000, 'FSG15e2D')
study1.SimulateParamStudy()

