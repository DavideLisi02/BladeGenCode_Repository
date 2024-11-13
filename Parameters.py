"""Parametrization Settings"""

class ParametrizationSettings:

    def __init__(self,
                **kwargs):
        """
        Class containing all the settings and information about
        the parametrized model.
        """
        super(ParametrizationSettings, self).__init__()

        self.object = 'Blade'  # Possible entries: 'Blade'
        self.definition = 'beta-M%' # Possible entries: 'beta-M%'
        
        self.index = 0 # Used for storing the index of the SImulation

        self.print_conversion_output = False

        if self.object=='Blade' and self.definition=='beta-M%':
            self.beta_in = 40 # Beta value at the inlet
            self.beta_out = 60 # Beta value at the outlet

            self.spline_degree = 2 # Degree of the spline
            self.tau = [0.5, 0.5] # Adimensional parameters for varying the parametrization configuration. The first value affects the meridional position of the control point. The second value affects the beta value of the control point
            self.N = 60 # Number of points for Meridional length's discretisation

            self.radialFibers = True #Set True if the .bgi file has Radial Fiber definition
            self.type_of_parametrization = 'Bezier' # String containing th name of the method used for parametrization. Possible methods: 'Bezier'
            self.w1 = 1# Weight on the second control point of the spline (set it = 1 for no-rational Bezier curve)

            self.par_name = f"{str(self.tau[0]).replace('.', '')}_{str(self.tau[1]).replace('.', '')}_{str(self.w1).replace('.', '')}" # String used for the name of the output file

            # NOTE: This overrides the previous declarations
            self.__dict__.update(kwargs)
        return