#!/bin/bash

echo "Please specify video path >"
read input_vid
echo "Please specify output directory >" 
read output_dir

video_file=`basename "$input_vid"`
video_name="${video_file%.*}"

## 1- Launch tracking

python track.py --video $input_vid --output $output_dir

echo "Tracking completed" 

## 2- Launch Openpose analysis

input_opp="${output_dir}/${video_name}_tra.png"

echo $input_opp

python analysis_image.py --image $input_opp --output $output_dir

echo "Openpose analysis completed"

## 3- Launch Grid analysis 

input_grid="${output_dir}/${video_name}_tra_opp.png"

echo $input_grid

python grid.py --image $input_grid --output $output_dir

echo Analysis completed, please refer to $output_dir directory for results

