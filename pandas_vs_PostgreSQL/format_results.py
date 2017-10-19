def create_dict(results_file):
    """Return dictionary of run time for each SQL task."""
    tasks = ('load', 'select', 'filter', 'groupby_agg')
    results_dict = {}

    with open(results_file, 'r') as f:
        task = f.readline().strip()
        results = f.read().split()
        replicates = []

        for r in results:
            if r in tasks:
                results_dict[task] = replicates
                task = r
                replicates = []
            else:
                replicates.append(float(r) / 1E9)

        results_dict[task] = replicates

    return results_dict

if __name__ == '__main__':
    import json
    import os
    import re

    full_results_dict = {}
    dir = 'parts/'
    results_files = os.listdir(dir)
    pattern = re.compile(r'\d+')

    # loop through each part file
    for f in results_files:
        row_num = pattern.findall(f)[0]
        full_results_dict[row_num] = create_dict(dir + f)

    # dump to json
    with open("results/postgre_direct_benchmark.json", "w") as f:
        json.dump(full_results_dict, f)
