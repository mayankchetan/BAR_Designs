"""

Example script to compute the steady-state performance in OpenFAST

"""

import weis
from weis.aeroelasticse.runFAST_pywrapper import runFAST_pywrapper_batch
from weis.aeroelasticse.CaseGen_General import CaseGen_General
from weis.aeroelasticse.openmdao_openfast import OLAFParams
from wisdem.commonse.mpi_tools  import MPI

import numpy as np
import os, platform

try:
    if os.environ['NREL_CLUSTER'] == 'eagle':
        eagleFlag = True
    else:
        eagleFlag = False
except KeyError:
    eagleFlag = False

# Paths calling the standard modules of WEIS
fastBatch = runFAST_pywrapper_batch()
run_dir1                    = os.path.join(os.path.dirname(weis.__file__) + os.sep + '..' + os.sep)
run_dir2                    = os.path.dirname( os.path.realpath(__file__) ) + os.sep

if eagleFlag:
    save_dir                = '/projects/bar/mchetan/projects/downwind/ad15-bd'
else:
    save_dir                = './outputs/ad15-bd'

fastBatch.FAST_directory    = os.path.join(run_dir2,'../../../BAR_URC/' ,'of-olaf') # Path to fst directory files
fastBatch.FAST_InputFile    = 'BAR_URC_out_0.fst'   # FAST input file (ext=.fst)
fastBatch.FAST_runDirectory = os.path.join(save_dir + 'outputs' + os.sep + 'urc')
fastBatch.debug_level       = 2

# User settings
n_cores     = 36     # Number of available cores
TMax        = 720.    # Length of wind grids and OpenFAST simulations, suggested 720 s
runTime     = 600.    # Suggested at 600. s
cut_in      = 3.    # Cut in wind speed
cut_out     = 25.   # Cut out wind speed
n_ws        = cut_out - cut_in + 1    # Number of wind speed bins
wind_speeds = np.linspace(int(cut_in), int(cut_out), int(n_ws)) # Wind speeds to run OpenFAST at
Ttrans      = max([0., TMax - 60.])  # Start of the transient for DLC with a transient, e.g. DLC 1.4
TStart      = max([0., TMax - runTime]) # Start of the recording of the channels of OpenFAST

# Initial conditions for ElastoDyn
u_ref       = np.arange(3.,26.) # Wind speed vector to specify the initial conditions
pitch_ref   = [ 0.   ,  0.   ,  0.   ,  0.   ,  0.   ,  1.301,  3.185,  6.398,
        8.693, 10.58 , 12.33 , 13.9  , 15.37 , 16.81 , 18.12 , 19.41 ,
       20.68 , 21.84 , 23.04 , 24.22 , 25.33 , 26.45 , 27.57 ] # Pitch values in deg
omega_ref   = [2.885, 3.827, 4.749, 5.677, 6.597, 7.425, 7.573, 7.576, 7.567,
       7.576, 7.573, 7.565, 7.581, 7.571, 7.567, 7.586, 7.567, 7.573,
       7.591, 7.563, 7.574, 7.597, 7.564] # Rotor speeds in rpm
pitch_init = np.interp(wind_speeds, u_ref, pitch_ref)
omega_init = np.interp(wind_speeds, u_ref, omega_ref)

adTimeSteps =  5 * 60 / 360 / np.array(omega_init) # Time for 5 degree rotation

# Settings passed to OpenFAST
case_inputs = {}
case_inputs[("Fst","TMax")]             = {'vals':[TMax], 'group':0}
case_inputs[("Fst","DT")]               = {'vals':[0.0002], 'group':0}
case_inputs[("Fst","DT_Out")]           = {'vals':[0.1], 'group':0}
case_inputs[("ServoDyn","DLL_DT")]      = {'vals':[0.01], 'group':0}
case_inputs[("Fst","CompInflow")]       = {'vals':[1], 'group':0}

case_inputs[("Fst","SttsTime")]       = {'vals':[1], 'group':0}
case_inputs[("Fst","TStart")]       = {'vals':[0], 'group':0}

# Below for BeamDyn
case_inputs[("Fst","CompElast")]       = {'vals':[2], 'group':0}

case_inputs[("Fst","CompServo")]        = {'vals':[1], 'group':0}
case_inputs[("Fst","OutFileFmt")]       = {'vals':[1], 'group':0}
case_inputs[("ElastoDyn","GenDOF")]     = {'vals':['True'], 'group':0}
case_inputs[("ServoDyn","PCMode")]      = {'vals':[5], 'group':0}
case_inputs[("ServoDyn","VSContrl")]    = {'vals':[5], 'group':0}

# Below for OLAF
case_inputs[("AeroDyn15","WakeMod")]    = {'vals':[1], 'group':0}
case_inputs[("AeroDyn15","AFAeroMod")]    = {'vals':[1], 'group':0}

# case_inputs[("AeroDyn15","DTAero")]    = {'vals': adTimeSteps, 'group':1}

case_inputs[("InflowWind","WindType")]  = {'vals':[1], 'group':0}
case_inputs[("InflowWind","HWindSpeed")]= {'vals': wind_speeds, 'group': 1}
case_inputs[("InflowWind","RefHt")]       = {'vals':[140], 'group':0}

case_inputs[("Fst","OutFileFmt")]       = {'vals':[3], 'group':0}
case_inputs[("ElastoDyn","RotSpeed")]   = {'vals': omega_init, 'group': 1}
case_inputs[("ElastoDyn","BlPitch1")]   = {'vals': pitch_init, 'group': 1}
case_inputs[("ElastoDyn","BlPitch2")]   = case_inputs[("ElastoDyn","BlPitch1")]
case_inputs[("ElastoDyn","BlPitch3")]   = case_inputs[("ElastoDyn","BlPitch1")]
dt_wanted, tMax, nNWPanel, nFWPanel, nFWPanelFree = OLAFParams(omega_init)
dt_olaf = np.zeros_like(dt_wanted)
dt = case_inputs[("Fst","DT")]["vals"]
n_dt = dt_wanted / dt
dt_olaf = dt * np.around(n_dt)
case_inputs[("AeroDyn15","OLAF","DTfvw")] = {'vals':dt_olaf, 'group':1} 
# case_inputs[("AeroDyn15","OLAF","nNWPanel")] = {'vals':nNWPanel, 'group':1} 
# case_inputs[("AeroDyn15","OLAF","WakeLength")] = {'vals':nFWPanel, 'group':1} 
# case_inputs[("AeroDyn15","OLAF","FreeWakeLength")] = {'vals':nFWPanelFree, 'group':1} 

# Find the controller
if platform.system() == 'Windows':
    path2dll = os.path.join(run_dir1, 'local','lib','libdiscon.dll')
elif platform.system() == 'Darwin':
    path2dll = os.path.join(run_dir1, 'local','lib','libdiscon.dylib')
else:
    path2dll = os.path.join(run_dir1, 'local','lib','libdiscon.so')

case_inputs[("ServoDyn","DLL_FileName")] = {'vals':[path2dll], 'group':0}

# Generate the matrix of cases
case_list, case_name_list = CaseGen_General(case_inputs, dir_matrix=fastBatch.FAST_runDirectory, namebase='bar-urc')

fastBatch.case_list = case_list
fastBatch.case_name_list = case_name_list

# Run OpenFAST, either serially or sequentially
if MPI:
    summary_stats, extreme_table, DELs, Damage, ct = fastBatch.run_mpi()
elif n_cores == 1 and not MPI:
    summary_stats, extreme_table, DELs, Damage, ct = fastBatch.run_serial()
elif not MPI:
    summary_stats, extreme_table, DELs, Damage, ct = fastBatch.run_multi(n_cores)
else:
    raise ValueError('Not running known configs.')