import unittest
import polars as pl
from saspy.polars_types import PolarsTypeMapper

class TestPolarsTypeMapperUnit(unittest.TestCase):
    def test_get_sas_transfer_metadata_basic(self):
        df = pl.DataFrame({
            'a': [1, 2, 3],
            'b': ['x', 'y', 'z'],
            'c': [True, False, True]
        })
        meta = PolarsTypeMapper.get_sas_transfer_metadata(df)
        
        # Verify lengths
        self.assertIn("'a'n 8", meta['length'])
        self.assertIn("'b'n $8", meta['length'])
        self.assertIn("'c'n 8", meta['length'])
        
        # Verify inputs
        self.assertIn("input 'a'n", meta['input'])
        self.assertIn("input 'b'n", meta['input'])
        self.assertIn("input 'c'n", meta['input'])

    def test_get_sas_transfer_metadata_dates(self):
        from datetime import date, datetime, time
        df = pl.DataFrame({
            'd': [date(2023, 1, 1)],
            'dt': [datetime(2023, 1, 1, 12, 0, 0)],
            't': [time(12, 0, 0)]
        })
        
        # Default behavior: everything as datetime
        meta = PolarsTypeMapper.get_sas_transfer_metadata(df)
        self.assertIn("'d'n E8601DT26.6", meta['format'])
        self.assertIn("'dt'n E8601DT26.6", meta['format'])
        self.assertIn("'t'n E8601DT26.6", meta['format'])
        
        # Explicit overrides
        meta = PolarsTypeMapper.get_sas_transfer_metadata(df, datetimes={'d': 'date', 't': 'time'})
        self.assertIn("'d'n E8601DA.", meta['format'])
        self.assertIn("'t'n E8601TM.", meta['format'])
        self.assertIn("'dt'n E8601DT26.6", meta['format'])
        
        # Verify xlate for dates
        self.assertIn("'d'n = datepart('d'n)", meta['xlate'])
        self.assertIn("'t'n = timepart('t'n)", meta['xlate'])

    def test_get_sas_transfer_metadata_string_lengths(self):
        df = pl.DataFrame({
            'short': ['a'],
            'long': ['this is a long string']
        })
        meta = PolarsTypeMapper.get_sas_transfer_metadata(df)
        self.assertIn("'short'n $8", meta['length']) # min 8
        self.assertIn("'long'n $21", meta['length'])

    def test_get_sas_transfer_metadata_newlines(self):
        df = pl.DataFrame({'text': ['a\nb']})
        meta = PolarsTypeMapper.get_sas_transfer_metadata(df, embedded_newlines=True)
        # Default LF='\x01' -> '01'x
        self.assertIn("'text'n = translate('text'n, '0A'x, '01'x)", meta['xlate'])
        self.assertIn("'text'n = translate('text'n, '0D'x, '02'x)", meta['xlate'])

    def test_get_sas_transfer_metadata_lazy(self):
        df = pl.LazyFrame({'a': [1], 'b': ['x']})
        meta = PolarsTypeMapper.get_sas_transfer_metadata(df)
        # For LazyFrame, default string length should be 32767
        self.assertIn("'b'n $32767", meta['length'])
        self.assertIn("'a'n 8", meta['length'])

    def test_get_sas_transfer_metadata_labels_formats(self):
        df = pl.DataFrame({'a': [1]})
        meta = PolarsTypeMapper.get_sas_transfer_metadata(
            df, 
            labels={'a': "'My Label'"},
            outfmts={'a': 'DOLLAR10.2'}
        )
        self.assertIn("label 'a'n = 'My Label'", meta['label'])
        self.assertIn("'a'n DOLLAR10.2", meta['format'])

if __name__ == '__main__':
    unittest.main()
