import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from numpy import nan


"""
This module is to compute a (theoretical) plot showing the maximum possible transferred force and torque at the 
tires of the vehicle.
It uses a set of vehicle parameters, but does not consider actual driveline performance
"""

# parameters
m = 280         # total mass of vehicle including driver
L = 1.535       # vehicle axle distance [m]
CGx = 0.58      # relative position of CG in x direction [-]
CGz = 0.28      # absolute height of CG in z direction [m]
CPx = 0.6       # relative position of CP in x direction [-]
CPz = 0.5       # absolute height of CP in z direction [m]
c_x = 1.83      # aerodynamic coefficient x (drag)
c_z = 4.18      # aerodynamic coefficient z (downforce)
A = 1           # surface area [m^2]
v = (0,40)      # range for velocity [m/s]
a = (-20,15)    # range for acceleration [m/s^2]
mue = 1.3       # road friction
f_roll = 0.01   # rolling resistance
TorqueMaxMachine = 35 #Nm
i_machine = 11
r_dyn = 0.228

maxP = 80000 # Maximum power the competition allows
maxP_machine = 25000 # maximum power of a single machine

useVariableRatio = True # if true, the wheel torques are allowed to be unequally distributed

#output parametrization:
plotFz = False
plotFx = True
plotFxLtd = False
plotPower = False
plotPowerLimited = True
plotTorque = True
plotAccelLine = True

def F_air(rho, cwA,v):
    return 1/2*rho*cwA*v**2

def F_inert(m,a):
    return m*a 

# constants
g = 9.81    # earth acceleration [m/s^2]
rho = 1.22  # density of air [kg/m^3]

#preprocessing
CGx=L*CGx
CPx=L*CPx
maxP_ax = 2*maxP_machine
TmaxTire = TorqueMaxMachine*i_machine

#prepare vectors and arrays
Vel = np.linspace(v[0],v[1])
Acc = np.linspace(a[0],a[1])
[Vel,Acc] = np.meshgrid(Vel,Acc)
Vel_kph=Vel*3.6
F_drag = F_air(rho,c_x*A,Vel[:])
F_down = F_air(rho,c_z*A,Vel[:])
F_accel = F_inert(m,Acc[:])
F_grav = np.ones(Vel.shape)*m*g
# Fz forces
Fz_r = 1/L*(F_grav * CGx + F_accel * CGz + F_down * CPx + F_drag * CPz)
Fz_f = 1/L*(F_grav * (L-CGx) - F_accel * CGz + F_down * (L-CPx) - F_drag * CPz)
Fz_ratio = Fz_f/(Fz_r+Fz_f)
# Fx forces
# for these forces, only consider the force actually transferred
# the maximum transferrable force at this point is calculated as:
Fx_r_max = Fz_r*mue
Fx_f_max = Fz_f*mue
Fx_max = Fx_r_max + Fx_f_max
# the resistance forces are calculated as: 
# assumption: The drive force is applied to the wheels according to the Fz-distribution
F_resistance = F_drag+f_roll*(F_grav+F_down)+F_accel
Fx_f_act = Fz_ratio * F_resistance
Fx_r_act = F_resistance - Fx_f_act
# if Fx_max is smaller than the resistance forces, this is an infeasible point
feas_pts=Fx_max<F_resistance

#compute Fx_ltd
Fx_r_ltd = Fx_r_act
Fx_r_ltd[np.abs(Fx_r_ltd)>np.abs(Fx_r_max)] = np.nan

Fx_f_ltd = Fx_f_act
Fx_f_ltd[np.abs(Fx_f_ltd)>np.abs(Fx_f_max)] = np.nan

Fx_ltd = Fx_r_ltd + Fx_f_ltd

# Wheel power
# first, show only competition limits
Pr = Fx_r_act*Vel
Pf = Fx_f_act*Vel
Ptot = Pr+Pf

Pr_ltd = Pr
Pf_ltd = Pf
Pr_ltd[Ptot>maxP]=np.nan
Pr_ltd[Ptot>maxP]=np.nan
Ptot[Ptot>maxP]=np.nan
# second, show only points which were previously deemed feasible and consider vehicle power
# build the max power matrix:

Tmax_v = maxP_ax/Vel[:]
Tmax_v[Tmax_v>2*TmaxTire] = TmaxTire

#now, compute for all points whether they are feasible (i.e. enough torque can be supplied)
Treq_f=Fx_f_ltd*r_dyn
Treq_r=Fx_r_ltd*r_dyn


Treq_f[np.abs(Treq_f)>Tmax_v]=np.nan
Treq_r[np.abs(Treq_r)>Tmax_v]=np.nan
if useVariableRatio:
    Treq = (Fx_f_ltd+Fx_r_ltd)*r_dyn
    Treq[Treq>2*Tmax_v]=np.nan
else:
    Treq = Treq_f+Treq_r

# now find the highest acceleration still possible for the given powertrain as a function of the velocity
vel_line = np.linspace(v[0],v[1])*3.6
acc_vals = np.linspace(a[0],a[1])
# set all nans to zero, as there is a problem with the argmax function else:
Treq[np.isnan(Treq)]=0
# axis is the one which should be left out, (not maxed over - max over velocity, get one value for each acceleration)
accel_idx = np.argmax(Treq, axis = 0)
accel_pos = np.array([acc_vals[a] for a in accel_idx])
accel_idx = np.argmin(Treq, axis = 0)
accel_neg = np.array([acc_vals[a] for a in accel_idx])

if plotFz:
    #force Rear
    fig1 = plt.figure()
    ax = fig1.add_subplot(111, projection='3d')
    ax.plot_surface(Vel_kph,Acc,Fz_r)
    ax.set_xlabel('Velocity [km/h]')
    ax.set_ylabel('Acceleration [m/s^2]')
    ax.set_zlabel('Tire contact force rear [N]')
  
    #force Front
    fig2 = plt.figure()
    ax = fig2.add_subplot(111, projection='3d')
    ax.plot_surface(Vel_kph,Acc,Fz_f)
    ax.set_xlabel('Velocity [km/h]')
    ax.set_ylabel('Acceleration [m/s^2]')
    ax.set_zlabel('Tire contact force front [N]') 
       
    #force sum
    fig3 = plt.figure()
    ax = fig3.add_subplot(111, projection='3d')
    ax.plot_surface(Vel_kph,Acc,Fz_f+Fz_r)
    ax.set_xlabel('Velocity [km/h]')
    ax.set_ylabel('Acceleration [m/s^2]')
    ax.set_zlabel('Tire contact force vehicle [N]')    
    plt.show()
    
if plotFx:
    #force Rear
    fig1 = plt.figure()
    ax = fig1.add_subplot(111, projection='3d')
    ax.plot_surface(Vel_kph,Acc,Fx_r_act)
    ax.set_xlabel('Velocity [km/h]')
    ax.set_ylabel('Acceleration [m/s^2]')
    ax.set_zlabel('Drive force rear [N]')
    ax.plot_surface(Vel_kph,Acc,Fx_r_max,color="red")
    ax.plot_surface(Vel_kph,Acc,-Fx_r_max,color="red")

    #force Front
    fig2 = plt.figure()
    ax = fig2.add_subplot(111, projection='3d')
    ax.plot_surface(Vel_kph,Acc,Fx_f_act)
    ax.set_xlabel('Velocity [km/h]')
    ax.set_ylabel('Acceleration [m/s^2]')
    ax.set_zlabel('Drive force front [N]') 
    ax.plot_surface(Vel_kph,Acc,Fx_f_max,color="red")
    ax.plot_surface(Vel_kph,Acc,-Fx_f_max,color="red")
       
    #force sum
    fig3 = plt.figure()
    ax = fig3.add_subplot(111, projection='3d')
    ax.plot_surface(Vel_kph,Acc,Fx_f_act+Fx_r_act)
    ax.set_xlabel('Velocity [km/h]')
    ax.set_ylabel('Acceleration [m/s^2]')
    ax.set_zlabel('Drive force vehicle [N]')    
    ax.plot_surface(Vel_kph,Acc,Fx_max,color="red")
    ax.plot_surface(Vel_kph,Acc,-Fx_max,color="red")
    plt.show()
    
if plotFxLtd:
    #force Rear
    fig1 = plt.figure()
    ax = fig1.add_subplot(111, projection='3d')
    ax.plot_surface(Vel_kph,Acc,Fx_r_ltd)
    ax.set_xlabel('Velocity [km/h]')
    ax.set_ylabel('Acceleration [m/s^2]')
    ax.set_zlabel('Tire contact force rear [N]')
  
    #force Front
    fig2 = plt.figure()
    ax = fig2.add_subplot(111, projection='3d')
    ax.plot_surface(Vel_kph,Acc,Fx_f_ltd)
    ax.set_xlabel('Velocity [km/h]')
    ax.set_ylabel('Acceleration [m/s^2]')
    ax.set_zlabel('Tire contact force front [N]') 
       
    #force sum
    fig3 = plt.figure()
    ax = fig3.add_subplot(111, projection='3d')
    ax.plot_surface(Vel_kph,Acc,Fx_ltd)
    ax.set_xlabel('Velocity [km/h]')
    ax.set_ylabel('Acceleration [m/s^2]')
    ax.set_zlabel('Tire contact force vehicle [N]')    
    plt.show()

if plotPower:
    #power Rear
    fig1 = plt.figure()
    ax = fig1.add_subplot(111, projection='3d')
    ax.plot_surface(Vel_kph,Acc,Pr)
    ax.set_xlabel('Velocity [km/h]')
    ax.set_ylabel('Acceleration [m/s^2]')
    ax.set_zlabel('Power rear [W]')
  
    #power Front
    fig2 = plt.figure()
    ax = fig2.add_subplot(111, projection='3d')
    ax.plot_surface(Vel_kph,Acc,Pf)
    ax.set_xlabel('Velocity [km/h]')
    ax.set_ylabel('Acceleration [m/s^2]')
    ax.set_zlabel('Power front [W]') 
       
    #power sum
    fig3 = plt.figure()
    ax = fig3.add_subplot(111, projection='3d')
    ax.plot_surface(Vel_kph,Acc,Pf+Pr)
    ax.set_xlabel('Velocity [km/h]')
    ax.set_ylabel('Acceleration [m/s^2]')
    ax.set_zlabel('Power vehicle [W]')    
    plt.show()

if plotPowerLimited:
    #power Rear
    fig1 = plt.figure()
    ax = fig1.add_subplot(111, projection='3d')
    ax.plot_surface(Vel_kph,Acc,Pr_ltd)
    ax.set_xlabel('Velocity [km/h]')
    ax.set_ylabel('Acceleration [m/s^2]')
    ax.set_zlabel('Power rear Limited [W]')
  
    #power Front
    fig2 = plt.figure()
    ax = fig2.add_subplot(111, projection='3d')
    ax.plot_surface(Vel_kph,Acc,Pf_ltd)
    ax.set_xlabel('Velocity [km/h]')
    ax.set_ylabel('Acceleration [m/s^2]')
    ax.set_zlabel('Power front Limited [W]') 
       
    #power sum
    fig3 = plt.figure()
    ax = fig3.add_subplot(111, projection='3d')
    ax.plot_surface(Vel_kph,Acc,Ptot)
    ax.set_xlabel('Velocity [km/h]')
    ax.set_ylabel('Acceleration [m/s^2]')
    ax.set_zlabel('Power vehicle Limited [W]')    
    plt.show()
    
if plotTorque:
    #power Rear
    fig1 = plt.figure()
    ax = fig1.add_subplot(111, projection='3d')
    ax.plot_surface(Vel_kph,Acc,Treq_r)
    ax.set_xlabel('Velocity [km/h]')
    ax.set_ylabel('Acceleration [m/s^2]')
    ax.set_zlabel('torque rear Limited [Nm]')
  
    #power Front
    fig2 = plt.figure()
    ax = fig2.add_subplot(111, projection='3d')
    ax.plot_surface(Vel_kph,Acc,Treq_f)
    ax.set_xlabel('Velocity [km/h]')
    ax.set_ylabel('Acceleration [m/s^2]')
    ax.set_zlabel('torque front Limited [Nm]') 
       
    #power sum
    fig3 = plt.figure()
    ax = fig3.add_subplot(111, projection='3d')
    ax.plot_surface(Vel_kph,Acc,Treq)
    ax.set_xlabel('Velocity [km/h]')
    ax.set_ylabel('Acceleration [m/s^2]')
    ax.set_zlabel('torque vehicle Limited [Nm]')    
    plt.show()
    
if plotAccelLine:
    fig1 = plt.figure()
    ax = fig1.add_subplot(111)
    ax.plot(vel_line, accel_pos)    
    ax.plot(vel_line, accel_neg)
    ax.set_xlabel('Velocity [km/h]')
    ax.set_ylabel('maximum Acceleration [m/s^2]')
    ax.grid()
    plt.show()