#!/usr/bin/env bash
docker run -itv $PWD:/root -w /root --platform linux/amd64 $@ \
       continuumio/miniconda3:24.11.1-0
