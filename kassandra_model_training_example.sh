#! /usr/bin/bash

#SBATCH --job-name "kassandra_model_training_TP"
#SBATCH --mem-per-cpu=40G
#SBATCH --cpus-per-task=4
#SBATCH --partition=longq

source LOCATION/OF/CONDA/SOURCE/activate
conda activate kassandra

python3 kassandra_model_training_TP.py