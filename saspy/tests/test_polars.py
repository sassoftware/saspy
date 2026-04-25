import unittest
import saspy
import pandas as pd
try:
    import polars as pl
except ImportError:
    pl = None

TEST_DATA = """
    data testdata;
        format d1 date. dt1 datetime. t1 time.;
        d1 = '03Jan1966'd; dt1 = '03Jan1966:13:30:59.000123'dt; t1 = '13:30:59't; name = 'Alice'; age = 30; output;
        d1 = '03Jan1967'd; dt1 = '03Jan1966:13:30:59.990123'dt; t1 = '13:31:59't; name = 'Bob';   age = 25; output;
        d1 = '03Jan1968'd; dt1 = '03Jan1966:13:30:59'dt;        t1 = '13:32:59't; name = 'Char';  age = 35; output;
    run;
"""

class TestPolarsNative(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession()
        cls.sas.set_batch(True)
        cls.sas.submit(TEST_DATA)
        cls.test_data = cls.sas.sasdata('testdata', results='text')

    @classmethod
    def tearDownClass(cls):
        if cls.sas:
            cls.sas._endsas()

    def test_to_polars_eager(self):
        if pl is None:
            self.skipTest('polars not installed')
        df = self.test_data.to_polars()
        self.assertIsInstance(df, pl.DataFrame)
        self.assertEqual(df.shape, (3, 5))
        self.assertEqual(df['name'].to_list(), ['Alice', 'Bob', 'Char'])
        self.assertEqual(df['age'].to_list(), [30, 25, 35])

    def test_to_polars_lazy(self):
        if pl is None:
            self.skipTest('polars not installed')
        ldf = self.test_data.to_polars(polars_mode='LAZY')
        self.assertIsInstance(ldf, pl.LazyFrame)
        df = ldf.collect()
        self.assertIsInstance(df, pl.DataFrame)
        self.assertEqual(df.shape, (3, 5))

    def test_polars2sasdata_eager(self):
        if pl is None:
            self.skipTest('polars not installed')
        df = pl.DataFrame({
            'a': [1, 2, 3],
            'b': ['x', 'y', 'z'],
            'c': [True, False, True]
        })
        sd = self.sas.polars2sasdata(df, 'pl_eager')
        self.assertIsInstance(sd, saspy.sasdata.SASdata)
        self.assertTrue(self.sas.exist('pl_eager'))
        
        # Verify content
        pdf = sd.to_df()
        self.assertEqual(len(pdf), 3)

    def test_polars2sasdata_lazy(self):
        if pl is None:
            self.skipTest('polars not installed')
        df = pl.DataFrame({
            'a': [1, 2, 3],
            'b': ['x', 'y', 'z']
        })
        ldf = df.lazy()
        sd = self.sas.polars2sasdata(ldf, 'pl_lazy')
        self.assertIsInstance(sd, saspy.sasdata.SASdata)
        self.assertTrue(self.sas.exist('pl_lazy'))

    def test_session_results_polars(self):
        if pl is None:
            self.skipTest('polars not installed')
        orig_results = self.sas.results
        try:
            self.sas.set_results('Polars')
            df = self.test_data.to_df()
            self.assertIsInstance(df, pl.DataFrame)
        finally:
            self.sas.set_results(orig_results)

if __name__ == '__main__':
    unittest.main()
