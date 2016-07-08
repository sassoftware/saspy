import unittest
import saspy


class TestConfig(unittest.TestCase):
    def __init__(self, *args):
        super(TestConfig, self).__init__(*args)

    def setUp(self):
        self.sas = saspy.SASsession()

    def tearDown(self):
        self.sas._endsas()

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
        self.assertIn("1       1      1997-07-25T00:00:00.000000", ll['LST'], msg="td2.head() result didn't contain row 1")

