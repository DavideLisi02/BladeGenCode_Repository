from utils.Bezier import * # maybe to be removed from here
from utils.GeometrySettings import *
from utils.stateFileModifier import *


Geometry = GeometrySettings(
    #Blade Parameters
    beta_in = 24, # Beta value at the inlet
    beta_out = 35, # Beta value at the outlet
    thickness = 0.2, # Thickness value
    tau = [0.5, 0.6], # tau = [tau_0, tau_1], where tau_0 is the meridional position of the control point and tau_1 is the beta value of the control point
    w1 = 2, # Weight on the second control point of the spline (set it = 1 for no-rational Bezier curve)
    beta_bezier_N = 300, # Number of points for Meridional length's discretisation
    #Hub and Shroud Parameters
    L_ind = 30,
    L_comp = 8,
    r2s = 5.6,
    r2h = 2,
    r4 = 10,
    b4 = 1,
    r5 = 30,
    modify_HubShroud=True, # If True, the Hub and Shroud profiles will be modified accordingly to the 1D values
    w1_hb = 1, # Weight on the second control point of the spline for the Hub profile
    w1_sh = 1, # Weight on the second control point of the spline for the Shroud profile
    #Splitter settings
    splitter_LE_meridional_target_hub=0.3, # Meridional target for the splitter leading edge on the hub
    splitter_LE_meridional_target_sh=0.3 # Meridional target for the splitter leading edge on the shroud
)


StateFile = StateFileModifier(
    Geometry,
    defaultfilePath = f"defaultBGI\\LUS_General_OnlySpan0_Copy.bgi", # Path of the default geometry file, located in ...//utils//defaultBGI
    destination_path = "D:\\Davide\\geometry_test.bgd", # Path where the modified geometry file will be saved
    std_BLADEGEN_Folder = "C:\\Program Files\\ANSYS Inc\\v242\\aisol\\BladeModeler\\BladeGen"  # Path of the BladeGen folders
    )

StateFile.create_modified_geometry()

