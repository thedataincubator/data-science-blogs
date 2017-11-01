#!/bin/bash

# create directories
for dir in csv csv/A csv/B results; do
    if [ ! -d $dir ]; then
	mkdir $dir
    fi
done

# create test csv files
for n in 10 100 1000 10000 100000 1000000 10000000; do
    file_A="csv/A/test_A_"$n"_rows.csv"
    file_B="csv/B/test_B_"$n"_rows.csv"
    
    if [ ! -f $file_A ] || [ ! -f $file_B ]; then
	echo "creating $n row dataset"
	python create_dataset.py $n 
    fi
done

# run pandas benchmark
num_replicates=100
python benchmark_test.py psycopg2 $num_replicates
python benchmark_test.py pandas $num_replicates
./pgbench_queries.sh $num_replicates
