# pandas vs. PostgreSQL
A benchmark comparing pandas and PostgreSQL for various table sizes and commands.

## Getting Started
To start the benchmark, run `run_script.sh`. The number of test replicates and size of the table/DataFrame can be adjusted in `run_script.sh`. The table/DataFrame are created from csv files. If these csv files do not exist, `run_script.sh` creates them by calling on `create_dataset.py`.

### Prerequisites
Apart from having pandas and Postgre installed, you need the following Python packages.

```
contexttimer
numpy
psycopg2
```

### The Benchmark
The benchmark is performed for following tasks: load csv, select column, filter, and group by and applying aggregate function. The results are stored as a separate JSON files for pandas and Postgre. The JSON file contains the results for each task and for each table size. A write-up of the results are found in the `analysis_writeup.ipynb` notebook.