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
points=100
beta=np.linspace(0,np.pi, points)

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


def rotate(x,y, gamma):
    x = x * np.cos(gamma) - y * np.sin(gamma)
    y = x * np.sin(gamma) + y * np.cos(gamma)
    return x, y

### rotate 45 degree
beta = 45 * np.pi / 180.
X_ss_rot, Y_ss_rot = rotate(X_ss, Y_ss, beta)
X_ps_rot, Y_ps_rot = rotate(X_ps, Y_ps, beta)

import matplotlib.pyplot as plt

fig, ax = plt.subplots()
# ax.plot(x, T, label='thickness')
plt.title('NACA 0006 (modified)')
ax.plot(x, C, '--', label='Chamberline')
ax.plot(X_ss, Y_ss, marker='.', label='ss')
ax.plot(X_ps, Y_ps, marker='.', label='ps')
ax.plot(X_ss_rot, Y_ss_rot, marker='.', label='ss')
ax.plot(X_ps_rot, Y_ps_rot, marker='.', label='ps')
ax.axis('equal')
ax.legend()
fig.tight_layout()
plt.show()

np.savetxt("ps.csv", np.c_[X_ps_rot, Y_ps_rot], delimiter=",")
np.savetxt("ss.csv", np.c_[X_ss_rot, Y_ss_rot], delimiter=",")

### write geomTurbo
with open("output.geomTurbo", 'w', encoding = 'utf-8') as f:
    f.write("GEOMETRY TURBO\n")
    f.write("VERSION        5.8\n")
    f.write("UNITS          Meters\n")
    f.write("UNITS-FACTOR   1\n")
    f.write("suction\n")
    f.write("SECTIONAL\n")
    f.write("# section 1\n")
    f.write("2\n")
    f.write("XYZ\n")
    f.write("".format(len(X_ss_rot)))
    for i, _ in enumerate(X_ss_rot):
        x = X_ss_rot[i]
        y = Y_ss_rot[i]
        z = 0.0
        f.write("{:.08f} {:.08f} {:.08f}\n".format(x,y,z))

    f.write("# section 2\n")
    f.write("2\n")
    f.write("XYZ\n")
    f.write("".format(len(X_ss_rot)))
    for i, _ in enumerate(X_ss_rot):
        x = X_ss_rot[i]
        y = Y_ss_rot[i]
        z = 1.0
        f.write("{:.08f} {:.08f} {:.08f}\n".format(x,y,z))

    f.write("pressure\n")
    f.write("SECTIONAL\n")
    f.write("2\n")
    f.write("# section 1\n")
    f.write("XYZ\n")
    f.write("".format(len(X_ps_rot)))
    for i, _ in enumerate(X_ps_rot):
        x = X_ps_rot[i]
        y = Y_ps_rot[i]
        z = 0.0
        f.write("{:.08f} {:.08f} {:.08f}\n".format(x,y,z))
    f.write("# section 2\n")
    f.write("XYZ\n")
    f.write("".format(len(X_ps_rot)))
    for i, _ in enumerate(X_ps_rot):
        x = X_ps_rot[i]
        y = Y_ps_rot[i]
        z = 1.0
        f.write("{:.08f} {:.08f} {:.08f}\n".format(x,y,z))

