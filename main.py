from Bezier import *
from Parameters import *
from stateFileModifier import *

###############################################################################################
###############################################################################################

# Beta at inlet and outlet from 1D
beta_in_settings = 24.008 # (beta2, beta in corrispondenza dell'hub all'inlet)
beta_out_settings = 35.15 # (beta4, beta in corrispondenza dell'hub all'outlet)
# Geometrical Parameters from 1D
L_ind = 30
L_comp = 8
r2s = 5.6
r2h = 2
r4  = 10
b4  = 1
r5  = 30
numOfBlades = 9

# Parametrization of blade settings
tau =  [0.5, 1]
w1 = 5

# Constant thickness settings
thickness = 0.2

# Other settings
HubShr_bezier_N = 100
beta_bezier_N = 100

###############################################################################################
###############################################################################################

HubShroud_1D_dimensions = {'object':'HubShroud', 'HubShr_bezier_N':HubShr_bezier_N, 'definition':'xz', 'spline_degree':2, 'L_ind':L_ind,'L_comp':L_comp, 'r2s':r2s, 'r2h':r2h, 'r4':r4, 'b4':b4, 'r5':r5}

Parameters = ParametrizationSettings(
        beta_in_settings = beta_in_settings,
        beta_out_settings = beta_out_settings,
        beta_bezier_N = beta_bezier_N,
        print_conversion_output = False,
        HubShroud_1D_dimensions = HubShroud_1D_dimensions,
        numOfBlades = numOfBlades,
        tau =  tau,
        w1 = w1,
        thickness = thickness,
        par_name = f"LUS")

Geometry_01 = Geometry(Parameters,
                        defaultfilePath = 'defaultBGI\\LUS_General_OnlySpan0_Copy.bgi', # Path of the starting bgi model to modify
                        output_jsonPath = 'modifiedJSON\\LUS_General_OnlySpan0_Copy_leadTrail.json',
                        output_bgiPath = 'modifiedBGI\\MODLUS_General_OnlySpan0_Copy_leadTrail.bgi',
                        output_unmodified_bgiPath = 'unmodifiedBGI\\UNMODLUS_General_OnlySpan0_Copy_leadTrail.bgi',
                        output_bgdPath = 'modifiedBGD\\MODLUS_General_OnlySpan0_Copy_leadTrail.bgd',
                        output_unmodified_bgdPath = 'unmodifiedBGD\\UNMODLUS_General_OnlySpan0_Copy_leadTrail.bgd',
                        std_ANSYS_Folder = "c:\\Program Files\\ANSYS Inc")

#Geometry_01.create_unmodified_json_geometry()
Geometry_01.create_modified_geometry()
#Geometry_01.create_unmodified_bgi_geometry()