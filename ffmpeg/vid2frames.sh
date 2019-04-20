#!/bin/bash

if [ "$1" == "-h" ]; then
  echo "Usage: `basename $0` [directory] [extension]. Extracts frames from videos."
  echo "Folder structure: dir/vid1.ext, dir/vid2.ext, ..."
  echo "extracts to frames/dir/vid1/vid1_001.jpg .. vid1_xxx.jpg, frames/dir/vid2/vid2_001.jpg"
  echo "also applies yadif filter (deinterlacing)"
  echo "example usage : vid2frame.sh Cats mpeg"
  exit 0
fi


if [ "$#" -ne 2 ]; then
    echo 'specify dir and extension. Try -h'
    exit 0
fi

dir=$1
files="$1/*.$2"
for file in $files
do
    filename=${file##*/}
    filename=${filename%.m2ts}

    mkdir -p frames/$dir/$filename
    # yadif if for deinterlacing
    ffmpeg -i $file -vf "yadif=1" -r 1/1 frames/$dir/$filename/$filename"_"%03d.jpg
done