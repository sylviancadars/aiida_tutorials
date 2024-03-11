#!/usr/bin/env runaiida
# -*- coding: utf-8 -*-
"""
Downloaded from aiida-quantumespresso documentation:

https://aiida-quantumespresso.readthedocs.io/en/latest/tutorials/first_pw.html#running-a-pw-x-calculation-through-the-api

"""

from aiida.engine import run
from aiida.orm import Dict, KpointsData, StructureData, load_code, load_group
from ase.build import bulk
from ase.io import read
from pymatgen.core.structure import Structure
import os

def get_predefined_structure(structure_name='Si_fcc', verbosity=1):
    """ pick among a list of simple predefined structures """
    if 'si_fcc' in structure_name.lower() or 'silicon' in structure_name.lower():
        structure = StructureData(ase=bulk('Si', 'fcc', 5.43))
        # TODO: Add other structures here
    if 'c_fcc' in structure_name.lower() or 'diamond' in structure_name.lower():
        structure = StructureData(ase=bulk('C', 'fcc', 3.567))
    else:
        raise ValueError('No mathing predefined structure', verbosity=1)

    if verbosity >= 1:
        print('Predefined structure {} of composition {}'.format(structure,
                                                                 structure.get_formula()))
    return structure


def get_structure_from_file(file_name, reader='ase', verbosity=1):
    """
    Load structure from a file using ASE or pymatgen
    """
    if 'pymatgen' in reader.lower() or 'pmg' in reader.lower():
        structure = StructureData(Structure.from_file(filename=file_name))
    else:
        structure = StructureData(ase=read(file_name))

    if verbosity >= 1:
        print('Structure {} of composition {} obtained from file {}'.format(
            structure, structure.get_formula(), os.path.abspath(file_name)))
    return structure


# Load the code configured for ``pw.x``. Make sure to replace this string
# with the label of a ``Code`` that you configured in your profile.
code = load_code('qe-6.5-pw@jean-zay')
builder = code.get_builder()

# Create a structure
# structure = get_predefined_structure('Si_fcc')
structure = get_structure_from_file('../structure-files/TeO2-alpha_P41212_1968_COD-1537586.cif')
# structure = get_structure_from_file('../structure-files/LaB6_Pm-3m_1986_icsd-612685.cif')

builder.structure = structure

# Load the pseudopotential family.
pseudo_family = load_group('SSSP/1.3/PBE/efficiency')
builder.pseudos = pseudo_family.get_pseudos(structure=structure)

# Request the recommended wavefunction and charge density cutoffs
# for the given structure and energy units.
cutoff_wfc, cutoff_rho = pseudo_family.get_recommended_cutoffs(
    structure=structure,
    unit='Ry'
)

parameters = Dict({
    'CONTROL': {
        'calculation': 'scf'
    },
    'SYSTEM': {
        'ecutwfc': cutoff_wfc,
        'ecutrho': cutoff_rho,
    }
})
builder.parameters = parameters

# Generate a 2x2x2 Monkhorst-Pack mesh
kpoints = KpointsData()
kpoints.set_kpoints_mesh([2, 2, 2])
# TODO: set k-points from density

builder.kpoints = kpoints

# Run the calculation on 1 CPU and kill it if it runs longer than 1800 seconds.
# Set ``withmpi`` to ``False`` if ``pw.x`` was compiled without MPI support.
builder.metadata.options = {
    'resources': {
        'num_machines': 1,
        'num_mpiprocs_per_machine': 4,
    },
    'max_wallclock_seconds': 1800,
    'withmpi': True,
    'qos': 'qos_cpu-dev',
    'account': 'zqm@cpu',
    'custom_scheduler_commands': (
        '#SBATCH --hint=nomultithread\n'
        '#SBATCH --cpus-per-task=1')
}

results, node = run.get_node(builder)
print(f'Calculation: {node.process_class}<{node.pk}> {node.process_state.value} [{node.exit_status}]')
print(f'Results: {results}')
assert node.is_finished_ok, f'{node} failed: [{node.exit_status}] {node.exit_message}'


