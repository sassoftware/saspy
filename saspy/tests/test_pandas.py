import unittest
import saspy
import pandas


class TestPandasDataFrameIntegration(unittest.TestCase):
    @classmethod    
    def setUpClass(cls):
        cls.sas = saspy.SASsession() #cfgname='default')
        #cls.assertIsInstance(cls.sas, saspy.SASsession, msg="sas = saspy.SASsession(...) failed")

    @classmethod
    def tearDownClass(cls):
        if cls.sas:
           cls.sas._endsas()

    def test_Pandas(self):
        self.sas.set_batch(True)

        ll = self.sas.submit('''
                             data testdata; format d1 date. dt1 datetime. ;
                             d1 = '03jan1966'd; dt1='03jan1966:13:30:59.000123'dt; output;
                             d1 = '03jan1967'd; dt1='03jan1966:13:30:59.990123'dt; output;
                             d1 = '03jan1968'd; dt1='03jan1966:13:30:59'dt; output;
                             d1 = '03nov1966'd; dt1='03jan1966:13:30:00.000126'dt; output;
                             d1 = '04jan1966'd; dt1='03jan1966:13:30:59'dt; output;
                             run;
                             ''')
        td = self.sas.sasdata('testdata', results='text')
        self.assertIsInstance(td, saspy.SASdata, msg="cars = sas.sasdata(...) failed")

    def test_Pandas_sd2df(self):
        #test sas data to data frame
        td = self.sas.sasdata('testdata', results='text')
        df = td.to_df()
        self.assertIsInstance(df, pandas.core.frame.DataFrame, msg="df = td.to_df(...) failed")
        result = df.head()
        expected = ['0', '1966-01-03', '1966-01-03', '13:30:59.000123']
        rows = result.to_string().splitlines()
        retrieved = []
        for i in range(len(rows)):
           retrieved.append(rows[i].split())
        self.assertIn(expected, retrieved, msg="df.head() result didn't contain row 1")

    def test_Pandas_df2sd(self):
        #test data frame to sas data
        td = self.sas.sasdata('testdata', results='text')
        df = td.to_df()
        td2 = self.sas.df2sd(df, 'td2', results='text')
        self.assertIsInstance(td2, saspy.SASdata, msg="td2 = sas.df2sd((...) failed")
        ll = td2.head()
        expected = ['1', '1966-01-03T00:00:00.000000', '1966-01-03T13:30:59.000123']
        rows = ll['LST'].splitlines()
        retrieved = []
        for i in range(len(rows)):
           retrieved.append(rows[i].split())
        self.assertIn(expected, retrieved, msg="td2.head() result didn't contain row 1")

