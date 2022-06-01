#!/bin/bash
#SBATCH --account=bar
#SBATCH --time=2-00:00:00
#SBATCH --job-name=drc_olaf_bd
#SBATCH --nodes=1             # This should be nC/36 (36 cores on eagle)
#SBATCH --ntasks-per-node=36
#SBATCH --mail-user mchetan@nrel.gov
#SBATCH --mail-type BEGIN,END,FAIL
#SBATCH --output=logs/%j.drc_olaf_bd.log
#### ####SBATCH --partition=debug


nDV=2 # Number of design variables (x2 for central difference)
nOF=1  # Number of openfast runs per finite-difference evaluation
nC=$((nDV + nDV * nOF)) # Number of cores needed. Make sure to request an appropriate number of nodes = N / 36
nC=36

module purge
module load conda cmake
module load comp-intel intel-mpi mkl
module unload gcc
module list

source activate /home/mchetan/.conda-envs/weis-env-olaf-04may22
which python

python runBarDRC.py
# python weis_driverumaine_semi.py
