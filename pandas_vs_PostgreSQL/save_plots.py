from collections import OrderedDict
import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def calc_stats(data_dict):
    num_rows = [int(x) for x in data_dict.keys()]
    num_rows.sort()

    tasks = data_dict.values()[0].keys()
    task_stats = {}

    for task in tasks:
        stats = OrderedDict()

        for row in num_rows:
            stats[row] = np.array(data_dict[str(row)][task]).mean()

        task_stats[task] = stats

    return task_stats

if __name__ == '__main__':

    # load results
    with open('results/pandas_benchmark.json', 'r') as f:
        pandas_results = json.load(f)

    with open('results/postgre_benchmark.json', 'r') as f:
        postgre_results = json.load(f)

    pandas_task_stats = calc_stats(pandas_results)
    postgre_task_stats = calc_stats(postgre_results)
    title_labels = dict(
        zip(['load', 'select', 'filter', 'groupby_agg', 'join'],
            ['Load', 'Select', 'Filter', 'Group By and Aggregate', 'Join']))

    for task in pandas_task_stats.keys():
        x_pandas = pandas_task_stats[task].keys()
        y_pandas = pandas_task_stats[task].values()

        x_postgre = postgre_task_stats[task].keys()
        y_postgre = postgre_task_stats[task].values()

        f = plt.figure()
        plt.loglog(
            x_pandas, y_pandas, marker='o', markersize=8, linestyle='--',
            linewidth=2)
        plt.loglog(
            x_postgre, y_postgre, marker='s', markersize=8, linestyle='--',
            linewidth=2)

        plt.xlabel('Number of Rows (-)', fontsize=16)
        plt.xticks(fontsize=16)
        plt.ylabel('Mean Execution Time (seconds)', fontsize=16)
        plt.yticks(fontsize=16)
        plt.title(title_labels[task], fontsize=16)
        plt.legend(['pandas', 'Postgre'], loc='upper left', fontsize=16)
        plt.tight_layout()
        f.savefig('figures/' + task + '_results_plot.png', dpi=300)
