import unittest
import polars as pl
import datetime
import saspy.polars_types as pt

class TestPolarsTypes(unittest.TestCase):
    def test_get_polars_dtype_numeric_and_string(self):
        self.assertIs(pt.PolarsTypeMapper.get_polars_dtype("C"), pl.String)
        self.assertIs(pt.PolarsTypeMapper.get_polars_dtype("N"), pl.Float64)
        self.assertIs(pt.PolarsTypeMapper.get_polars_dtype("N", "DATETIME"), pl.Datetime)
        self.assertIs(pt.PolarsTypeMapper.get_polars_dtype("N", "TIME"), pl.Time)

    def test_convert_datetime_to_string_transforms_columns(self):
        df = pl.DataFrame({
            "datetime_col": pl.Series([
                datetime.datetime(2023,1,1,0,0,0),
                datetime.datetime(2023,1,1,1,0,0),
                datetime.datetime(2023,1,1,2,0,0)
            ]),
            "int_col": pl.Series([1, 2, 3]),
        })
        result = pt.PolarsTypeMapper.convert_datetime_to_string(df, ["datetime_col"])
        self.assertEqual(result["datetime_col"].dtype, pl.Utf8)
        self.assertEqual(result["int_col"].dtype, pl.Int64)
        self.assertTrue(result["datetime_col"][0].startswith("2023-01-01T00:00:00"))

if __name__ == "__main__":
    unittest.main()
