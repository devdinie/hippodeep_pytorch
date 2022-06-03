#!/bin/bash

source /scratch/swapna/mamba-forge/bin/activate Uvenv2;
mkdir logs/proctimes

for file in  MAGeT_testData/* ; 
do
	start_time=$(date +%s.%3N) ;
	IFS='_' read -ra subject_id <<< "$(basename $file)"
	bash deepseg1.sh $file ;
	end_time=$(date +%s.%3N);
	elapsed=$(echo "scale=3; $end_time - $start_time" | bc)
	printf "Elapsed time: $elapsed ms\nStart time: $start_time ms\nEnd time: $end_time ms\n" > logs/proctimes/proctime_$subject_id.txt 
done
