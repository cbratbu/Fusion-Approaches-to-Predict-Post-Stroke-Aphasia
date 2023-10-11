#!/bin/bash -l

# Set SCC project
$ -P projectnb/skiran/saurav/Fall-2022/src2/

# Request 28 CPUs
#$ -pe omp 28
#$ -l mem_per_core=1.2G

#$ -l h_rt=70:00:00
#$ -m beas

#$ -M saurav07@bu.edu

module load python3/3.8.10
module load pytorch/1.11.0

/projectnb/skiran/saurav/Fall-2022/src2/experiment_scripts/EXP-final-RF-normal/runSeperate_11.sh
