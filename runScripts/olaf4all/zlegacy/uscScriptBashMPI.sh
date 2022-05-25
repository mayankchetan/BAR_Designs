#!/bin/bash
#SBATCH --account=bar
#SBATCH --time=00:30:00
#SBATCH --job-name=test_olaf_bd
#SBATCH --nodes=1             # This should be nC/36 (36 cores on eagle)
#SBATCH --ntasks-per-node=36
#SBATCH --mail-user mchetan@nrel.gov
#SBATCH --mail-type BEGIN,END,FAIL
#SBATCH --output=logs/%j.test_olaf_bd.log
#SBATCH --partition=debug


module purge
module load conda cmake
module load comp-intel intel-mpi mkl
module unload gcc
module list

source activate /home/mchetan/.conda-envs/weis-env-09may
which python

for i in *.py; do # Whitespace-safe but not recursive.
    printf "Executing $i\n"
    mpiexec -np 30 /home/mchetan/tools/openfast/ofInstall/may9/bin/openfast "$i"
done

# mpiexec -np 30 python runBarUSC-bd-olaf.py
# # python weis_driverumaine_semi.py
 