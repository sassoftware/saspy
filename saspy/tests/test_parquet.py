import unittest
import saspy
import pandas as pd
import numpy  as np
import tempfile
import os

class TestPandasDataFrameIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession()
        cls.sas.set_batch(True)

    @classmethod
    def tearDownClass(cls):
        cls.sas._endsas()

    def test_sas_dataset_with_no_rows(self):
        """Test sasdata2parquet with sas dataset containing no rows"""
        self.sas.submit("""proc sql; CREATE TABLE work.empty(c1 CHAR(10), n1 NUMERIC, d1 DATE, i1 INT, f1 FLOAT); quit;""")

        # this should create a parquet file with the correct schema but there are no rows in the dataset, so the parquet file should have no rows as well
        self.sas.sasdata2parquet('empty.parquet', table='empty', libref='work')

        # now use python to read the parquet file and check that it has the correct schema and no rows
        df_empty = pd.read_parquet('empty.parquet')

        #print("df_empty = %s\n" % df_empty)
        #print("df_empty schema = %s \n" % df_empty.dtypes)
        #print("df_empty num_rows = %d\n" % len(df_empty))

        self.assertEqual(len(df_empty), 0, "The number of rows should have been 0 but was %d" % len(df_empty))
        self.assertEqual(len(df_empty.columns), 5, "The number of columns should have been 5 but was %d" % len(df_empty.columns))  # c1, n1, d1, i1, f1

        self.assertIn('c1', df_empty.columns, "The column names should have included 'c1' but were %s" % df_empty.columns)
        self.assertIn('n1', df_empty.columns, "The column names should have included 'n1' but were %s" % df_empty.columns)
        self.assertIn('d1', df_empty.columns, "The column names should have included 'd1' but were %s" % df_empty.columns)
        self.assertIn('i1', df_empty.columns, "The column names should have included 'i1' but were %s" % df_empty.columns)
        self.assertIn('f1', df_empty.columns, "The column names should have included 'f1' but were %s" % df_empty.columns)

        self.assertEqual(df_empty['c1'].dtype, np.dtype('O'), "The column type for 'c1' should have been object but was %s" % df_empty['c1'].dtype)
        self.assertEqual(df_empty['n1'].dtype, np.dtype('float64'), "The column type for 'n1' should have been float64 but was %s" % df_empty['n1'].dtype)
        self.assertEqual(df_empty['d1'].dtype, np.dtype('datetime64[ns]'), "The column type for 'd1' should have been datetime64[ns] but was %s" % df_empty['d1'].dtype)
        self.assertEqual(df_empty['i1'].dtype, np.dtype('float64'), "The column type for 'i1' should have been float64 but was %s" % df_empty['i1'].dtype)
        self.assertEqual(df_empty['f1'].dtype, np.dtype('float64'), "The column type for 'f1' should have been float64 but was %s" % df_empty['f1'].dtype)

        os.remove('empty.parquet')  # clean up the parquet file after the test