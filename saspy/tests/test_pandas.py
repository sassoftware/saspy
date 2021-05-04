import unittest
import saspy
import pandas as pd
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


class TestPandasDataFrameIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession()
        cls.sas.set_batch(True)
        cls.sas.submit(TEST_DATA)

        cls.test_data = cls.sas.sasdata('testdata', results='text')

    @classmethod
    def tearDownClass(cls):
        cls.sas._endsas()

    def test_pandas_sd2df_instance(self):
        """
        Test method sasdata2dataframe returns a pandas.DataFrame
        """
        df = self.test_data.to_df()

        self.assertIsInstance(df, pd.DataFrame)

    def test_pandas_sd2df_values(self):
        """
        Test method sasdata2dataframe returns a pandas.DataFrame containing
        the correct data.
        """
        EXPECTED = ['0', '1966-01-03', '1966-01-03', '13:30:59.000123']

        df = self.test_data.to_df()
        result = df.head()

        # FIXME: May be more robust to compare actual data structures.
        rows = result.to_string().splitlines()
        retrieved = [x.split() for x in rows]

        self.assertIn(EXPECTED, retrieved, msg="df.head() result didn't contain row 1")

    def test_pandas_df2sd_instance(self):
        """
        Test method dataframe2sasdata properly writes.
        """
        df = self.test_data.to_df()
        td2 = self.sas.df2sd(df, 'td2', results='text')

        self.assertIsInstance(td2, saspy.sasdata.SASdata)

    def test_pandas_df2sd_values(self):
        """
        Test method dataframe2sasdata properly writes the correct values.
        """
        EXPECTED = ['1', '1966-01-03T00:00:00.000000', '1966-01-03T13:30:59.000123']

        df = self.test_data.to_df()
        td2 = self.sas.df2sd(df, 'td2', results='text')
        ll = td2.head()

        # FIXME: May be more robust to compare actual data structures.
        rows = ll['LST'].splitlines()
        retrieved = [x.split() for x in rows]

        self.assertIn(EXPECTED, retrieved, msg="td2.head() result didn't contain row 1")

    def test_pandas_sd2df_csv_instance(self):
        """
        Test method sasdata2dataframe using `method=csv` returns a
        pandas.DataFrame.
        """
        df = self.test_data.to_df_CSV()
        self.assertIsInstance(df, pd.DataFrame)

    def test_pandas_sd2df_csv_values(self):
        """
        Test method sasdata2dataframe using `method=csv` returns a
        pandas.DataFrame containing the correct values.
        """
        EXPECTED = ['0', '1966-01-03', '1966-01-03', '13:30:59.000123']

        df = self.test_data.to_df_CSV()
        result = df.head()

        # FIXME: May be more robust to compare actual data structures.
        rows = result.to_string().splitlines()
        retrieved = [x.split() for x in rows]

        self.assertIn(EXPECTED, retrieved, msg="df.head() result didn't contain row 1")

    def test_pandas_sd2df_csv_tempfile_instance(self):
        """
        Test method sasdata2dataframe using `method=csv` and argument
        `tempfile=...` returns a pandas.DataFrame.
        """
        tmpdir = tempfile.TemporaryDirectory()
        tmpcsv = os.path.join(tmpdir.name, 'tomodsx')

        df = self.test_data.to_df_CSV(tempfile=tmpcsv)

        tmpdir.cleanup()

        self.assertIsInstance(df, pd.core.frame.DataFrame)

    def test_pandas_sd2df_csv_tempfile_values(self):
        """
        Test method sasdata2dataframe using `method=csv` and argument
        `tempfile=...` returns a pandas.DataFrame containing the correct
        values.
        """
        EXPECTED = ['0', '1966-01-03', '1966-01-03', '13:30:59.000123']
        tmpdir = tempfile.TemporaryDirectory()
        tmpcsv = os.path.join(tmpdir.name, 'tomodsx.csv')

        df = self.test_data.to_df_CSV(tempfile=tmpcsv)
        result = df.head()

        rows = result.to_string().splitlines()
        retrieved = [x.split() for x in rows]

        tmpdir.cleanup()

        self.assertIn(EXPECTED, retrieved, msg="df.head() result didn't contain row 1")

    def test_pandas_sd2df_csv_tempfile_tempkeep_true(self):
        """
        Test method sasdata2dataframe using `method=csv` and arguments
        `tempfile=..., tempkeep=True` retains the temporary CSV file in the
        provided location.
        """
        tmpdir = tempfile.TemporaryDirectory()
        tmpcsv = os.path.join(tmpdir.name, 'tomodsx.csv')

        df = self.test_data.to_df_CSV(tempfile=tmpcsv, tempkeep=True)

        if self.sas.sascfg.mode == 'IOM':
          self.assertTrue(os.path.isfile(tmpcsv))

        tmpdir.cleanup()

    def test_pandas_sd2df_csv_tempfile_tempkeep_false(self):
        """
        Test method sasdata2dataframe using `method=csv` and arguments
        `tempfile=..., tempkeep=False` does not retain the temporary CSV file
        in the provided location.
        """
        tmpdir = tempfile.TemporaryDirectory()
        tmpcsv = os.path.join(tmpdir.name, 'tomodsx.csv')

        df = self.test_data.to_df_CSV(tempfile=tmpcsv, tempkeep=False)

        self.assertFalse(os.path.isfile(tmpcsv))

        tmpdir.cleanup()


    def test_sd2df_DISK(self):
        """
        Test method sasdata2dataframe using `method=disk` and arguments
        """

        data = [
        [442.5, '"quoted\x01 string"', 'non\t\tquoted string',44.4,'"leading quote string',    '"leading"and embed\x0Aded string','''"all' "over' 'the "place"''',0],
        [132.5, '"quoted\x02 string"', 'non quoted string',   41.4,'"leading quote string',    '"leading"and embed\x0Dded string','''"all' "over' 'the "place"''',20.7],
        [242.5, '"quoted\x03 string"', 'non quoted string',   42.4,'"leading\t\t quote string','"leading"and embed\x0Aded string','''"all' "over' 'the "place"''',20.8],
        [342.5, '"quoted\x02 string"', '',                    43.4,'"leading quote string',    '"leading"and embed\x0Dded string','''"all' "over' 'the "place"''',10.9],
        [342.5, "'quoted\x01 string'", 'non quoted string',   43.4,'''"leading'quote string''','"leading"and embed\x0Adedstring"','''"all' "over' 'the "place"''',10.9],
        ]

        df = pd.DataFrame(data)

        sd  = self.sas.df2sd(df, 'quotes')

        df2 = sd.to_df()
        df3 = sd.to_df_DISK()

        self.assertTrue(df2.shape == (5, 8))
        self.assertTrue(df3.shape == (5, 8))
        self.assertFalse(False in (df2 == df3))

        cars = self.sas.sasdata('cars','sashelp', results='text')
        df   = cars.to_df_DISK(colsep='A', rowsep='E', colrep='"', rowrep='?')

        self.assertTrue(df.shape == (428, 15))


class TestPandasValidVarname(unittest.TestCase):
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

        cls.duplicate_data = pd.DataFrame.from_dict(duplicate_dict)
        cls.test_data = pd.DataFrame.from_dict(test_dict)

    @classmethod
    def tearDownClass(cls):
        cls.sas._endsas()

    def test_validvarname_v7(self):
        """
        Test method validvarname using `version=v7`.
        """
        v7_data = self.sas.validvarname(self.test_data)
        converted_col_names = list(v7_data.columns)
        correct_names = ["Salary_2018", "_2019_Salary_USD_", 
                        "Really_Long_Variable_Name_To_Sh0", "Really_Long_Variable_Name_To_Sh1"]
        
        [self.assertIn(name, converted_col_names) for name in correct_names]
        self.assertEqual(len(correct_names), len(converted_col_names))
        

    def test_validvarname_v6(self):
        """
        Test method validvarname using `version=v6`.
        """
        v6_data = self.sas.validvarname(self.duplicate_data, version='v6')
        converted_col_names = list(v6_data.columns)

        correct_names = ['My_Stri0', 'My_Stri1', 
                         'My_Stri2', 'My_Stri3', 
                         'My_Stri4', 'My_Stri5', 
                         'My_Stri6', 'My_Stri7',
                         'My_Stri8', 'My_Stri9']
        
        [self.assertIn(name, converted_col_names) for name in correct_names]
        self.assertEqual(len(correct_names), len(converted_col_names))
    
    def test_validvarname_upcase(self):
        """
        Test method validvarname using `version=upcase`.
        """
        upcase_data = self.sas.validvarname(self.test_data, version='upcase')
        converted_col_names = list(upcase_data.columns)
        correct_names = ["Salary_2018", "_2019_Salary_USD_", 
                        "Really_Long_Variable_Name_To_Sh0", "Really_Long_Variable_Name_To_Sh1"]
        correct_names = [name.upper() for name in correct_names]
        
        [self.assertIn(name, converted_col_names) for name in correct_names]
        self.assertEqual(len(correct_names), len(converted_col_names))


    def test_validvarname_any(self):
        """
        Test method validvarname using `version=any`.
        """
        any_data = self.sas.validvarname(self.test_data, version='any')
        converted_col_names = list(any_data.columns)

        correct_names = ['Salary 2018',
                         '2019_Salary $(USD)',
                         'Really_Long_Variable_Name_To_Sho',
                         'Really Long Variable Name To Sho']
        [self.assertIn(name, converted_col_names) for name in correct_names]
        self.assertEqual(len(correct_names), len(converted_col_names))
