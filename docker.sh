#!/bin/bash

image="m1dnight/vub-resto-v2:latest"

# Build
docker build -t "${image}" .

# Push
docker push "${image}"