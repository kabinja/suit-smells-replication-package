#!/bin/bash -l

#SBATCH -n 1
#SBATCH -N 1
#SBATCH -c 4
#SBATCH -J smells

configuration=$1
java -jar ./jar/ikora-evolution.jar -config $configuration