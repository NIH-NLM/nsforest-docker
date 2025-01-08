#!/usr/bin/env bash
docker run -it -w /root --platform linux/amd64 --mount type=bind,source="$(pwd)"/tests,target=/root/tests ralatsdio/nsforest:latest python /root/tests/test.py