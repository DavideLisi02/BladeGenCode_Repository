from Bezier import *

"""Parametrization Settings"""

class ParametrizationSettings:

    def __init__(self,
                 beta_in_settings = 35,
                 beta_out_settings = 60,
                 spline_degree_settings = 2, # Degree of the spline,
                 tau_settings = [0.5, 0.5], # Adimensional parameters for varying the parametrization configuration. The first value affects the meridional position of the control point. The second value affects the beta value of the control point
                 beta_bezier_N_settings = 60, # Number of points for Meridional length's discretisation
                 fibers_settings = 'General_only_at_Hub', #Set True if the .bgi file has Radial Fiber definition
                 type_of_parametrization_settings = 'Bezier', # String containing th name of the method used for parametrization. Possible methods: 'Bezier'
                 w1_settings = 1,# Weight on the second control point of the spline (set it = 1 for no-rational Bezier curve)
                **kwargs):
        """
        Class containing all the settings and information about
        the parametrized model.
        """
        super(ParametrizationSettings, self).__init__()

        #Settings for the Blade Parametrization
        self.modify_Blade = True
        self.Beta_definition = 'beta-M%' # Possible entries: 'beta-M%'
        self.beta_bezier_N = beta_bezier_N_settings
        
        #Settings for deciding the number of blades
        self.modify_numOfBlades = True
        self.numOfBlades = 9

        #Settings for modifying the Hub and Shroud profiles accordingly to 1D    
        self.modify_HubShroud = True
        self.HubShr_bezier_N = 100
        self.HubShroud_1D_dimensions = {'object':'HubShroud', 'HubShr_bezier_N':self.HubShr_bezier_N,'definition':'xz', 'spline_degree':2, 'L_ind':30,'L_comp':8, 'r2s':5.6, 'r2h':2, 'r4':10, 'b4':1, 'r5':30}
        self.HubShroud_definition = self.HubShroud_1D_dimensions['definition']

        #Settings for deciding the thickness value
        self.modify_Thickness = True
        self.thickness = 0.2 
        
        self.index = 0 # Used for storing the index of the Simulation

        self.print_conversion_output = False # Used to decide to print or not the output in the terminal

        if self.modify_Blade: 
            if self.Beta_definition =='beta-M%':
                self.beta_in = beta_in_settings # Beta value at the inlet
                self.beta_out = beta_out_settings # Beta value at the outlet

                self.spline_degree = spline_degree_settings # Degree of the spline
                self.tau = tau_settings # Adimensional parameters for varying the parametrization configuration. The first value affects the meridional position of the control point. The second value affects the beta value of the control point
                self.beta_bezier_N = beta_bezier_N_settings # Number of points for Meridional length's discretisation

                self.fibers = fibers_settings #Set True if the .bgi file has Radial Fiber definition
                self.type_of_parametrization = type_of_parametrization_settings # String containing th name of the method used for parametrization. Possible methods: 'Bezier'
                self.w1 = w1_settings# Weight on the second control point of the spline (set it = 1 for no-rational Bezier curve)

                self.par_name = f"{str(self.tau[0]).replace('.', '')}_{str(self.tau[1]).replace('.', '')}_{str(self.w1).replace('.', '')}" # String used for the name of the output file

                print(f"\nComputing bezier curve for beta/m curve: tau = {self.tau} | w1 = {self.w1}\n")

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

                #SPLITTER BLADE

                #Splliter point leading edge point at hub
                hub_meridional_target = 0.3
                hub_profile = np.array(self.Hub_Shroud_curves_points[0])                
                ds_hub = np.sum((hub_profile[1:,:] - hub_profile[:-1,:])**2,axis=1)**0.5
                meridional_hub = np.zeros(ds_hub.shape[0]+1)
                for i in range(ds_hub.shape[0]):
                    meridional_hub[i+1]=ds_hub[i]+meridional_hub[i]
                meridional_norm_hub = meridional_hub/np.max(meridional_hub)
                idx_hub = np.argmin(np.abs(hub_meridional_target-meridional_norm_hub))
                coords_splitter_hub = hub_profile[idx_hub,:]

                #Splliter point leading edge point at shroud
                sh_meridional_target = 0.3
                sh_profile = np.array(self.Hub_Shroud_curves_points[1])
                ds_sh = np.sum((sh_profile[1:,:] - sh_profile[:-1,:])**2,axis=1)**0.5
                meridional_sh = np.zeros(ds_sh.shape[0]+1)
                for i in range(ds_sh.shape[0]):
                    meridional_sh[i+1]=ds_sh[i]+meridional_sh[i]
                meridional_norm_sh = meridional_sh/np.max(meridional_sh)
                idx_sh = np.argmin(np.abs(sh_meridional_target-meridional_norm_sh))
                coords_splitter_sh = sh_profile[idx_sh,:]

                #Splitter Leading Edge
                self.splitter_LE = [
                    coords_splitter_hub.tolist(), 
                    coords_splitter_sh.tolist()
                ]

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
                (xl1, yl1), (xl2, yl2) = [self.Hub_Shroud_curves_points[0][1], self.Hub_Shroud_curves_points[1][1]]
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

        if self.modify_Thickness:
            m_perc_values = np.linspace(0, 100, 5)
            self.thickness_curve = [(m_perc, self.thickness) for m_perc in m_perc_values]

            # NOTE: This overrides the previous declarations
            self.__dict__.update(kwargs)

        return