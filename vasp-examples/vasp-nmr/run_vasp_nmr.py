"""
NMR calculation using aiida-vasp

This function uses the aiida_user_utils.vasp module build_and_submit_nmr(),
which uses a number of helper functions within this or the
aiida_user_utils.common module to automatize the NMR calculations.

This includes among other things:
    - automatic selection of computer options for jean-zay.idris.fr or  or
    curta.mcia.fr through aiida_user_utils.common.get_computer_options()
    - choice of pseudopotentials based on pymatgen NMRSet
    - choice of the number of processors
    - automatic choice of cutoff energy based on values recommended within
    pseudo definitions

"""


import aiida_user_utils.common as auuc
import aiida_user_utils.vasp as vasp
from aiida import load_profile
from aiida.orm import StructureData
from pymatgen.core.structure import Structure

load_profile()

def get_structure_from_mp_rester(mp_id):
    mprester = auuc.get_mprester()
    structure = StructureData(pymatgen=mprester.get_structure_by_material_id(mp_id))
    structure.description = '{} structure loaded from materials project database with id {}'.format(
        structure.get_pymatgen().composition.reduced_formula, mp_id)
    return structure

def get_structure_from_cif_file(structure_file):
    structure = StructureData(pymatgen=Structure.from_file(structure_file))
    # add structure description
    return structure

# ********** USER PARAMETERS *****************
nb_of_nodes = 1  # Use 2 for 40-50 atom SiCN models
test_mode = True  # Use False for 40-50 atom SiCN models
max_nb_of_tasks_per_node = 20  # 20 for Si. None for larger systems
# The actual number of requested processors will be adapted to optimize the
# number of bands.
verbosity = 2
# ********************************************

# Different structures and loading methods:
structure = get_structure_from_cif_file('../../structure-files/Si_mp-109.cif')
# structure = get_structure_from_cif_file('../../structure-files/Mg2SiO4_mp-2895.cif')
# structure = get_structure_from_mp_rester('mp-546794')  #  SiO2 mp-546794, sapce group I-42d
# structure = get_structure_from_mp_rester('mp-2895')  # Mg2SiO4, 28 atoms
# structure = aiida.orm.utils.load_node(INSERT_NODE_PK_OR_UUID)  # get from database

process_node = vasp.build_and_submit_nmr(structure, code='vasp-5.4.4@jean-zay',
                                         account='zqm@cpu', test_mode=test_mode,
                                         nb_of_nodes=nb_of_nodes,
                                         max_nb_of_tasks_per_node=max_nb_of_tasks_per_node,
                                         verbosity=verbosity)

