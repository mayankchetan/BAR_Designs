#!/bin/bash
#SBATCH --account=bar
#SBATCH --time=01:00:00
#SBATCH --job-name=speedTest
#SBATCH --nodes=1             # This should be nC/36 (36 cores on eagle)
#SBATCH --ntasks-per-node=36
#SBATCH --mail-user mchetan@nrel.gov
#SBATCH --mail-type BEGIN,END,FAIL
#SBATCH --output=speedLogs/%j.speedTest.log
#SBATCH --partition=debug


nDV=2 # Number of design variables (x2 for central difference)
nOF=1  # Number of openfast runs per finite-difference evaluation
nC=$((nDV + nDV * nOF)) # Number of cores needed. Make sure to request an appropriate number of nodes = N / 36
nC=36

module purge
module load conda cmake
module load comp-intel intel-mpi mkl
module unload gcc
module list

source activate /projects/bar/mchetan/speedTest/weisRel
which python

time python runBarURC_args.py --startW 5 --endW 15 --numCores 20 &

free -m -s 30