#!/bin/bash
##Name
#SBATCH --job-name=atm_run5b
## Allocation Definition
## On mox and ikt, the account and partition options should be the same.
#SBATCH --account=astro
#SBATCH --partition=astro
## Resources
## Nodes
#SBATCH --nodes=1   
## Walltime. Do not specify a walltime substantially more than your job needs.
#SBATCH --time=168:00:00
## Memory per node. It is important to specify the memory since the default memory is very small.
## For mox, --mem may be more than 100G depending on the memory of your nodes.
## For ikt, --mem may be 58G or more depending on the memory of your nodes.
## See above section on "Specifying memory" for choices for --mem.
#SBATCH --mem=250G
##turn on e-mail notification
#SBATCH --mail-type=ALL
#SBATCH --mail-user=moeyensj@uw.edu
## export all your environment variables to the batch job session
#SBATCH --export=all
#SBATCH --open-mode=append

cd /gscratch/astro/moeyensj/atm/atm_data/paper1/runs/sigma10
source ~/.bashrc
conda info -a
conda activate atm_run5b
python runMultiFit_run5b.py
