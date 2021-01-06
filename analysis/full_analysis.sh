#!/bin/bash

echo "Please specify input name"
read input_img
echo "Please specify output directory" 
read output_dir


## 1- Launch tracking

python tracking.py 

echo "Tracking completed" 

## 2- Launch Openpose analysis

python analysis_image.py --image $input_img --output $output_dir

echo "Openpose analysis completed"

## 3- Launch Grid analysis 

python grid.py "${output_dir}/Gardien_OpenPose_Color.png" "${output_dir}/Gardien_OpenPose_Color_final.png"


echo Analysis completed, please refer to $output_dir directory for results

