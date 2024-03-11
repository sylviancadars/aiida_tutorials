from aiida import load_profile
from aiida.engine import calcfunction

load_profile()

def perturb_and_relax(initial_structure, perturbation_max, perturbation_min):
    pmg_init = initial_structure.get_pymatgen()
    pmg_perturbed = pmg_init.copy()
    pmg_perturbed.perturb(perturbation_max, perturbation_min)
    pmg_relaxed = pmg_perturbed.relax(verbose=True, fmax=0.2, steps=500)

    return('perturbed_structure': )


"""

In [19]: pmg_struct.perturb(0.5, 0.0)

In [20]: pmg_struct_init = load_node(965).get_pymatgen()

In [21]: from pyama.structureComparisonsPkg.distanceTools import distanceMatrixData

In [22]: dmd = distanceMatrixData()

In [23]: dmd.calculate_cosine_distance(pmg_struct_init, pmg_struct)
Out[23]: 0.2909318359227835

In [24]: pmg_struct_perturbed = pmg_struct_init.copy()

In [25]: pmg_struct_perturbed.perturb(1.0, 0.5)

In [26]: dmd.calculate_cosine_distance(pmg_struct_init, pmg_struct_perturbed)
Out[26]: 0.3902138396694068

In [27]: pmg_struct_perturbed_relax = pmg_struct_perturbed.copy()

In [28]: pmg_struct_perturbed_relax.relax()

