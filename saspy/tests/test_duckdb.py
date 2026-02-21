import unittest
import saspy
import pandas as pd
import duckdb
import numpy  as np
import tempfile
import os


TEST_DATA = """
    data testdata;
        format d1 date. dt1 datetime.;

        d1 = '03Jan1966'd; dt1 = '03Jan1966:13:30:59.000123'dt; output;
        d1 = '03Jan1967'd; dt1 = '03Jan1966:13:30:59.990123'dt; output;
        d1 = '03Jan1968'd; dt1 = '03Jan1966:13:30:59'dt;        output;
        d1 = '03Nov1966'd; dt1 = '03Jan1966:13:30:00.000126'dt; output;
        d1 = '04Jan1966'd; dt1 = '03Jan1966:13:30:59'dt;        output;
    run;
"""


class TestDuckDBDataFrameIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession()
        cls.sas.set_batch(True)
        cls.sas.submit(TEST_DATA)

        cls.test_data = cls.sas.sasdata('testdata', results='duckdb')

    @classmethod
    def tearDownClass(cls):
        cls.sas._endsas()

    def test_duckdb_sd2df_instance(self):
        """
        Test method to_df with results='duckdb' returns a duckdb relation.
        """
        df = self.test_data.to_df()

        # Check for duckdb relation. It's usually <class '_duckdb.DuckDBPyRelation'>
        self.assertTrue(str(type(df)).find('DuckDBPyRelation') != -1)

    def test_duckdb_sd2df_values(self):
        """
        Test method to_df with results='duckdb' returns a duckdb relation containing
        the correct data.
        """
        EXPECTED = "1966-01-03"

        df = self.test_data.to_df()
        
        # In DuckDB relation, we can fetchone() or convert a row to pandas
        row = df.limit(1).fetchone()
        # Columns in our test data: d1 (date), dt1 (datetime)
        self.assertEqual(row[0].strftime('%Y-%m-%d'), EXPECTED)

    def test_duckdb_df2sd_instance(self):
        """
        Test method df2sd with a duckdb relation properly writes.
        """
        # Create a duckdb relation from a pandas dataframe
        con = duckdb.connect(':memory:')
        con.execute("CREATE TABLE t (a INTEGER)")
        con.execute("INSERT INTO t VALUES (1), (2), (3)")
        rel = con.table('t')
        
        td2 = self.sas.df2sd(rel, 'td2_db', results='text')

        self.assertIsInstance(td2, saspy.sasdata.SASdata)

    def test_duckdb_df2sd_values(self):
        """
        Test method df2sd with a duckdb relation properly writes the correct values.
        """
        EXPECTED = ['1', '1966-01-03T00:00:00.000000', '1966-01-03T13:30:59.000123']

        # Get a relation from ODA
        rel = self.test_data.to_df()
        td2 = self.sas.df2sd(rel, 'td2_db_vals', results='text')
        ll = td2.head()

        rows = ll['LST'].splitlines()
        retrieved = [x.split() for x in rows]

        self.assertIn(EXPECTED, retrieved, msg="td2.head() result didn't contain row 1")

    def test_duckdb_sd2df_csv_instance(self):
        """
        Test method to_df with results='DUCKDB' and method='CSV' returns a duckdb relation.
        """
        df = self.test_data.to_df(method='CSV')
        self.assertTrue(str(type(df)).find('DuckDBPyRelation') != -1)

    def test_duckdb_sd2df_disk(self):
        """
        Test method to_df with results='DUCKDB' and method='DISK'.
        """
        df = self.test_data.to_df(method='DISK')
        self.assertTrue(str(type(df)).find('DuckDBPyRelation') != -1)
        row = df.limit(1).fetchone()
        self.assertEqual(row[0].strftime('%Y-%m-%d'), "1966-01-03")

    def test_duckdb_wide_data(self):
        """
        Test method df2sd and to_df with wider than 32767 lrecl data using DuckDB
        """
        x = 'x x'*12767
        y = 'y\ny'*12767
        z = 'z z'*12767
        pdf = pd.DataFrame([{'x' : x[:32767], 'y' : y[:32767], 'z' : z[:32767], 'z2' : 'z'*32767}])
        pdf = pd.concat([pdf]*6, ignore_index=True)
        
        con = duckdb.connect(':memory:')
        con.register('df_view', pdf)
        rel = con.table('df_view')

        sde = self.sas.df2sd(rel, 'wide_db', results='text')
        res_rel = sde.to_df(results='duckdb')

        self.assertTrue(str(type(res_rel)).find('DuckDBPyRelation') != -1)
        self.assertEqual(6, res_rel.count('*').fetchone()[0])
        sde.delete(); del(sde); del(res_rel); del(rel); del(pdf)

class TestDuckDBValidVarname(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession()
        test_dict = {'Salary 2018': [1],
                   '2019_Salary $(USD)': [1],
                   'Really_Long_Variable_Name_To_Shorten': [1],
                   'Really Long Variable Name To Shorten': [1]}
        
        pdf = pd.DataFrame.from_dict(test_dict)
        con = duckdb.connect(':memory:')
        con.register('v_view', pdf)
        cls.test_rel = con.table('v_view')

    @classmethod
    def tearDownClass(cls):
        cls.sas._endsas()

    def test_duckdb_validvarname_v7(self):
        """
        Test method validvarname using `version=v7` with DuckDB.
        """
        v7_data = self.sas.validvarname(self.test_rel)
        # Result should be a DuckDB Relation
        self.assertTrue(str(type(v7_data)).find('DuckDBPyRelation') != -1)
        
        converted_col_names = v7_data.columns
        correct_names = ["Salary_2018", "_2019_Salary_USD_",
                        "Really_Long_Variable_Name_To_Sh0", "Really_Long_Variable_Name_To_Sh1"]

        [self.assertIn(name, converted_col_names) for name in correct_names]
        self.assertEqual(len(correct_names), len(converted_col_names))

    def test_duckdb_validvarname_any(self):
        """
        Test method validvarname using `version=any` with DuckDB.
        """
        any_data = self.sas.validvarname(self.test_rel, version='any')
        self.assertTrue(str(type(any_data)).find('DuckDBPyRelation') != -1)
        
        converted_col_names = any_data.columns

        correct_names = ['Salary 2018',
                         '2019_Salary $(USD)',
                         'Really_Long_Variable_Name_To_Sho',
                         'Really Long Variable Name To Sho']
        [self.assertIn(name, converted_col_names) for name in correct_names]
        self.assertEqual(len(correct_names), len(converted_col_names))

if __name__ == '__main__':
    unittest.main()
