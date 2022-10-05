import numpy as np

"""
Standard configuration 10 

T. H. Fransson and J. M. Verdon. Updated report on Standard Configurations for
the Determination of unsteady Flow Through Vibrating Axial-flow Turbomachine-
Cascades. Technical Report TRITA/KRV/92.009, KTH, Stockholm, 1992

"""


H_T = 0.06
H_C = 0.05
R = (H_C * H_C + 0.25) / (2 * H_C)
angle = 45
beta=np.linspace(0,np.pi,100)

x=(1-np.cos(beta))/2.

T = H_T * (2.969 * pow(x, 0.5) - 1.26 * x - 3.516 * pow(x,2) + 2.843 * pow(x, 3) - 1.036 * pow(x, 4))
C = H_C - R + pow((R*R - pow(x- 0.5, 2)), 0.5)

dC = np.gradient(C)
dx = np.gradient(x)

theta = np.arctan(dC / dx)
X_ss = (x - 0.5 * T * np.sin(theta))
Y_ss = (C + 0.5 * T * np.cos(theta))

X_ps = (x + 0.5 * T * np.sin(theta))
Y_ps = (C - 0.5 * T * np.cos(theta))

import matplotlib.pyplot as plt

fig, ax = plt.subplots()
# ax.plot(x, T, label='thickness')
plt.title('NACA 0006 (modified)')
ax.plot(x, C, '--', label='Chamberline')
ax.plot(X_ss, Y_ss, marker='.', label='ss')
ax.plot(X_ps, Y_ps, marker='.', label='ps')
ax.axis('equal')
ax.legend()
fig.tight_layout()
plt.show()

np.savetxt("ps.csv", np.c_[X_ps, Y_ps], delimiter=",")
np.savetxt("ss.csv", np.c_[X_ss, Y_ss], delimiter=",")
