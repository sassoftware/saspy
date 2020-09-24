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




