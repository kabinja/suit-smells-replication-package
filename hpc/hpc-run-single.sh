#!/bin/bash -l

#SBATCH -N 1
#SBARCH -m 20
#SBATCH -c 4
#SBATCH -J smells

configuration=$1
java -Xms16g -Xmx16g -jar ./jar/ikora-evolution.jar -config $configuration