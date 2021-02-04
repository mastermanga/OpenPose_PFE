#!/bin/bash

echo "Please specify videos folder directory >"
read input_directory
echo "Please specify output directory >" 
read output_dir

for file in $input_directory/*
do
    ./full_analysis.sh $file $output_dir

done

echo $output_dir