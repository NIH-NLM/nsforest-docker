#!/usr/bin/env bash
docker run -itv $PWD:/root -w /root --platform linux/amd64 $@ \
       continuumio/miniconda3@sha256:166ff37fba6c25fcad8516aa5481a2a8dfde11370f81b245c1e2e8002e68bcce
