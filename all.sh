#!/bin/bash

if [ $# -lt 1 ]; then
  echo "[ERROR]need comment to commit"
  exit -1
fi

bash build.sh && bash deploy.sh $1 && bash push2source.sh $1

