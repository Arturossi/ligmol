#!/bin/bash
# 1 noeud 8 coeurs
#SBATCH -p pri2013-short
#SBATCH -A qosisisifm
##SBATCH -p publicgpu
#SBATCH --job-name=BCD-ATN_guest
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 0:30:00

# Configuration
#
# Make sure you load all the necessary modules for your AMBER installation.
# Don't forget the CUDA modules
module load compilers/intel17
module load mpi/openmpi-2.0.i17-omnipath
module load compilers/cuda-9.2

# Path to amber.sh replace with your own
source /workdir/isis/dbarreto/software/amber_publicgpu/amber18/amber.sh 

# Go to folder ( RESP ), guest is either BCD-ATN, BCD, or ATN
INPUT_DIR="../../../../../simulation/bcd/BCD-ATN/resp/guest/"

parmed -O <<EOF
parm       ${INPUT_DIR}/ionized_solvated.prmtop
loadRestrt ${INPUT_DIR}/ionized_solvated.rst7
strip :WAT,Na+,Cl-
parmout complex.prmtop
writeCoordinates complex.rst7
go
quit
EOF

cpptraj <<EOF
parm   ${INPUT_DIR}/ionized_solvated.prmtop
trajin ${INPUT_DIR}/prod.nc
strip :WAT,Na+,Cl-
autoimage familiar
trajout imaged.nc
go
quit
EOF

cpptraj <<EOF
parm complex.prmtop
trajin imaged.nc
reference complex.rst7
rms ref reference ':1 & !@H='
trajout fitted.nc
go
quit
EOF

