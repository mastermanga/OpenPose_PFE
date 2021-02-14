#!/bin/bash

input_directory=$1
output_dir=$2

for file in $input_directory/*
do
    ./full_analysis.sh $file $output_dir

done

echo $output_dir