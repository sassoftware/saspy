import unittest
import saspy


class TestPandasDataFrameIntegration(unittest.TestCase):
    def __init__(self, *args):
        super(TestPandasDataFrameIntegration, self).__init__(*args)
        self.sas = saspy.SASsession()#cfgname='default')
        self.assertIsInstance(self.sas, saspy.SASsession, msg="sas = saspy.SASsession(...) failed")

    def __del__(self, *args):
        if self.sas:
           self.sas._endsas()

    def setUp(self):
        #self.sas = saspy.SASsession()
        pass

    def tearDown(self):
        #if self.sas:
        #   self.sas._endsas()
        pass

    def test_Pandas(self):
        import pandas
        self.sas.set_batch(True)

        ll = self.sas.submit('''
                             data testdata; format d1 date. dt1 datetime. ;
                             d1 = '03jan1966'd; dt1='03jan1966:13:30:59'dt; output;           
                             d1 = '03jan1966'd; dt1='03jan1966:13:30:59'dt; output;           
                             d1 = '03jan1966'd; dt1='03jan1966:13:30:59'dt; output;           
                             d1 = '03jan1966'd; dt1='03jan1966:13:30:59'dt; output;           
                             d1 = '03jan1966'd; dt1='03jan1966:13:30:59'dt; output; 
                             run;
                             ''')

        td = self.sas.sasdata('testdata', results='text')
        self.assertIsInstance(td, saspy.SASdata, msg="cars = sas.sasdata(...) failed")

        #test sas data to data frame
        df = td.to_df()
        self.assertIsInstance(df, pandas.core.frame.DataFrame, msg="df = td.to_df(...) failed")
        result = df.head()
        expected = ['0', '1966-01-03', '1966-01-03', '13:30:59']
        rows = result.to_string().splitlines()
        retrieved = []
        for i in range(len(rows)):
           retrieved.append(rows[i].split())
        self.assertIn(expected, retrieved, msg="df.head() result didn't contain row 1")

        #test data frame to sas data
        td2 = self.sas.df2sd(df, 'td2', results='text')
        self.assertIsInstance(td2, saspy.SASdata, msg="td2 = sas.df2sd((...) failed")
        ll = td2.head()
        expected = ['1', '1966-01-03T00:00:00.000000', '1966-01-03T13:30:59.000000']
        rows = ll['LST'].splitlines()
        retrieved = []
        for i in range(len(rows)):
           retrieved.append(rows[i].split())
        self.assertIn(expected, retrieved, msg="td2.head() result didn't contain row 1")

