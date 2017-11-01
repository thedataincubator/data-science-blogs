import json
import os
import re
import sys

csv_files = os.listdir('csv/A/')
log_files = os.listdir('log/')

num_rows = [re.findall(r'\d+', f)[0] for f in csv_files]
results = {}

# loop through each number of rows, loading the appropriate log files for each
# task. The 3rd column of each line of the file is the execution time, in
# milliseconds.

for n in num_rows:
    S = '_' + n + '.log'
    results_for_row = {}

    for f in [log for log in log_files if S in log]:
        task = re.findall(r'(_\w+_)', f)[0][1:-1]
        time = []

        with open('log/' + f, 'r') as file:
            for line in file:
                time.append(float(line.split(" ")[2]) / 1E6)

        results_for_row[task] = time

    results[n] = results_for_row

# dump results to JSON
with open('results/postgres_benchmark.json', 'w') as f:
    json.dump(results, f)
