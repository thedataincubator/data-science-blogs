import os
import psycopg2


class PostgresTasks(object):

    def __init__(self, csv_file_A, csv_file_B):
        self.csv_file_A = csv_file_A
        self.csv_file_B = csv_file_B

        # get user name for postgres connection
        user = os.popen("echo $USER").read().strip()
        dbname = user

        # create psql connection, cursor, and create test table
        self.conn = psycopg2.connect(dbname=dbname, user=user)
        self.cur = self.conn.cursor()
        self.cur.execute("DROP TABLE IF EXISTS test_table_A;")
        self.cur.execute("DROP TABLE IF EXISTS test_table_B;")

        query_A = """
        CREATE TABLE test_table_A
        (id int, score_1 float, score_2 float, section char(1));
        """

        query_B = """
        CREATE TABLE test_table_B
        (id int, score_3 float);
        """

        self.cur.execute(query_A)
        self.cur.execute(query_B)

        # load csv files to tables
        with open(self.csv_file_A, 'r') as f:
            self.cur.copy_from(f, "test_table_A", sep=',')

        with open(self.csv_file_B, 'r') as f:
            self.cur.copy_from(f, "test_table_B", sep=',')

    def load(self):
        self.cur.execute("DELETE FROM test_table_A;")

        with open(self.csv_file_A, 'r') as f:
            self.cur.copy_from(f, "test_table_A", sep=',')

    def select(self):
        self.cur.execute('SELECT score_1 FROM test_table_A;')

    def filter(self):
        self.cur.execute(
            "SELECT * FROM test_table_A WHERE section = 'A';")

    def groupby_agg(self):
        query = """
        SELECT AVG(score_1), MAX(score_2)
        FROM test_table_A
        GROUP BY section;
        """

        self.cur.execute(query)

    def join(self):
        query = """
        SELECT * FROM test_table_A
        JOIN test_table_B on test_table_A.id = test_table_B.id;
        """

        self.cur.execute(query)

    def get_num_rows(self):
        self.cur.execute("SELECT COUNT(*) FROM test_table;")
        num_rows = self.cur.fetchall()

        return int(num_rows[0][0])

    def clean_up(self):
        self.cur.execute("DROP TABLE IF EXISTS test_table_A;")
        self.cur.execute("DROP TABLE IF EXISTS test_table_B;")
        self.conn.commit()
        self.conn.close()
