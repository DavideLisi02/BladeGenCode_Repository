from Bezier import *
from Parameters import *
from stateFileModifier import *

Parameters = ParametrizationSettings()
Curve = Bezier(Parameters)

Geometry_02 = Geometry(Parameters,
                      Curve,
                      defaultfilePath ='defaultBGI\\geometry02.bgi',
                      output_jsonPath = 'modifiedJSON\\geometry02.json')

#Geometry_02.create_unmodified_json_geometry()
#Geometry_02.create_modified_geometry()
Geometry_02.create_unmodified_bgi_geometry()