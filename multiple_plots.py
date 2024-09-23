from single_plot import plot_Bezier
from Bezier import *
from Parameters import *
import numpy as np

tau_N = 10 # Discrtization of the parameter tau
tau_0_max = 1
tau_0_min = 0
tau_1_max = 1.5
tau_1_min = -0.5

pars_list = [ParametrizationSettings(tau =  [tau_0_ij, tau_1_ij])
        for tau_0_ij in np.linspace(tau_0_min, tau_0_max, tau_N)
        for tau_1_ij in np.linspace(tau_1_min, tau_1_max, tau_N)
    ]

i = 0
for par in pars_list:
    curve = Bezier(par)
    if i < tau_N:
        plot_Bezier(curve, legend = f'tau[1] = {par.tau[1]}')
    else:
        plot_Bezier(curve)
    i+=1

plt.legend()
plt.show()
plt.close()