import numpy as np
import pandas as pd


def create_csv(n=1000):
    seed = np.random.seed(1)

    # generate random dataset
    columns = ('id', 'section', 'score_1', 'score_2')
    labels = ('A', 'B', 'C', 'D')

    id = np.random.choice(range(n), n, replace=False)
    section = np.random.choice(labels, n)
    score_1 = np.random.rand(n)
    score_2 = np.random.rand(n)
    score_3 = np.random.rand(n)

    # create and dump DataFrame to csv
    df_A = pd.DataFrame(dict(zip(columns, (id, section, score_1, score_2))))
    df_B = pd.DataFrame(dict(zip(('id', 'score_3'), (id, score_3))))
    df_A.to_csv('csv/A/test_A_' + str(n) +
                '_rows.csv', index=False, header=False)
    df_B.to_csv('csv/B/test_B_' + str(n) +
                '_rows.csv', index=False, header=False)

if __name__ == '__main__':
    import sys

    create_csv(int(sys.argv[1]))
