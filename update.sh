#!/usr/bin/env bash
# Run this script in base image:
# $ docker run -itv $PWD:/root -w /root --platform linux/amd64 continuumio/miniconda3:24.11.1-0
eval "$(conda shell.bash hook)"
conda env create -f update.yaml
conda activate nsforest
conda env export | grep -v prefix > environment.yaml
conda deactivate
conda env remove -n nsforest
