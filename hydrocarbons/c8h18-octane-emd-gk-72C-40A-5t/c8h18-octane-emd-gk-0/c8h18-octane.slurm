#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --cluster=smp
#SBATCH --time=6-0
#SBATCH --qos=long
#SBATCH --job-name=c8h18-octane-emd-gk.lammps-0-40A
#SBATCH --output=lammps-stdout.log

# Load Modules
module load intel/2017.1.132 intel-mpi/2017.1.132

# Copy everything to scratch
mkdir -p $SLURM_SUBMIT_DIR/output
shopt -s nullglob # Sets nullglob
inputs=$(ls *.{lammps,restart,data})
shopt -u nullglob # unsets nullglob
for i in ${inputs[@]}; do
    sbcast $SLURM_SUBMIT_DIR/$i $SLURM_SCRATCH/$i
done

# The ulimit
ulimit -s unlimited

cd $SLURM_SCRATCH

run_on_exit(){
    cp -pR $SLURM_SCRATCH/* $SLURM_SUBMIT_DIR/output
}
trap run_on_exit EXIT

srun --mpi=pmi2 ~/workspace/lammps-hf-h2p/src/lmp_mpi -in octane.lammps
