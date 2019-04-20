#!/bin/bash

if [ "$1" == "-h" ]; then
  echo "Usage: `basename $0` [video]. Appends reverse played video to get boomerang effect"
  exit 0
fi

if [ "$#" -ne 1 ]; then
    echo 'please provide video. Try -h'
    exit 0
fi


input=$1
output="${input%.*}_boomerang.${input##*.}"



ffmpeg -i $input -filter_complex "[0:v]reverse,fifo[r];[0:v][r] concat=n=2:v=1 [v]" -map "[v]" $output