#!/bin/bash -l

#SBATCH -N 1
#SBARCH -m 12
#SBATCH -c 4
#SBATCH -J smells

configuration=$1
java -Xms8g -Xmx8g -jar ./jar/ikora-evolution.jar -config $configuration