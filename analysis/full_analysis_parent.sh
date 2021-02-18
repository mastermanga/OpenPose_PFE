#!/bin/bash


input_vid=$1
output_dir=$2

video_file=`basename "$input_vid"`
video_name="${video_file%.*}"

mkdir -p $output_dir

## 1- Launch tracking

python analysis/track.py --video $input_vid --output $output_dir

echo "Tracking completed" 

## 2- Launch Openpose analysis

input_first_opp="${output_dir}/${video_name}_first.png"

input_last_opp="${output_dir}/${video_name}_last.png"

input_white_opp="${output_dir}/${video_name}_white.png"

echo $input_first_opp

python analysis/analysis_image.py --image $input_first_opp --image_last $input_last_opp --image_white $input_white_opp --output $output_dir

echo "Openpose analysis completed"

## 3- Launch Grid analysis 

input_grid="${output_dir}/${video_name}_opp_white.png"

echo $input_grid

python analysis/grid.py --image $input_grid --output $output_dir

echo Analysis completed, please refer to $output_dir directory for results
