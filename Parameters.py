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
        self.HubShroud_1D_dimensions = {'object':'HubShroud', 'definition':'xz', 'spline_degree':2, 'L_ind':30,'L_comp':8, 'r2s':5.6, 'r2h':2, 'r4':10, 'b4':1, 'r5':30}
        self.HubShroud_definition = self.HubShroud_1D_dimensions['definition']

        #Settings for deciding the thickness value
        self.modify_Thickness = True
        self.Thickness = 0.2 
        
        self.index = 0 # Used for storing the index of the Simulation

        self.print_conversion_output = False # Used to decide to print or not the output in the terminal

        if self.modify_Blade: 
            if self.Beta_definition =='beta-M%':
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
                    beta_curve_parameters = {'definition':self.Beta_definition,
                                        'object':'Blade',
                                        'beta_in':self.beta_in,
                                        'beta_out':self.beta_out,
                                        'tau':self.tau,
                                        'w1':self.w1,
                                        'spline_degree':self.spline_degree,
                                        'beta_bezier_N':self.beta_bezier_N}
                    self.Beta_M_bezier_curve_points = Bezier(beta_curve_parameters).points


            # NOTE: This overrides the previous declarations
            self.__dict__.update(kwargs)

        if self.modify_HubShroud:
            if self.HubShroud_definition == 'xz': 
                self.spline_degree = self.HubShroud_1D_dimensions['spline_degree']
                L_ind = self.HubShroud_1D_dimensions['L_ind']
                r2h = self.HubShroud_1D_dimensions['r2h']
                r2s = self.HubShroud_1D_dimensions['r2s']
                L_comp = self.HubShroud_1D_dimensions['L_comp']
                r4 = self.HubShroud_1D_dimensions['r4']
                r5 = self.HubShroud_1D_dimensions['r5']
                b4 = self.HubShroud_1D_dimensions['b4']
                
                # HUB AND SHROUD CURVE CALCULATIONS
                self.inducer_Hub_points = [
                    (0        ,  r2h),       # Point A
                    (L_ind*0.6,  r2h),       # Point B
                    (L_ind*0.9,  r2h),       # Point C
                    (L_ind*1  ,  r2h)        # Point D
                ]
                
                self.inducer_Shroud_points = [
                    (0        ,  r2s),       # Point G
                    (L_ind*0.6,  r2s),       # Point H
                    (L_ind*0.9,  r2s),       # Point I
                    (L_ind*1  ,  r2s)        # Point L
                ]
                
                self.Hub_Shroud_curves_points = Bezier(self.HubShroud_1D_dimensions).points # Format of this varaible: [HubProfile_points, ShrProfile_points]
                
                self.diffuser_Hub_points = [
                    (L_ind+L_comp, r4),       # Point E
                    (L_ind+L_comp, r5),       # Point F
                ]
                
                self.diffuser_Shroud_points = [
                    (L_ind+L_comp-b4,  r4),       # Point M
                    (L_ind+L_comp-b4,  r5),       # Point N
                ]

                self.total_Hub_profile = [self.inducer_Hub_points] + [self.Hub_Shroud_curves_points[0]] + [self.diffuser_Hub_points]    
                self.total_Shroud_profile = [self.inducer_Shroud_points] + [self.Hub_Shroud_curves_points[1]] + [self.diffuser_Shroud_points]    

                #INLET CURVE AND EXHAUST CURVE CALCULATIONS
                self.inlet_curve = [
                    (0, r2h),       # Point A
                    (0, r2s),       # Point G
                ]
                self.exhaust_curve = [
                    (L_ind + L_comp - b4, r5),       # Point N
                    (L_ind + L_comp, r5),       # Point F
                ]

                #LEADING AND TRAILING EDGE CALCULATIONS
                #Leading Edge
                (xl1, yl1), (xl2, yl2) = [self.Hub_Shroud_curves_points[0][2], self.Hub_Shroud_curves_points[1][2]]
                num_points = 5  # total points including the start and end
                self.leading_edge_curve = []
                for i in range(num_points):
                    t = i / (num_points - 1)  # parameter from 0 to 1
                    x = xl1 + t * (xl2 - xl1)
                    y = yl1 + t * (yl2 - yl1)
                    self.leading_edge_curve.append((x, y))
                #Trailing Edge
                (xt1, yt1), (xt2, yt2) = [self.Hub_Shroud_curves_points[0][-2], self.Hub_Shroud_curves_points[1][-2]]
                num_points = 5  # total points including the start and end
                self.trailing_edge_curve = []
                for i in range(num_points):
                    t = i / (num_points - 1)  # parameter from 0 to 1
                    x = xt1 + t * (xt2 - xt1)
                    y = yt1 + t * (yt2 - yt1)
                    self.trailing_edge_curve.append((x, y))
                

                # NOTE: This overrides the previous declarations
                self.__dict__.update(kwargs)

        return