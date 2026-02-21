import unittest
import saspy
import pandas as pd
import pyarrow as pa
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


class TestPyArrowDataFrameIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession()
        cls.sas.set_batch(True)
        cls.sas.submit(TEST_DATA)

        cls.test_data = cls.sas.sasdata('testdata', results='pyarrow')

    @classmethod
    def tearDownClass(cls):
        cls.sas._endsas()

    def test_pyarrow_sd2df_instance(self):
        """
        Test method to_df with results='PYARROW' returns a pyarrow.Table
        """
        df = self.test_data.to_df()

        self.assertIsInstance(df, pa.Table)

    def test_pyarrow_sd2df_values(self):
        """
        Test method to_df with results='PYARROW' returns a pyarrow.Table
        containing the correct data.
        """
        EXPECTED = "1966-01-03"

        df = self.test_data.to_df()
        
        # In PyArrow, we can check the first value of the first column
        # Columns in our test data: d1 (date), dt1 (datetime)
        self.assertEqual(df.column('d1')[0].as_py().strftime('%Y-%m-%d'), EXPECTED)

    def test_pyarrow_df2sd_instance(self):
        """
        Test method df2sd with a pyarrow.Table properly writes.
        """
        df = self.test_data.to_df()
        td2 = self.sas.df2sd(df, 'td2_pa', results='text')

        self.assertIsInstance(td2, saspy.sasdata.SASdata)

    def test_pyarrow_df2sd_values(self):
        """
        Test method df2sd with a pyarrow.Table properly writes the correct values.
        """
        EXPECTED = ['1', '1966-01-03T00:00:00.000000', '1966-01-03T13:30:59.000123']

        df = self.test_data.to_df()
        td2 = self.sas.df2sd(df, 'td2_pa', results='text')
        ll = td2.head()

        rows = ll['LST'].splitlines()
        retrieved = [x.split() for x in rows]

        self.assertIn(EXPECTED, retrieved, msg="td2.head() result didn't contain row 1")

    def test_pyarrow_sd2df_csv_instance(self):
        """
        Test method to_df with results='PYARROW' and method='CSV' returns a pyarrow.Table.
        """
        df = self.test_data.to_df(method='CSV')
        self.assertIsInstance(df, pa.Table)

    def test_pyarrow_sd2df_disk(self):
        """
        Test method to_df with results='PYARROW' and method='DISK'.
        """
        df = self.test_data.to_df(method='DISK')
        self.assertIsInstance(df, pa.Table)
        self.assertEqual(df.column('d1')[0].as_py().strftime('%Y-%m-%d'), "1966-01-03")

    def test_pyarrow_wide_data(self):
        """
        Test method df2sd and to_df with wider than 32767 lrecl data using PyArrow
        """
        x = 'x x'*12767
        y = 'y\ny'*12767
        z = 'z z'*12767
        pdf = pd.DataFrame([{'x' : x[:32767], 'y' : y[:32767], 'z' : z[:32767], 'z2' : 'z'*32767}])
        pdf = pd.concat([pdf]*6, ignore_index=True)
        df = pa.Table.from_pandas(pdf)

        sde = self.sas.df2sd(df, 'wide_pa', results='text')
        res_df = sde.to_df(results='pyarrow')

        self.assertIsInstance(res_df, pa.Table)
        self.assertEqual(df.num_rows, res_df.num_rows)
        self.assertEqual(df.num_columns, res_df.num_columns)
        sde.delete(); del(sde); del(res_df); del(df)

class TestPyArrowValidVarname(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession()
        test_dict = {'Salary 2018': [1],
                   '2019_Salary $(USD)': [1],
                   'Really_Long_Variable_Name_To_Shorten': [1],
                   'Really Long Variable Name To Shorten': [1]}
        
        pdf = pd.DataFrame.from_dict(test_dict)
        cls.test_data = pa.Table.from_pandas(pdf)

    @classmethod
    def tearDownClass(cls):
        cls.sas._endsas()

    def test_pyarrow_validvarname_v7(self):
        """
        Test method validvarname using `version=v7` with PyArrow.
        """
        v7_data = self.sas.validvarname(self.test_data)
        self.assertIsInstance(v7_data, pa.Table)
        
        converted_col_names = v7_data.column_names
        correct_names = ["Salary_2018", "_2019_Salary_USD_",
                        "Really_Long_Variable_Name_To_Sh0", "Really_Long_Variable_Name_To_Sh1"]

        [self.assertIn(name, converted_col_names) for name in correct_names]
        self.assertEqual(len(correct_names), len(converted_col_names))

    def test_pyarrow_validvarname_any(self):
        """
        Test method validvarname using `version=any` with PyArrow.
        """
        any_data = self.sas.validvarname(self.test_data, version='any')
        self.assertIsInstance(any_data, pa.Table)
        
        converted_col_names = any_data.column_names

        correct_names = ['Salary 2018',
                         '2019_Salary $(USD)',
                         'Really_Long_Variable_Name_To_Sho',
                         'Really Long Variable Name To Sho']
        [self.assertIn(name, converted_col_names) for name in correct_names]
        self.assertEqual(len(correct_names), len(converted_col_names))
