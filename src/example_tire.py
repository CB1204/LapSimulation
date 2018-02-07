from simpleTire import Tire
import numpy as np
import matplotlib.pyplot as plt

# Range of slip angles and slip ratios
sa = np.linspace(-0.8, 0.8, 61)
sr = np.linspace(-0.8, 0.8, 61)

# Create mesh of slip angles and slip ratios
[SA, SR] = np.meshgrid(sa, sr)

# Create Tire
T = Tire()

# Calculate Tire Forces
[fx_sa, fy_sa] = T.force(0, sa, 2000)
[fx_sr, fy_sr] = T.force(sr, 0, 2000)
[FX, FY] = T.force(SR, SA, 2000)

# Plot lateral force vs slip angle
plt.figure(1)
plt.clf()
plt.plot(sa, fy_sa, 'k')

plt.xlabel('sa (rad)')
plt.ylabel('fy (N)')
plt.grid(True)

# Plot longitudinal force vs slip ratio
plt.figure(2)
plt.clf()
plt.plot(sr, fx_sr, 'k')

plt.xlabel('sr (rad)')
plt.ylabel('fx (N)')
plt.grid(True)

# Plot friction ellipse of combined slip
plt.figure(3)
plt.clf()
plt.plot(FY, FX, 'r')
plt.plot(FY.T, FX.T, 'b')

plt.xlabel('fy (N)')
plt.ylabel('fx (N)')
plt.grid(True)

# show all plots
plt.show()
