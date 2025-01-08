#!/usr/bin/env bash
# Run this script in base image:
# $ docker run -itv $PWD:/root -w /root --platform linux/amd64 continuumio/miniconda3@sha256:166ff37fba6c25fcad8516aa5481a2a8dfde11370f81b245c1e2e8002e68bcce
eval "$(conda shell.bash hook)"
conda env create -f update.yaml
conda activate nsforest
conda env export | grep -v prefix > environment.yaml
conda deactivate
conda env remove -n nsforest
