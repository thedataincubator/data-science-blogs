import pandas as pd


class PandasTasks(object):

    def __init__(self, csv_file_A, csv_file_B):
        self.csv_file_A = csv_file_A
        self.csv_file_B = csv_file_B
        self.columns_A = ('id', 'score_1', 'score_2', 'section')
        self.columns_B = ('id', 'score_3')

        self.df_A = pd.read_csv(csv_file_A, header=None, index_col=False,
                                names=self.columns_A)
        self.df_B = pd.read_csv(csv_file_B, header=None, index_col=False,
                                names=self.columns_B)

    def load(self):
        self.df_A = pd.read_csv(self.csv_file_A, header=None, index_col=False,
                                names=self.columns_A)

    def select(self):
        self.df_A['score_1']

    def filter(self):
        self.df_A[self.df_A['section'] == 'A']

    def groupby_agg(self):
        self.df_A.groupby('section').agg({'score_1': 'mean', 'score_2': 'max'})

    def join(self):
        self.df_A.merge(self.df_B, left_on='id', right_on='id')

    def get_num_rows(self):
        return len(self.df_A)

    def clean_up(self):
        del(self.df_A)
        del(self.df_B)
