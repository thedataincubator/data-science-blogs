#!/bin/bash
#
# Run PostgreSQL benchmark using pgbench. The only positional parameter is the
# the number of benchmark replicates.

# initialize directories and remove old pgbench_log files
if [ ! -d log ]; then
    mkdir log
fi

if [ -e pgbench_log.* ]; then
    rm pgbench_log*
fi

# loop through all csv files
for file_A in csv/A/*; do
    
    # initialize table and variables
    psql -U $USER -d $USER -f queries/init.sql > /dev/null
    num_rows=$(echo $file_A | grep -oP '\d+')

    # create and run loading csv query files
    file_B="csv/B/test_B_"$num_rows"_rows.csv"
    query_A="COPY test_table_A FROM ""'""$PWD"/"$file_A""'"" WITH DELIMITER ',';"
    query_B="COPY test_table_B FROM ""'""$PWD"/"$file_B""'"" WITH DELIMITER ',';"

    echo "DELETE FROM test_table_A;" > queries/load_all.sql
    echo "DELETE FROM test_table_B;" >> queries/load_all.sql
    echo "$query_A" >> queries/load_all.sql
    echo "$query_B" >> queries/load_all.sql

    echo "DELETE FROM test_table_A;" > queries/load.sql
    echo "$query_A" >> queries/load.sql

    psql -U $USER -d $USER -f queries/load_all.sql > /dev/null
    
    # benchmark each task
    for task in select filter groupby_agg join load; do
	echo "running "$task" for "$num_rows" rows using Postgres"
	pgbench -ln -t $1 -f queries/$task.sql > /dev/null
	mv pgbench_log* log/pgbench_$task"_"$num_rows".log"
    done

   # drop tables
    psql -U $USER -d $USER -f queries/clean_up.sql
done

# format results from logs and clean up		
python create_json.py

if [ -d log ]; then
    rm -rf log 
fi
