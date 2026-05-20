import unittest
from datetime import date, datetime, time

import saspy

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

TEST_DATA_ALL_TYPES = """
    data testdata_all_types;
        format dt date. dtm datetime. tm time.;
        dt = '01Jan2024'd; dtm = '01Jan2024:10:30:00'dt; tm = '10:30:00't;
        num_int = 42; num_float = 3.14159; str_var = 'Hello'; bool_var = 1;
        missing_num = .; missing_char = ' '; output;
        dt = '02Jan2024'd; dtm = '01Jan2024:11:45:30.123'dt; tm = '11:45:30't;
        num_int = 100; num_float = 2.71828; str_var = 'World'; bool_var = 0;
        missing_num = .; missing_char = ''; output;
    run;
"""

TEST_DATA_EMPTY = """
    data testdata_empty;
        set testdata(obs=0);
    run;
"""


class TestPolarsNative(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession()
        cls.sas.set_batch(True)
        cls.sas.submit(TEST_DATA)
        cls.test_data = cls.sas.sasdata("testdata", results="text")

    @classmethod
    def tearDownClass(cls):
        if cls.sas:
            cls.sas._endsas()

    def test_to_polars_eager(self):
        if pl is None:
            self.skipTest("polars not installed")
        df = self.test_data.to_polars()
        self.assertIsInstance(df, pl.DataFrame)
        self.assertEqual(df.shape, (3, 5))
        self.assertEqual(df["name"].to_list(), ["Alice", "Bob", "Char"])
        self.assertEqual(df["age"].to_list(), [30, 25, 35])

    def test_to_polars_lazy(self):
        if pl is None:
            self.skipTest("polars not installed")
        ldf = self.test_data.to_polars(polars_mode="LAZY")
        self.assertIsInstance(ldf, pl.LazyFrame)
        df = ldf.collect()
        self.assertIsInstance(df, pl.DataFrame)
        self.assertEqual(df.shape, (3, 5))

    def test_polars2sasdata_eager(self):
        if pl is None:
            self.skipTest("polars not installed")
        df = pl.DataFrame(
            {"a": [1, 2, 3], "b": ["x", "y", "z"], "c": [True, False, True]}
        )
        sd = self.sas.polars2sasdata(df, "pl_eager")
        self.assertIsInstance(sd, saspy.sasdata.SASdata)
        self.assertTrue(self.sas.exist("pl_eager"))

        pdf = sd.to_df()
        self.assertEqual(len(pdf), 3)

    def test_polars2sasdata_lazy(self):
        if pl is None:
            self.skipTest("polars not installed")
        df = pl.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
        ldf = df.lazy()
        sd = self.sas.polars2sasdata(ldf, "pl_lazy")
        self.assertIsInstance(sd, saspy.sasdata.SASdata)
        self.assertTrue(self.sas.exist("pl_lazy"))

    def test_session_results_polars(self):
        if pl is None:
            self.skipTest("polars not installed")
        orig_results = self.sas.results
        try:
            self.sas.set_results("Polars")
            df = self.test_data.to_df()
            self.assertIsInstance(df, pl.DataFrame)
        finally:
            self.sas.set_results(orig_results)


class TestPolarsDataTypes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession()
        cls.sas.set_batch(True)
        cls.sas.submit(TEST_DATA_ALL_TYPES)
        cls.test_data = cls.sas.sasdata("testdata_all_types", results="text")

    @classmethod
    def tearDownClass(cls):
        if cls.sas:
            cls.sas._endsas()

    def test_to_polars_date_type(self):
        if pl is None:
            self.skipTest("polars not installed")
        df = self.test_data.to_polars()
        self.assertEqual(df["dt"].dtype, pl.Date)
        self.assertEqual(df["dt"][0], date(2024, 1, 1))

    def test_to_polars_datetime_type(self):
        if pl is None:
            self.skipTest("polars not installed")
        df = self.test_data.to_polars()
        self.assertEqual(df["dtm"].dtype, pl.Datetime)
        self.assertIsNotNone(df["dtm"][0])

    def test_to_polars_time_type(self):
        if pl is None:
            self.skipTest("polars not installed")
        df = self.test_data.to_polars()
        self.assertEqual(df["tm"].dtype, pl.Time)

    def test_to_polars_float_type(self):
        if pl is None:
            self.skipTest("polars not installed")
        df = self.test_data.to_polars()
        self.assertEqual(df["num_float"].dtype, pl.Float64)
        self.assertAlmostEqual(df["num_float"][0], 3.14159, places=4)

    def test_to_polars_integer_type(self):
        if pl is None:
            self.skipTest("polars not installed")
        df = self.test_data.to_polars()
        self.assertEqual(df["num_int"].dtype, pl.Int64)
        self.assertEqual(df["num_int"][0], 42)

    def test_to_polars_string_type(self):
        if pl is None:
            self.skipTest("polars not installed")
        df = self.test_data.to_polars()
        self.assertEqual(df["str_var"].dtype, pl.Utf8)
        self.assertEqual(df["str_var"].to_list(), ["Hello", "World"])

    def test_to_polars_boolean_type(self):
        if pl is None:
            self.skipTest("polars not installed")
        df = self.test_data.to_polars()
        self.assertEqual(df["bool_var"].dtype, pl.Boolean)

    def test_to_polars_null_handling(self):
        if pl is None:
            self.skipTest("polars not installed")
        df = self.test_data.to_polars()
        self.assertTrue(df["missing_num"].is_null().to_list()[0])


class TestPolarsEdgeCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession()
        cls.sas.set_batch(True)

    @classmethod
    def tearDownClass(cls):
        if cls.sas:
            cls.sas._endsas()

    def test_to_polars_empty_dataframe(self):
        if pl is None:
            self.skipTest("polars not installed")
        self.sas.submit(TEST_DATA)
        self.sas.submit(TEST_DATA_EMPTY)
        test_data = self.sas.sasdata("testdata_empty", results="text")
        df = test_data.to_polars()
        self.assertEqual(df.shape, (0, 5))

    def test_polars2sasdata_empty_dataframe(self):
        if pl is None:
            self.skipTest("polars not installed")
        df = pl.DataFrame({"a": [], "b": []})
        sd = self.sas.polars2sasdata(df, "pl_empty")
        self.assertTrue(self.sas.exist("pl_empty"))
        result = sd.to_df()
        self.assertEqual(len(result), 0)

    def test_polars2sasdata_special_char_column_names(self):
        if pl is None:
            self.skipTest("polars not installed")
        df = pl.DataFrame({"col$a": [1, 2], "col#b": ["x", "y"]})
        with self.assertRaises(Exception):
            self.sas.polars2sasdata(df, "pl_bad_name")

    def test_polars2sasdata_missing_column(self):
        if pl is None:
            self.skipTest("polars not installed")
        df = pl.DataFrame({"a": [1, 2, 3]})
        sd = self.sas.polars2sasdata(df, "pl_single_col")
        self.assertTrue(self.sas.exist("pl_single_col"))


class TestPolarsRoundTrip(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession()
        cls.sas.set_batch(True)
        cls.sas.submit(TEST_DATA)

    @classmethod
    def tearDownClass(cls):
        if cls.sas:
            cls.sas._endsas()

    def test_sas_to_polars_to_sas_roundtrip(self):
        if pl is None:
            self.skipTest("polars not installed")
        original_df = self.sas.sasdata("testdata", results="text").to_df()
        original_len = len(original_df)

        polars_df = self.sas.sasdata("testdata", results="Polars").to_polars()
        self.assertIsInstance(polars_df, pl.DataFrame)

        sd = self.sas.polars2sasdata(polars_df, "roundtrip_test")
        result_df = sd.to_df()

        self.assertEqual(len(result_df), original_len)


class TestPolarsStreaming(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession()
        cls.sas.set_batch(True)
        cls.sas.submit(TEST_DATA)
        cls.test_data = cls.sas.sasdata("testdata", results="text")

    @classmethod
    def tearDownClass(cls):
        if cls.sas:
            cls.sas._endsas()

    def test_to_polars_with_stream(self):
        if pl is None:
            self.skipTest("polars not installed")
        try:
            df = self.test_data.to_polars(stream=True)
            self.assertIsInstance(df, (pl.DataFrame, pl.LazyFrame))
        except TypeError:
            self.skipTest("stream parameter not supported")

    def test_polars2sasdata_with_stream(self):
        if pl is None:
            self.skipTest("polars not installed")
        df = pl.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
        try:
            sd = self.sas.polars2sasdata(df, "pl_stream", stream=True)
            self.assertTrue(self.sas.exist("pl_stream"))
        except TypeError:
            self.skipTest("stream parameter not supported")


class TestPolarsErrorHandling(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession()
        cls.sas.set_batch(True)
        cls.sas.submit(TEST_DATA)
        cls.test_data = cls.sas.sasdata("testdata", results="text")

    @classmethod
    def tearDownClass(cls):
        if cls.sas:
            cls.sas._endsas()

    def test_to_polars_invalid_mode(self):
        if pl is None:
            self.skipTest("polars not installed")
        with self.assertRaises(ValueError):
            self.test_data.to_polars(polars_mode="INVALID")

    def test_polars2sasdata_invalid_name(self):
        if pl is None:
            self.skipTest("polars not installed")
        df = pl.DataFrame({"a": [1, 2, 3]})
        with self.assertRaises(Exception):
            self.sas.polars2sasdata(df, "123invalid")

    def test_polars2sasdata_type_mismatch(self):
        if pl is None:
            self.skipTest("polars not installed")
        df = pl.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
        sd = self.sas.polars2sasdata(df, "type_test")
        result = sd.to_df()
        self.assertEqual(len(result), 3)


if __name__ == "__main__":
    unittest.main()
