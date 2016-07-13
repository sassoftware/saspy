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

    def test_Panda(self):
        import pandas
        self.sas.set_batch(True)

        td = self.sas.sasdata('timedata', libref='sashelp', results='text')
        self.assertIsInstance(td, saspy.SASdata, msg="cars = sas.sasdata(...) failed")

        df = td.to_df()
        self.assertIsInstance(df, pandas.core.frame.DataFrame, msg="df = td.to_df(...) failed")

        td2 = self.sas.df2sd(df, 'td2', results='text')
        self.assertIsInstance(td2, saspy.SASdata, msg="td2 = sas.df2sd((...) failed")

        ll = td2.head()
        expected = ['1', '1', '1997-07-25T00:00:00.000000']
        rows = ll['LST'].splitlines()
        retrieved = []
        for i in range(len(rows)):
           retrieved.append(rows[i].split())
        self.assertIn(expected, retrieved, msg="td2.head() result didn't contain row 1")

