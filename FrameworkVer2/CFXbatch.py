"""
The CFXbatch framework allows users to effortlessly launch CFD simulations for turbocompressors based on specified geometries and operating conditions. "launcher.py" is an example of script where the user
defines the simulation parameters and launches the calculations by running CFX in the background (i.e. batch mode). While many aspects of the CFD setup are pre-configured, the framework offers flexibility 
to adjust key factors that vary across different scenarios, as deemed important by the author.

Author: Issam Soukhmane
Date: 23-09-2024
"""

import os
import subprocess

abspath = os.path.abspath(__file__)
package_path = os.path.dirname(abspath)
os.chdir(package_path)

################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################

def substitute_after_equal(input_string, replacement_string):
    # Find the index of '=' in the input string
    equal_index = input_string.find('=')

    if equal_index != -1:
        # Substitute characters after '=' with the replacement string
        result_string = input_string[:equal_index + 1] + replacement_string
    else:
        # If '=' is not found, raise a ValueError
        raise ValueError("Equal sign (=) not found in the input string.")

    return result_string
                
def convert_slashes(path,mode):

    if(mode == 'forward'):
        return path.replace('\\', '/')
    if(mode == 'backward'):
        return path.replace('/', '\\')
    

def create_or_overwrite_folder(folder_path):
    # Check if the folder exists
    if os.path.exists(folder_path):
        # If it exists, remove it and its contents
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for directory in dirs:
                os.rmdir(os.path.join(root, directory))
        os.rmdir(folder_path)

    # Create a new folder
    os.makedirs(folder_path)

################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################

def update_WORKBENCH_template(package_path, project_path, case_name, simulation_definition):

    script_template = """
# encoding: utf-8
# 2023 R1
SetScriptVersion(Version="23.1.153")

########################################################################################### BLADEgen SCRIPTING

# SETTING UP BLADEgen 

template0 = GetTemplate(TemplateName="BladeGen")
system0 = template0.CreateSystem()
bladeDesign1 = system0.GetContainer(ComponentName="Blade Design")

option1 = bladeDesign1.Import(FilePath="{bladegen_path}")

template1 = GetTemplate(TemplateName="TurboGrid")
bladeDesignComponent1 = system0.GetComponent(Name="Blade Design")
componentTemplate1 = GetComponentTemplate(Name="TSMeshTemplate")
system1 = template1.CreateSystem(DataTransferFrom=[Set(FromComponent=bladeDesignComponent1, TransferName=None, ToComponentTemplate=componentTemplate1)],RelativeTo=system0)

Save(FilePath="{workbench_path}",Overwrite=True)

########################################################################################### TURBOgrid SCRIPTING

designPoint1 = Parameters.GetDesignPoint(Name="0")

# SETTING UP TURBOgrid

turboMesh1 = system1.GetContainer(ComponentName="Turbo Mesh")

# SENDING COMMANDS TO TURBOgrid

turboMesh1.Edit()




turboMesh1.SendCommand(Command=\"\"\"GEOMETRY:
MACHINE DATA:
File Length Units = mm
Machine Type = Centrifugal Compressor
END
END
PARAMETERIZATION:
END\"\"\")

turboMesh1.SendCommand(Command=\"\"\"LIBRARY:
  CEL:
    EXPRESSIONS:
      global size factor = 0.77
    END
  END
END\"\"\")
turboMesh1.SendCommand(Command=\"\"\"PARAMETERIZATION:
  INPUT FIELD: global size factor
    Method = Expression
    Expression Name = global size factor
  END
END\"\"\")
turboMesh1.SendCommand(Command=\"\"\"LIBRARY:
  CEL:
    EXPRESSIONS:
      tip clearance = 50 [micron]
    END
  END
END\"\"\")
turboMesh1.SendCommand(Command=\"\"\"PARAMETERIZATION:
  INPUT FIELD: tip clearance
    Method = Expression
    Expression Name = tip clearance
  END
END\"\"\")
turboMesh1.SendCommand(Command=\"\"\"LIBRARY:
  CEL:
    EXPRESSIONS:
      tip clearance = 5E-05 [m]
    END
  END
END\"\"\")



turboMesh1.SendCommand(Command=\"\"\"GEOMETRY:
BLADE SET:
SHROUD TIP:
Option = Normal Distance
Tip Clearance = tip clearance
END
END
END\"\"\")



turboMesh1.SendCommand(Command=\"\"\"
GEOMETRY:
INLET:
Parametric Hub Location = 0.01
Parametric Shroud Location = 0.01
END
END\"\"\")



turboMesh1.SendCommand(Command=\"\"\"GEOMETRY:
OUTLET:
Parametric Hub Location = 0.03
Parametric Shroud Location = 0.03
END
END\"\"\")



turboMesh1.SendCommand(Command=\"\"\"MESH DATA:
  ATM Constant First Element Offset = On
  ATM Five Star Vertex Mesh Size Factor = 0.7
  ATM Proportional BL Factor Base = 3.0
  ATM Proportional BL Factor Ratio = 0.0
  ATM Spanwise To B2B Count Factor = 1
  Between Boundary Layers Distribution Option = End Ratio
  Boundary Layer Specification Method = Proportional
  Global Size Factor = global size factor
  HGrid At Inlet = on
  HGrid At Outlet = on
  HGrid in Parametric Space at Inlet = Off
  HGrid in Parametric Space at Outlet = Off
  High Fidelity Hub Tip Interface Size Mode = Size Factor
  High Fidelity Shroud Tip Interface Size Mode = Size Factor
  Inlet Default Growth Ratio = 1.05
  Inlet Defining Parameter Type = Target Expansion Rate
  Inlet Domain = On
  Inlet Multi Segment Enabled = On
  Inlet Multi Segment First Element Factor = 0.1
  LE Cutoff Edge Split Factor = 1.0
  Meridional Splitter Boundary Layer Factor = 1.0
  Mesh Size Specification Mode = Topology Block Edge Split
  Outlet Default Growth Ratio = 1.05
  Outlet Defining Parameter Type = Target Expansion Rate
  Outlet Domain = On
  Outlet Multi Segment Enabled = On
  Outlet Multi Segment First Element Factor = 0.1
  Override Inlet Distribution = Off
  Override Outlet Distribution = Off
  Reynolds Number = 1.0e6
  TE Cutoff Edge Split Factor = 1.05
  Target Maximum Expansion Rate Enabled = On
  Vertex Offset Specification Mode = Absolute
  BLADE MESH DATA: Main Blade
    ATM Hub Tip Maximum Expansion Rate = 1.3
    ATM Hub Tip Maximum Expansion Rate Enabled = Off
    ATM Shroud Tip Maximum Expansion Rate = 1.3
    ATM Shroud Tip Maximum Expansion Rate Enabled = Off
    Cutoff Blade Edge Expansion Factor = 0.5
    GGI Tip Hub Le Cut Off MeanLine Method = Auto
    GGI Tip Hub Te Cut Off MeanLine Method = Auto
    GGI Tip Shroud Le Cut Off MeanLine Method = Auto
    GGI Tip Shroud Te Cut Off MeanLine Method = Auto
    Override Hub Tip Element Count Calculation = Off
    Override Shroud Tip Element Count Calculation = Off
  END
  BLADE MESH DATA: Splitter Blade 1
    ATM Hub Tip Maximum Expansion Rate = 1.3
    ATM Hub Tip Maximum Expansion Rate Enabled = Off
    ATM Shroud Tip Maximum Expansion Rate = 1.3
    ATM Shroud Tip Maximum Expansion Rate Enabled = Off
    Cutoff Blade Edge Expansion Factor = 0.5
    GGI Tip Hub Le Cut Off MeanLine Method = Auto
    GGI Tip Hub Te Cut Off MeanLine Method = Auto
    GGI Tip Shroud Le Cut Off MeanLine Method = Auto
    GGI Tip Shroud Te Cut Off MeanLine Method = Auto
    Override Hub Tip Element Count Calculation = Off
    Override Shroud Tip Element Count Calculation = Off
  END
END
MESH DATA:
  Override Outlet Element Count Calculation = 0
  Outlet Default Growth Ratio = 1.05
  Outlet Multi Segment Enabled = On
END
MESH DATA:
  Override Inlet Element Count Calculation = 0
  Inlet Default Growth Ratio = 1.05
  Inlet Multi Segment Enabled = On
END
TOPOLOGY SET:
  Lock Down ATM Mesh Size = Off
END
PARAMETERIZATION:
END\"\"\")






parameter1 = Parameters.GetParameter(Name="P1")
designPoint1.SetParameterExpression(
    Parameter=parameter1,
    Expression="{mesh_size_factor}")
parameter2 = Parameters.GetParameter(Name="P2")
designPoint1.SetParameterExpression(
    Parameter=parameter2,
    Expression="{tip_clearance} [micron]")

turboMesh1.SendCommand(Command="> update")
turboMesh1.SendCommand(Command="> um mode=normal, object=/TOPOLOGY SET")
turboMesh1.SendCommand(Command="> update")
turboMesh1.SendCommand(Command="> update")

Save(FilePath="{workbench_path}",Overwrite=True)

turboMesh1.Exit()

########################################################################################### CFXpre SCRIPTING

# SETTING UP CFXpre

template2 = GetTemplate(TemplateName="CFX")
system2 = GetSystem(Name="TS")
turboMeshComponent1 = system2.GetComponent(Name="Turbo Mesh")
componentTemplate1 = GetComponentTemplate(Name="CFXPhysicsTemplate")
system3 = template2.CreateSystem(DataTransferFrom=[Set(FromComponent=turboMeshComponent1, TransferName=None, ToComponentTemplate=componentTemplate1)],RelativeTo=system2)
setup1 = system3.GetContainer(ComponentName="Setup")

setup1.Import(FilePath="{CFXpre_path}")

setup1.SendCommand(Command=\"\"\"LIBRARY: 
&replace   MATERIAL: fluid
    Material Group = User
    Object Origin = User
    Option = Pure Substance
    Thermodynamic State = Gas
    PROPERTIES: 
      Component Name = {fluid_name}
      Option = Table
      Table Format = TASCflow RGP
      Table Name = {RGP_path}
    END # PROPERTIES:
  END # MATERIAL:fluid
END # LIBRARY:
PARAMETERIZATION:
END\"\"\")

setup1.SendCommand(Command=\"\"\"
> update
LIBRARY: 
CEL: 
    EXPRESSIONS: 
    global size factor = 0.67
    tip clearance = 5E-05 [m]
    count = if(ctstep <10 , 0, flag instantaneous convergence*(ave(count old)@Inducer Inlet + flag instantaneous convergence))
    efficiency = ave(Isentropic Compression Efficiency)@Diffuser Outlet
    efficiency prev = ave(efficiency old)@Inducer Inlet
    efficiency prev1 = ave(efficiency old1)@Inducer Inlet
    efficiency prev2 = ave(efficiency old2)@Inducer Inlet
    efficiency prev3 = ave(efficiency old3)@Inducer Inlet
    flag instantaneous convergence = if(moving window mean amplitude efficiency < 0.0001,1,0)
    mass flow = 0.025 [kg s^-1]
    mfr in = abs(massFlow()@Inducer Inlet)
    mfr out = abs(massFlow()@Diffuser Outlet)
    mfr ratio = mfr out/mfr in
    moving window mean amplitude efficiency = (abs(moving window mean efficiency - efficiency) + abs(moving window mean efficiency - efficiency prev) + abs(moving window mean efficiency - efficiency prev1) + abs(moving window mean efficiency - efficiency prev2) + abs(moving window mean efficiency - efficiency prev3))
    moving window mean efficiency = (efficiency + efficiency prev + efficiency prev1 +efficiency prev2 + efficiency prev3)/5
    n channels = {n_channels}
    n max iterations = 2
    old pressure ratio = 1
    pressure ratio = (massFlowAve(Total Pressure)@Diffuser Outlet+reference pressure)/(massFlowAve(Total Pressure)@Inducer Inlet+reference pressure)
    pressure ratio prev = ave(pressure ratio old)@Inducer Inlet
    pressure ratio prev1 = ave(pressure ratio old1)@Inducer Inlet
    pressure ratio prev2 = ave(pressure ratio old2)@Inducer Inlet
    pressure ratio prev3 = ave(pressure ratio old3)@Inducer Inlet
    reference pressure = total inlet pressure
    residual target = 1E-05
    rotational speed = 12566.4 [radian s^-1]
    roughness = 1E-05 [m]
    total inlet pressure = 200001 [Pa]
    total inlet temperature = 273 [K]
    END
END
END
> update\"\"\")

parameter3 = Parameters.GetParameter(Name="P3")
designPoint1.SetParameterExpression(
    Parameter=parameter3,
    Expression="{mass_flow} [kg s^-1]")
parameter4 = Parameters.GetParameter(Name="P4")
designPoint1.SetParameterExpression(
    Parameter=parameter4,
    Expression="{n_iterations}")

parameter5 = Parameters.GetParameter(Name="P5")
designPoint1.SetParameterExpression(
    Parameter=parameter5,
    Expression="{target_residual}")
parameter6 = Parameters.GetParameter(Name="P6")
designPoint1.SetParameterExpression(
    Parameter=parameter6,
    Expression="{Nrot} [rev min^-1]")

parameter7 = Parameters.GetParameter(Name="P7")
designPoint1.SetParameterExpression(
    Parameter=parameter7,
    Expression="{roughness} [micron]")
parameter8 = Parameters.GetParameter(Name="P8")
designPoint1.SetParameterExpression(
    Parameter=parameter8,
    Expression="{Pin} [Pa]")

parameter9 = Parameters.GetParameter(Name="P9")
designPoint1.SetParameterExpression(
    Parameter=parameter9,
    Expression="{Tin} [K]")

########################################################################################### CFXsolver SCRIPTING

# SETTING UP CFXsolver

system4 = GetSystem(Name="CFX")
solution1 = system4.GetContainer(ComponentName="Solution")

solutionSettings1 = solution1.GetSolutionSettings()
solutionSettings1.UpdateOption = "RemoteSolveManager"
solutionSettings1.ConfiguredQueue = "{queue_name}"
solutionSettings1.ExecutionMode = "Parallel"
solutionSettings1.NumberOfProcesses = {n_partitions}

# SENDING COMMANDS TO CFXsolver

solution1.SetExecutionControl(CCL=r\"\"\"&replace SIMULATION CONTROL:
EXECUTION CONTROL:
    EXECUTABLE SELECTION:
    Double Precision = Off
    Large Problem = Off
    END
    INTERPOLATOR STEP CONTROL:
    Runtime Priority = Standard
    MEMORY CONTROL:
        Memory Allocation Factor = 1.0
        Option = Model Based
    END
    END
    PARTITIONER STEP CONTROL:
    Multidomain Option = Automatic
    Runtime Priority = Standard
    MEMORY CONTROL:
        Memory Allocation Factor = 1.0
        Option = Model Based
    END
    PARTITION SMOOTHING:
        Maximum Partition Smoothing Sweeps = 100
        Option = Smooth
    END
    PARTITIONING TYPE:
        MeTiS Type = k-way
        Option = MeTiS
        Partition Size Rule = Automatic
    END
    END
    RUN DEFINITION:
    Run Mode = Full
    Solver Input File = {CFXdef_path}
    END
    SOLVER STEP CONTROL:
    Runtime Priority = Standard
    MEMORY CONTROL:
        Memory Allocation Factor = 1.0
        Option = Model Based
    END
    PARALLEL ENVIRONMENT:
        Number of Processes = {n_partitions}
        Start Method = Intel MPI Local Parallel
    END
    END
END
END
\"\"\")
Save(FilePath="{workbench_path}",Overwrite=True)
solutionComponent1 = system4.GetComponent(Name="Solution")
solutionComponent1.Update(Force=True)
Save(FilePath="{workbench_path}",Overwrite=True)
solution1.Exit()
    """

    if(simulation_definition["RGP address"] != None):
        RGP_path = simulation_definition["RGP address"]
    else:
        RGP_path = convert_slashes('%s/%s/buffer_files/%s.rgp'%(project_path,case_name,simulation_definition["fluid name"]),'forward')

    # Format the script with the encoding format
    formatted_script = script_template.format(bladegen_path=convert_slashes('%s/%s/buffer_files/geometry.bgd'%(project_path,case_name),'forward'),
                                            workbench_path=convert_slashes('%s/%s/%s.wbpj'%(project_path,case_name,case_name),'forward'),
                                            turbogrid_path=convert_slashes('%s/%s/buffer_files/TURBOgrid_state.tst'%(project_path,case_name),'forward'),
                                            CFXpre_path=convert_slashes('%s/CFXsetup_files/CFXpre_case.cfx'%package_path,'forward'),
                                            CFXdef_path=convert_slashes('%s\%s\%s_files\dp0\CFX\CFX\CFXpre_case.def'%(project_path,case_name,case_name),'backward'),
                                            fluid_name = simulation_definition["fluid name"],
                                            RGP_path=RGP_path,
                                            tip_clearance=simulation_definition["tip clearance"],
                                            n_channels=simulation_definition["n channels"],
                                            Pin=simulation_definition["Pin"],
                                            Tin=simulation_definition["Tin"],
                                            mass_flow=simulation_definition["mass flow"],
                                            Nrot=simulation_definition["rotational speed"],
                                            roughness=simulation_definition["roughness"],
                                            mesh_size_factor=simulation_definition["mesh size factor"],
                                            n_iterations=simulation_definition["n iterations"],
                                            target_residual=simulation_definition["target residual"],
                                            n_partitions=simulation_definition["n partitions"],
                                            queue_name=simulation_definition["queue_name"]
                                            )

    with open('%s\%s\\buffer_files\pipeline.wbjn'%(project_path, case_name), 'w') as file:
        file.write(formatted_script)

def update_TURBOgrid_state(package_path, project_path, case_name):
  #! DEPRECATED (defining TURBOgrid settings directly on WORKbench journal instead of using a TURBOgrid state)

    target_string = ['BG.inf','BG_hub.curve','BG_shroud.curve','BG_profile.curve']
    n_target_string = len(target_string)
    indices = [[] for _ in range(n_target_string)]
    
    with open('%s\CFXsetup_files\TURBOgrid_state.tst'%package_path, 'r') as file_read:
        lines = file_read.readlines()

    with open('%s\%s\\buffer_files\TURBOgrid_state.tst'%(project_path, case_name), 'w') as file:
    
        for i, line in enumerate(lines):
            flag = True
            for j in range(n_target_string):
                if line.strip().endswith(target_string[j]):
                        replacement_string = ' ' + project_path + '\%s\%s_files\dp0\BG\TS'%(case_name,case_name) + '\%s'%target_string[j] + '\n'
                        updated_line = substitute_after_equal(line, replacement_string)
                        file.write(updated_line)
                        flag = False
            if(flag == True):
                file.write(line)

def update_BGD(package_path, project_path, case_name, geometry_type, geometry_name):

    if(geometry_type=="from database"):

        with open('%s\CFXsetup_files\\geometry_turbocompressor_database\%s.bgd'%(package_path, geometry_name), 'r') as file_read:
            lines = file_read.readlines()

        with open('%s\%s\\buffer_files\geometry.bgd'%(project_path, case_name), 'w') as file:
        
            for i, line in enumerate(lines):
                    file.write(line)

def create_RGP(package_path, project_path, case_name, simulation_definition):

    process = subprocess.Popen(['matlab', '-batch', r"cd('%s\CFXsetup_files'); addpath(genpath('C:\Program Files (x86)\REFPROP')); rgpGen('%s\%s\buffer_files','%s',%f,%f,%f,%f,%f,%f,%f,%f,%f); exit"%(package_path, project_path, case_name, simulation_definition["fluid name"], simulation_definition["RGP Pmin"], simulation_definition["RGP Pmax"], simulation_definition["RGP Tmin"], simulation_definition["RGP Tmax"], simulation_definition["RGP Tsatmin"], simulation_definition["RGP Tsatmax"], simulation_definition["RGP nP"], simulation_definition["RGP nT"], simulation_definition["RGP nPsat"])], 
                                stdin=subprocess.PIPE, 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE, 
                                text=True)
    # Wait for the subprocess to finish
    process.wait()
    process.kill()

################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################

def run_CFXbatch(simulation_definition):

    abspath = os.path.abspath(__file__)
    package_path = os.path.dirname(abspath)

    ansys_path = simulation_definition["ansys_path"]
    wb_path = ansys_path + r"\Framework\bin\Win64\runwb2.exe"

    project_path = simulation_definition["project_path"]
    project_path = convert_slashes(project_path,'backward')
    case_name = simulation_definition["case_name"]

    try:    
        os.makedirs(r'%s'%(project_path))
    except Exception:
        fakevar=1

    create_or_overwrite_folder(r'%s\%s'%(project_path,case_name))
    create_or_overwrite_folder(r'%s\%s\buffer_files'%(project_path,case_name))

    update_WORKBENCH_template(package_path, project_path, case_name, simulation_definition)
    update_BGD(package_path, project_path, case_name, simulation_definition["geometry type"], simulation_definition["geometry name"])    
    # update_TURBOgrid_state(package_path, project_path, case_name)

    if(simulation_definition["RGP address"]==None):
        create_RGP(package_path, project_path, case_name, simulation_definition)

    # Open the subprocess to access CFX environment
    process = subprocess.Popen([wb_path, '-B', '-R', '%s\%s\\buffer_files\pipeline.wbjn'%(project_path, case_name)], 
                                stdin=subprocess.PIPE, 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE, 
                                text=True)
    # Wait for the subprocess to finish
    process.wait()
    process.kill()

################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################

#! DEPRECATED (using separate to setup and launch calculations. see launcher.py as an example)
# simulation_definition = {

#     #! Ansys local address 

#     "ansys_path" : r"C:\Program Files\ANSYS Inc\v241",

#     #! project/case name definition

#     "project_path" : r'C:\Users\soukhman\Desktop\CTC2',
#     "case_name" : 'simulation1',

#     #! geometry definition

#     "geometry type" : "from database", # "from database --> retrieve existing geometry" - "from parametrization --> use Davide's work to generate a geometry"
#     "geometry name" : "CTC2_stage1",
#     "parametrization" : None,

#     "tip clearance" : 50, #[micron]
#     "n channels" : 9,
#     "geom param1" : None,
#     "geom param2" : None,
#     "geom param3" : None,
#     "geom param4" : None,
#     "roughness" : 10, #[micron]

#     #! fluid definition 

#     "fluid name" : "r134a",
#     "RGP address" : None,           # keep None if you want to create an RGP table from scratch
#     "RGP Pmin" : 10000,
#     "RGP Pmax" : 3000000,
#     "RGP Tmin" : 180,
#     "RGP Tmax" : 450,
#     "RGP Tsatmin" : 180,
#     "RGP Tsatmax" : 350,
#     "RGP nP" : 366,                 # number pressure points
#     "RGP nT" : 251,                 # number temperature points
#     "RGP nPsat" : 155,              # number pressure points on saturation line

#     #! operating condition definition

#     "Pin" : 200000, #[Pa]
#     "Tin" : 273, #[K]
#     "mass flow" : 0.03, #[kg s^-1]
#     "rotational speed" : 150000, #[rev min^-1]

#     #! mesh and solver definition 
#     "mesh size factor" : 0.77,
#     "n partitions" : 10,
#     "n iterations" : 200, 
#     "target residual" : 1e-6 
# }

# run_CFXbatch(simulation_definition)
