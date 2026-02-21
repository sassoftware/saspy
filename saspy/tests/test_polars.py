import unittest
import saspy
import pandas as pd
import polars as pl
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


class TestPolarsDataFrameIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession()
        cls.sas.set_batch(True)
        cls.sas.submit(TEST_DATA)

        cls.test_data = cls.sas.sasdata('testdata', results='polars')

    @classmethod
    def tearDownClass(cls):
        cls.sas._endsas()

    def test_polars_sd2df_instance(self):
        """
        Test method to_df with results='POLARS' returns a polars.DataFrame
        """
        df = self.test_data.to_df()

        self.assertIsInstance(df, pl.DataFrame)

    def test_polars_sd2df_values(self):
        """
        Test method to_df with results='POLARS' returns a polars.DataFrame
        containing the correct data.
        """
        EXPECTED = "1966-01-03"

        df = self.test_data.to_df()
        
        self.assertEqual(df.to_series(1)[0].strftime('%Y-%m-%d'), EXPECTED)

    def test_polars_df2sd_instance(self):
        """
        Test method df2sd with a polars.DataFrame properly writes.
        """
        df = self.test_data.to_df()
        td2 = self.sas.df2sd(df, 'td2', results='text')

        self.assertIsInstance(td2, saspy.sasdata.SASdata)

    def test_polars_df2sd_values(self):
        """
        Test method df2sd with a polars.DataFrame properly writes the correct values.
        """
        EXPECTED = ['1', '1966-01-03T00:00:00.000000', '1966-01-03T13:30:59.000123']

        df = self.test_data.to_df()
        td2 = self.sas.df2sd(df, 'td2', results='text')
        ll = td2.head()

        rows = ll['LST'].splitlines()
        retrieved = [x.split() for x in rows]

        self.assertIn(EXPECTED, retrieved, msg="td2.head() result didn't contain row 1")

    def test_polars_lazy_df2sd_instance(self):
        """
        Test method df2sd with a polars.LazyFrame properly writes.
        """
        df = self.test_data.to_df().lazy()
        td2 = self.sas.df2sd(df, 'td2_lazy', results='text')

        self.assertIsInstance(td2, saspy.sasdata.SASdata)

    def test_polars_sd2df_csv_instance(self):
        """
        Test method to_df with results='POLARS' and method='CSV' returns a polars.DataFrame.
        """
        df = self.test_data.to_df(method='CSV')
        self.assertIsInstance(df, pl.DataFrame)

    def test_polars_sd2df_csv_tempfile_instance(self):
        """
        Test method to_df with results='POLARS' and method='CSV' and argument
        `tempfile=...` returns a polars.DataFrame.
        """
        tmpdir = tempfile.TemporaryDirectory()
        tmpcsv = os.path.join(tmpdir.name, 'tomodsx_pl')

        df = self.test_data.to_df(method='CSV', tempfile=tmpcsv)

        tmpdir.cleanup()

        self.assertIsInstance(df, pl.DataFrame)

    def test_polars_sd2df_disk(self):
        """
        Test method to_df with results='POLARS' and method='DISK'.
        """
        df = self.test_data.to_df(method='DISK')
        self.assertIsInstance(df, pl.DataFrame)
        self.assertEqual(df.to_series(1)[0].strftime('%Y-%m-%d'), "1966-01-03")

    def test_polars_wide_data(self):
        """
        Test method df2sd and to_df with wider than 32767 lrecl data using Polars
        """
        x = 'x x'*12767
        y = 'y\ny'*12767
        z = 'z z'*12767
        df = pl.DataFrame([{'x' : x[:32767], 'y' : y[:32767], 'z' : z[:32767], 'z2' : 'z'*32767}])
        df = pl.concat([df, df, df, df, df, df])
        
        # Polars handles nulls differently, but let's test a few
        # Using a more Polars-idiomatic way to add nulls if needed, 
        # but here we just check if it round-trips correctly.

        sde = self.sas.df2sd(df, 'wide_pl', results='text')
        res_df = sde.to_df() # results='polars' is inherited from self.test_data? No, from session or specified.
        # But this class set results='polars' on self.test_data specifically. 
        # Let's ensure we get Polars back.
        res_df = sde.to_df(results='polars')

        self.assertIsInstance(res_df, pl.DataFrame)
        self.assertEqual(df.shape, res_df.shape)
        sde.delete(); del(sde); del(res_df); del(df)

class TestPolarsValidVarname(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession()
        test_dict = {'Salary 2018': [1],
                   '2019_Salary $(USD)': [1],
                   'Really_Long_Variable_Name_To_Shorten': [1],
                   'Really Long Variable Name To Shorten': [1]}
        duplicate_dict = {'My String!abc' : [0], 'My String@abc' : [1],
                         'My String#abc' : [2], 'My String$abc' : [3],
                         'My String%abc': [4], 'My String^abc' : [5],
                         'My String&abc' :[6], 'My String*abc' : [7],
                         'My String(abc' :[8], 'My String)abc' :[9]}

        cls.duplicate_data = pl.DataFrame(duplicate_dict)
        cls.test_data = pl.DataFrame(test_dict)

    @classmethod
    def tearDownClass(cls):
        cls.sas._endsas()

    def test_polars_validvarname_v7(self):
        """
        Test method validvarname using `version=v7` with Polars.
        """
        v7_data = self.sas.validvarname(self.test_data)
        converted_col_names = list(v7_data.columns)
        correct_names = ["Salary_2018", "_2019_Salary_USD_",
                        "Really_Long_Variable_Name_To_Sh0", "Really_Long_Variable_Name_To_Sh1"]

        [self.assertIn(name, converted_col_names) for name in correct_names]
        self.assertEqual(len(correct_names), len(converted_col_names))

    def test_polars_validvarname_any(self):
        """
        Test method validvarname using `version=any` with Polars.
        """
        any_data = self.sas.validvarname(self.test_data, version='any')
        converted_col_names = list(any_data.columns)

        # Polars names might be truncated if too long, but here they are short enough or handled by validvarname
        correct_names = ['Salary 2018',
                         '2019_Salary $(USD)',
                         'Really_Long_Variable_Name_To_Sho',
                         'Really Long Variable Name To Sho']
        [self.assertIn(name, converted_col_names) for name in correct_names]
        self.assertEqual(len(correct_names), len(converted_col_names))
