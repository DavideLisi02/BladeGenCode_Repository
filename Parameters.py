from Bezier import *

"""Parametrization Settings"""

class ParametrizationSettings:

    def __init__(self,
                **kwargs):
        """
        Class containing all the settings and information about
        the parametrized model.
        """
        super(ParametrizationSettings, self).__init__()

        #Settings for the Blade Parametrization
        self.modify_Blade = True
        self.Beta_definition = 'beta-M%' # Possible entries: 'beta-M%'
        
        #Settings for deciding the number of blades
        self.modify_numOfBlades = True
        self.numOfBlades = 9

        #Settings for modifying the Hub and Shroud profiles accordingly to 1D    
        self.modify_HubShroud = True
        self.HubShroud_1D_dimensions = {}

        #Settings for deciding the thickness value
        self.modify_Thickness = True
        self.Thickness = 0.2 
        
        self.index = 0 # Used for storing the index of the Simulation

        self.print_conversion_output = False # Used to decide to print or not the output in the terminal

        if self.modify_Blade: 
            if self.definition=='beta-M%':
                self.beta_in = 40 # Beta value at the inlet
                self.beta_out = 60 # Beta value at the outlet

                self.spline_degree = 2 # Degree of the spline
                self.tau = [0.5, 0.5] # Adimensional parameters for varying the parametrization configuration. The first value affects the meridional position of the control point. The second value affects the beta value of the control point
                self.beta_bezier_N = 60 # Number of points for Meridional length's discretisation

                self.fibers = 'General_only_at_Hub' #Set True if the .bgi file has Radial Fiber definition
                self.type_of_parametrization = 'Bezier' # String containing th name of the method used for parametrization. Possible methods: 'Bezier'
                self.w1 = 1# Weight on the second control point of the spline (set it = 1 for no-rational Bezier curve)

                self.par_name = f"{str(self.tau[0]).replace('.', '')}_{str(self.tau[1]).replace('.', '')}_{str(self.w1).replace('.', '')}" # String used for the name of the output file

                if self.type_of_parametrization == 'Bezier':
                    curve_parameters = {'definition':self.definition,
                                        'object':'Blade',
                                        'beta_in':self.beta_in,
                                        'beta_out':self.beta_out,
                                        'tau':self.tau,
                                        'w1':self.w1,
                                        'spline_degree':self.spline_degree,
                                        'beta_bezier_N':self.beta_bezier_N}
                    self.Beta_M_bezier_curve_points = Bezier(curve_parameters)


            # NOTE: This overrides the previous declarations
            self.__dict__.update(kwargs)
        return