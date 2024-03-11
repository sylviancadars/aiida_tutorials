
from aiida.engine import run
from aiida.orm import (load_code, Dict, StructureData)
from aiida import load_profile

from ase.io import read

from aiida_user_utils.common import get_computer_options

load_profile()

cp2k_code = load_code('cp2k-6.1@curta')

# Structure
structure = StructureData(ase=read('inputs/initial_config.extxyz'))

cp2k_data_folder = '/gpfs/home/ircer/CP2K/cp2k-6.1/data'
# TODO: Try to set data folder from executable ? Difficult to make it robust...

# Parameters
parameters = Dict(
    dict={
           "GLOBAL": {
               # "PROJECT_NAME": "SiCN",  AIIDA AUTOMATICALLY ADDS A "PROJECT"
               # KEYWORD (REDUNDANCY CAUSES FAILURE)
               "PRINT_LEVEL": "LOW",
               "RUN_TYPE": "MD",
               "WALLTIME": "00:05:00",
           },
           "FORCE_EVAL": {
               "PRINT": {
                   "STRESS_TENSOR": {
                       "_": "ON",
                   },
               },
               "DFT": {
                   "MGRID": {
                       "CUTOFF": 400.0,
                       "REL_CUTOFF": 50.0,
                   },
                   "QS": {
                       "EPS_DEFAULT": 1e-12,
                       "EXTRAPOLATION": "ASPC",
                       "EXTRAPOLATION_ORDER": 0,
                       "METHOD": "GPW",
                   },
                   "SCF": {
                       "DIAGONALIZATION": {
                           "_": False,
                       },
                       "MIXING": {
                           "ALPHA": 0.3,
                           "METHOD": "BROYDEN_MIXING",
                           "NBUFFER": 8,
                       },
                       "OT": {
                           "_": True,
                           "MINIMIZER": "CG",
                           "LINESEARCH": "3PNT",
                           "PRECONDITIONER": "FULL_SINGLE_INVERSE",
                           "ENERGY_GAP": 0.01,
                           "STEPSIZE": 0.03,
                       },
                       "OUTER_SCF": {
                           "MAX_SCF": 30,
                           "EPS_SCF": 1e-06,
                       },
                       "PRINT": {
                           "RESTART": {
                               "EACH": {
                                   "QS_SCF": 30,
                               },
                               "BACKUP_COPIES": 2,
                           },
                           "RESTART_HISTORY": {
                               "BACKUP_COPIES": 2,
                           },
                       },
                       "SCF_GUESS": "RESTART",
                       "EPS_SCF": 1e-06,
                       "MAX_SCF": 30,
                       "MAX_SCF_HISTORY": 2,
                   },
                   "XC": {
                       "XC_FUNCTIONAL": {
                           "PBE": {
                           },
                       },
                   },
                   "PRINT": {
                   },
                   "BASIS_SET_FILE_NAME": [
                       "{}/GTH_BASIS_SETS".format(cp2k_data_folder),
                       "{}/BASIS_MOLOPT_UCL".format(cp2k_data_folder),
                   ],
                   "POTENTIAL_FILE_NAME": "{}/GTH_POTENTIALS".format(cp2k_data_folder),
               },
               "SUBSYS": {
                   "PRINT": {
                       "ATOMIC_COORDINATES": {
                           "_": "ON",
                       },
                   },
                   "KIND": [
                       {
                       "_": "Si",
                       "BASIS_SET": "DZVP-GTH-q4",
                       "POTENTIAL": "GTH-PBE-q4",
                       },
                       {
                       "_": "C",
                       "BASIS_SET": "DZVP-GTH-q4",
                       "POTENTIAL": "GTH-PBE-q4",
                       },
                       {
                       "_": "N",
                       "BASIS_SET": "DZVP-GTH-q5",
                       "POTENTIAL": "GTH-PBE-q5",
                       },
                       {
                       "_": "H",
                       "BASIS_SET": "DZVP-GTH-q1",
                       "POTENTIAL": "GTH-PBE-q1",
                       },
                   ],
               },
               "METHOD": "QS",
               "STRESS_TENSOR": "ANALYTICAL",
           },
           "MOTION": {
               "MD": {
                   "LANGEVIN": {
                       "GAMMA": 0.1,
                       "NOISY_GAMMA": 0.03,
                   },
                   "ENSEMBLE": "LANGEVIN",
                   "TEMPERATURE": 300.0,
                   "TIMESTEP": 2.0,
                   "STEPS": 7500,
               },
               "PRINT": {
                   "TRAJECTORY": {
                       "EACH": {
                           "MD": 1,
                       },
                   },
                   "STRESS": {
                       "_": "ON",
                       "EACH": {
                           "MD": 1,
                       },
                       "FILENAME": "pressure",
                   },
                   "VELOCITIES": {
                       "_": "OFF",
                   },
                   "FORCES": {
                       "_": "OFF",
                   },
                   "RESTART_HISTORY": {
                       "EACH": {
                           "MD": 1000,
                       },
                   },
                   "RESTART": {
                       "EACH": {
                           "MD": 1,
                       },
                       "BACKUP_COPIES": 2,
                   },
               },
           },
    })

# Construct process builder.
builder = cp2k_code.get_builder()
builder.structure = structure
builder.parameters = parameters
builder.code = cp2k_code
# Loadding options from aiida_user_utils.common.get_computer_options() function
builder.metadata.options = get_computer_options(cp2k_code.computer.label,
                                                return_attributedict=True,
                                                test_mode=True)
builder.metadata.options.max_wallclock_seconds = 1 * 60 * 60
"""
builder.metadata.options.resources = {
    "num_machines": 1,
    "num_mpiprocs_per_machine": 4,
}
builder.metadata.options.max_wallclock_seconds = 1 * 3 * 60
builder.metadata.options.qos = 'qos_cpu-dev'
builder.metadata.options.account = 'zqm@cpu'
builder.metadata.options.custom_scheduler_commands = (
    '#SBATCH --hint=nomultithread\n'
    '#SBATCH --cpus-per-task=1')
"""

print('Ready to run {} calculation with builder = {}'.format(cp2k_code, builder))
run(builder)

