from Bezier import *
from Parameters import *
from stateFileModifier import *

Parameters = ParametrizationSettings(
        beta_in = 24.008,
        beta_out = 35.15,
        print_conversion_output = True,
        tau =  [0.5, 1],
        w1 = 5,
        par_name = f"LUS")

Curve = Bezier(Parameters)

Geometry_02 = Geometry(Parameters,
                        Curve,
                        defaultfilePath = 'defaultBGI\\LUS.bgi', # Path of the starting bgi model to modify
                        output_jsonPath = 'modifiedJSON\\MODLUS_test.json',
                        output_bgiPath = 'modifiedBGI\\MODLUS_test.bgi',
                        output_unmodified_bgiPath = 'unmodifiedBGI\\UNMODLUS_test.bgi',
                        output_bgdPath = 'modifiedBGD\\MODLUS_test.bgd',
                        output_unmodified_bgdPath = 'unmodifiedBGD\\UNMODLUS_test.bgd',
                        std_ANSYS_Folder = "c:\\Program Files\\ANSYS Inc")

#Geometry_02.create_unmodified_json_geometry()
Geometry_02.create_modified_geometry()
#Geometry_02.create_unmodified_bgi_geometry()