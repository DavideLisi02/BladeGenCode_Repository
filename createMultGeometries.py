from Bezier import *
from Parameters import *
from stateFileModifier import *
import Folder_management

###########################################################
###########################################################

# SETTINGS OF THE SIMULATED DATASET

# Print Results & Conversion Output | Y/n = True/False
print_results = True
print_conversion_output = False

# Beta at inlet and outlet from 1D
beta_in_settings = 24.008 # (beta_2, beta in corrispondenza dell'hub all'inlet)
beta_out_settings = 35.15 # (beta_4, beta in corrispondenza dell'hub all'outlet)

# Geometrical Parameters from 1D
L_ind = 30 #30
L_comp = 8 #8
r2s = 7 #5.6
r2h = 2 #2
r4  = 10 #10
b4  = 1 #1
r5  = 30 #30

# Constant thickness settings
thickness = 0.2

# Decide how many points to compute for the Bezier curves
beta_bezier_N = 100
HubShr_bezier_N = 100

# Discrtization of the parameter tau_0
tau_0_N = 1 
tau_0_max = 1
tau_0_min = 0
# Discrtization of the parameter tau_1
tau_1_N = 4 
tau_1_max = 1.5
tau_1_min = -0.5
# Discrtization of the parameter w1
w1_N = 1 
w1_min = 1
w1_max = 10 

# Folder Management Settings
Project_Name = "Database Test 1"
Project_Folder = "D:\Davide"
default_geometry_path = 'defaultBGI\\LUS_General_OnlySpan0_Copy.bgi'
std_BLADEGEN_Folder_settings = "C:\\Program Files\\ANSYS Inc"





###########################################################
###########################################################

Folder_management.Create_Project_Folder(Project_Name = "Database Test 1",
                      Project_Folder = "D:\Davide",
                      default_geometry_path = 'defaultBGI\\LUS_General_OnlySpan0_Copy.bgi')

tau_0 = np.linspace(tau_0_min, tau_0_max, tau_0_N)
tau_1 = np.linspace(tau_1_min, tau_1_max, tau_1_N)
w1 = np.linspace(w1_min, w1_max, w1_N)
HubShroud_1D_dimensions = {'object':'HubShroud', 'HubShr_bezier_N':HubShr_bezier_N, 'definition':'xz', 'spline_degree':2, 'L_ind':L_ind,'L_comp':L_comp, 'r2s':r2s, 'r2h':r2h, 'r4':r4, 'b4':b4, 'r5':r5}


# Creating the parameters 
pars_list = [ParametrizationSettings(
    beta_in_settings = beta_in_settings,
    beta_out_settings = beta_out_settings,
    beta_bezier_N = beta_bezier_N,
    HubShroud_1D_dimensions = HubShroud_1D_dimensions,
    print_conversion_output = print_conversion_output,
    tau =  [tau_0_ijk, tau_1_ijk],
    w1 = w1_ijk,
    thickness = thickness,
    index = ((i*tau_0_N+j)*tau_1_N)+k,
    par_name = f"{str(tau_0_ijk).replace('.', '')}_{str(tau_1_ijk).replace('.', '')}_{str(w1_ijk).replace('.', '')}")
                for i,tau_0_ijk in enumerate(tau_0)
                for j,tau_1_ijk in enumerate(tau_1)
                for k,w1_ijk in enumerate(w1)
    ]

# Creating the results dictionary 
results_dict = { ((i*tau_0_N+j)*tau_1_N)+k : [[tau_0_ijk, tau_1_ijk, w1_ijk],"Results"] #The "Results" string at the end is where the results will be stored (Still to be implemented), while the first one is the index
                for i,tau_0_ijk in enumerate(tau_0)
                for j,tau_1_ijk in enumerate(tau_1)
                for k,w1_ijk in enumerate(w1) }


for par in pars_list:
    file_index = par.index # Index used for the name of the stored files
    file_code = f"{par.par_name}" # Code used for the name of the stored files
    file_name_settings = f"geometry_{file_index}_{file_code}"
    Geometry_i= Geometry(par,
                        defaultfilePath = f"defaultBGI\\LUS_General_OnlySpan0_Copy.bgi",
                        file_name = file_name_settings,
                        Project_name = Project_Name,
                        Project_Folder = Project_Folder,
                        std_BLADEGEN_Folder = "C:\\Program Files\\ANSYS Inc\\v242\\aisol\\BladeModeler\\BladeGen")

    #Geometry_i.create_unmodified_json_geometry()
    Geometry_i.create_modified_geometry() # TO BE MODIFIED : | 1 Setup Ansys Folder | 2: go to stateFileModifier.create_modified_geometry | 3: uncomment line saying self.convert_bgi_to_bgd(self.output_bgiPath, self.output_bgdPath, ANSYSfolderPath = self.std_ANSYS_Folder)
    #Geometry_i.create_unmodified_bgi_geometry()
    if print_results:
        print(f"Geometry was created for  : tau = {par.tau} | w1 = {par.w1} | Name = {par.par_name}")

if print_results:
    print(f"Results Dictionary Initialized:\n{results_dict}\n")