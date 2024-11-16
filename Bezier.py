import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt

class Bezier:
    """Bezier curve"""
    def __init__(self, curve_parameters, **kwargs):

        super(Bezier, self).__init__()

        # Curve parameters - see parameters.py for more details
        self.object = curve_parameters['object']  
        self.definition = curve_parameters['definition']

        if self.object == 'Blade' and self.definition == 'beta-M%':
            
            self.beta_in = curve_parameters['beta_in']  
            self.beta_out = curve_parameters['beta_out']
            self.object = curve_parameters['tau']  
            self.w1 = curve_parameters['w1']
            self.spline_degree = curve_parameters['spline_degree']
            self.beta_bezier_N = curve_parameters['beta_bezier_N']
            
            if self.spline_degree == 2:

                # Control points
                self.P0 = np.array([0, self.beta_in])  # Start point
                self.P1 = np.array([100*self.tau[0], self.beta_in+(self.beta_out-self.beta_in)*self.tau[1]])  # Control point
                self.P2 = np.array([100, self.beta_out])  # End point

                # Meridional length values
                self.m_values = np.linspace(0, 100, self.beta_bezier_N) # Discretization of Meridional length
                
                points = np.array([((1 - m/100)**2 * self.P0 + 2 * (1 - m/100) * m/100 * self.w1 * self.P1 + (m/100)**2 * self.P2) /
                                        ((1 - m/100)**2 + 2 * (1 - m/100) * m/100 * self.w1 + (m/100)**2)   for m in self.m_values])# Bezier curve calculation for each meridional point of the discretization
                self.points = points.tolist()
            
            else: # For the possibility of using spline curves with different degrees and number of control points
                self.points = None

            # NOTE: This overrides the previous declarations
            self.__dict__.update(kwargs)
        

