import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt

class Bezier:
    """Bezier curve"""

    def __init__(self, parameters, **kwargs):

        super(Bezier, self).__init__()

        # Parameters - see parameters.py for more details
        self.parameters = parameters    

        # Control points
        self.P0 = np.array([0, self.parameters.beta_in])  # Start point
        self.P1 = np.array([100*self.parameters.tau[0], self.parameters.beta_in+(self.parameters.beta_out-self.parameters.beta_in)*self.parameters.tau[1]])  # Control point
        self.P2 = np.array([100, self.parameters.beta_out])  # End point

        # Meridional length values
        self.m_values = np.linspace(0, 100, self.parameters.N) # Discretization of Meridional length

        if self.parameters.spline_degree == 2:
            self.bezier = np.array([((1 - m/100)**2 * self.P0 + 2 * (1 - m/100) * m/100 * self.parameters.w1 * self.P1 + (m/100)**2 * self.P2) /
                                     ((1 - m/100)**2 + 2 * (1 - m/100) * m/100 * self.parameters.w1 + (m/100)**2)   for m in self.m_values])# Bezier curve calculation for each meridional point of the discretization
        else:
            self.bezier = None

        # NOTE: This overrides the previous declarations
        self.__dict__.update(kwargs)

