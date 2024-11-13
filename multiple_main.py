from Bezier import *
from Parameters import *
from stateFileModifier import *

###########################################################
###########################################################

# SETTINGS OF THE SIMULATED DATASET

# Discrtization of the parameter tau_0
tau_0_N = 3 
tau_0_max = 1
tau_0_min = 0
# Discrtization of the parameter tau_1
tau_1_N = 3 
tau_1_max = 1.5
tau_1_min = -0.5
# Discrtization of the parameter w1
w1_N = 3 
w1_min = 1
w1_max = 10 

# Folder Management Settings
default_geometry_settings = '02'
defaultfilefolder_settings ='defaultBGI\\'
output_jsonfolder_settings = 'modifiedJSON\\'
output_bgifolder_settings = 'modifiedBGI\\'
output_unmodified_bgifolder_settings = 'unmodifiedBGI\\'
output_bgdfolder_settings = 'modifiedBGD\\'
output_unmodified_bgdfolder_settings = 'unmodifiedBGD\\'
std_ANSYS_Folder_settings = "c:\\Program Files\\ANSYS Inc"

###########################################################
###########################################################

tau_0 = np.linspace(tau_0_min, tau_0_max, tau_0_N)
tau_1 = np.linspace(tau_1_min, tau_1_max, tau_1_N)
w1 = np.linspace(tau_1_min, tau_1_max, w1_N)

# Creatin
pars_list = [ParametrizationSettings(
    tau =  [tau_0_ijk, tau_1_ijk],
    w1 = w1_ijk,
    index = ((i*tau_0_N+j)*tau_1_N)+k )
                for i,tau_0_ijk in enumerate(tau_0)
                for j,tau_1_ijk in enumerate(tau_1)
                for k,w1_ijk in enumerate(w1)
    ]

results_dict = { ((i*tau_0_N+j)*tau_1_N)+k : [[tau_0_ijk, tau_1_ijk, w1_ijk],"Results"] #The "Results" string at the end is where the results will be stored (Still to be implemented), while the first one is the index
                for i,tau_0_ijk in enumerate(tau_0)
                for j,tau_1_ijk in enumerate(tau_1)
                for k,w1_ijk in enumerate(w1) }

for par in pars_list:
    Curve = Bezier(par)
    file_index = par.index # Index used for the name of the stored files
    file_code = f"{default_geometry_settings}_{par.par_name}" # Code used for the name of the stored files
    Geometry_i= Geometry(par,
                        Curve,
                        defaultfilePath = f"{defaultfilefolder_settings}geometry{default_geometry_settings}.bgi",
                        output_jsonPath = f"{output_jsonfolder_settings}MODgeometry_{file_index}_{file_code}.json",
                        output_bgiPath = f"{output_bgifolder_settings}MODgeometry_{file_index}_{file_code}.bgi",
                        output_unmodified_bgiPath = f"{output_unmodified_bgifolder_settings}UNMODgeometry_{file_index}_{file_code}.bgi",
                        output_bgdPath = f"{output_bgdfolder_settings}MODgeometry_{file_index}_{file_code}.bgd",
                        output_unmodified_bgdPath = f"{output_unmodified_bgdfolder_settings}UNMODgeometry_{file_index}_{file_code}.bgd",
                        std_ANSYS_Folder = "c:\\Program Files\\ANSYS Inc")

    #Geometry_02.create_unmodified_json_geometry()
    Geometry_i.create_modified_geometry() # Go to bgi-bgd conversion and uncomment the line needed oince AnsysiBatcher has been setup - go to stateFileModifier.create_modified_geometry
    #Geometry_02.create_unmodified_bgi_geometry()


print(f"Results Dictionary Initialized:\n{results_dict}\n")