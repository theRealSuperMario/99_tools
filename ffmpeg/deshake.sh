#!/bin/bash

if [ "$1" == "-h" ]; then
  echo "Usage: `basename $0` [video]. Stabilizes video"
  exit 0
fi

if [ "$#" -ne 1 ]; then
    echo 'please provide video. Try -h'
    exit 0
fi

input=$1
output="${input%.*}_boomerang.${input##*.}"


ffmpeg -i $input -vf deshake $output