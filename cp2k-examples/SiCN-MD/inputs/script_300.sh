#!/bin/bash
#SBATCH --job-name SGCPMD_300K
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=40
#SBATCH --time=01:45:00
#SBATCH -A zqm@cpu
#SBATCH --hint=nomultithread
#SBATCH --output=log
#SBATCH --error=log
#SBATCH --partition=prepost

env
cd $PWD
ulimit -s unlimited

module load intel-compilers/19.0.4
module load intel-mpi/19.0.4 
module load cp2k/6.1-mpi-popt

srun cp2k.popt -i input_300K.in -o output_300K_CPMD.out3
