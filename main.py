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

# Parametrization of blade settings
tau =  [0.5, 1]
w1 = 5

###############################################################################################
###############################################################################################

HubShroud_1D_dimensions = {'object':'HubShroud', 'definition':'xz', 'spline_degree':2, 'L_ind':L_ind,'L_comp':L_comp, 'r2s':r2s, 'r2h':r2h, 'r4':r4, 'b4':b4, 'r5':r5}

Parameters = ParametrizationSettings(
        beta_in = beta_in_settings,
        beta_out = beta_out_settings,
        print_conversion_output = True,
        HubShroud_1D_dimensions = HubShroud_1D_dimensions,
        tau =  tau,
        w1 = w1,
        par_name = f"LUS")

Geometry_01 = Geometry(Parameters,
                        defaultfilePath = 'defaultBGI\\LUS_General_OnlySpan0_Copy.bgi', # Path of the starting bgi model to modify
                        output_jsonPath = 'modifiedJSON\\LUS_General_OnlySpan0_Copy.json',
                        output_bgiPath = 'modifiedBGI\\MODLUS_General_OnlySpan0_Copy_leadTrail.bgi',
                        output_unmodified_bgiPath = 'unmodifiedBGI\\UNMODLUS_General_OnlySpan0_Copy_leadTrail.bgi',
                        output_bgdPath = 'modifiedBGD\\MODLUS_General_OnlySpan0_Copy_leadTrail.bgd',
                        output_unmodified_bgdPath = 'unmodifiedBGD\\UNMODLUS_General_OnlySpan0_Copy_leadTrail.bgd',
                        std_ANSYS_Folder = "c:\\Program Files\\ANSYS Inc")

#Geometry_01.create_unmodified_json_geometry()
Geometry_01.create_modified_geometry()
#Geometry_01.create_unmodified_bgi_geometry()