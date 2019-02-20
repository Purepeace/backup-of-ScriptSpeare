#!/usr/bin/env bash
set -e

#usage:
#0) assume there are only .mp4 video files and only one masterscript (.txt file) per play
#1) place python parsers in same dir as processor and place every in directory of a play
#2) run command:"chmod u+x processor.#!/bin/sh
#3) ./processor.sh "gentle's url (short version)"

url=$1

audios=($(ls *.mp4))
script=$(ls *.txt)
preParsedFile=$(python3 preParser.py $script)

for a in "${audios[@]}"
do
  :
  echo Gentle is processing: $a
  curl -F "audio=@$a" -F "transcript=@$preParsedFile" "http://$url/transcriptions?async=false" > "${a}-FROM-${script}.json"
  python3 auto-adjusment.py "${a}-FROM-${script}.json"
done
