from Bezier import *
from Parameters import *
import numpy as np

def plot_Bezier(curve, legend = None):

    curve_points = curve.points
    # Plotting the curve and control points
    plt.plot(curve_points[:, 0], curve_points[:, 1], label=legend)

    return None

parameters = ParametrizationSettings(  # You can change some of the default setting in this line
    tau = [0.3, -1],
    w1 = 1) 

curve = Bezier(parameters) # Computing the parametrization
P0 = curve.P0
P1 = curve.P1
P2 = curve.P2
plot_Bezier(curve)

plt.plot([P0[0], P1[0], P2[0]], [P0[1], P1[1], P2[1]], "ro--", label="Control Points")
plt.text(P0[0], P0[1], 'P0', fontsize=12)
plt.text(P1[0], P1[1], 'P1', fontsize=12)
plt.text(P2[0], P2[1], 'P2', fontsize=12)

plt.legend()
plt.show()
plt.close()