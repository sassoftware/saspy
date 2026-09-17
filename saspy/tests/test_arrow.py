"""
Test suite for Arrow-related features in saspy.

Tests the following functionality:
1. Metadata enhancement: list_tables with labels, sasdata.schema
2. Arrow support: arrow_char_lengths, sasdata2arrow, arrow2sasdata,  importing sas datasets with no rows
"""

import saspy
import unittest
from decimal import Decimal

try:
    import pyarrow as pa
    import pyarrow.parquet as pq
    PYARROW_AVAILABLE = True
except ImportError:
    PYARROW_AVAILABLE = False


@unittest.skipIf(not PYARROW_AVAILABLE, "pyarrow is not installed")
class TestMetadataEnhancement(unittest.TestCase):
    """Test metadata enhancement features"""

    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession()
        cls.sas.set_batch(True)
        
        # Create test dataset with label and extended attributes
        cls.sas.submit("""
            data work.test_label(label="Test Dataset Label");
                input id name $ age;
                label id = "ID Number" name = "Name" age = "Age";
                datalines;
            1 Alice 25
            2 Bob 30
            3 Carol 28
            ;
            run;
            proc datasets lib=work nolist;
                modify test_label;
                xattr add ds attr="ds attribute" ;
                 xattr add var id (attr="var attribute") ;
            quit;
        """)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'sas'):
            cls.sas._endsas()

    def test_list_tables_with_label(self):
        """Test list_tables with label=True"""
        # Get tables with labels
        tables = self.sas.list_tables(libref='work', label=True)
        
        self.assertIsInstance(tables, list)
        self.assertGreater(len(tables), 0)
        
        # Find our test dataset
        test_label_found = False
        for memname, info in tables:
            if memname.upper() == 'TEST_LABEL':
                test_label_found = True
                self.assertIsInstance(info, dict)
                self.assertIn('memtype', info)
                # Label may or may not be present depending on implementation
                break
        
        self.assertTrue(test_label_found, "test_label dataset not found")

    def test_schema_as_arrow(self):
        """Test sasdata.schema returns pyarrow.Schema"""
        sd = self.sas.sasdata('test_label', 'work')
        schema = sd.schema(sasattrs=True, xattrs=True)
        
        self.assertIsInstance(schema, pa.Schema)
        
        # Check fields
        field_names = [field.name for field in schema]
        self.assertIn('id', field_names)
        self.assertIn('name', field_names)
        self.assertIn('age', field_names)
        self.assertEqual(schema.metadata.get(b'extended_attributes'), b'{"attr": "ds attribute"}')
        self.assertEqual(schema.field(b'id').metadata.get(b'extended_attributes'), b'{"attr": "var attribute"}')

    def test_schema_as_dict(self):
        """Test sasdata.schema can return dict when pyarrow not available"""
        sd = self.sas.sasdata('test_label', 'work')
        
        # Even with pyarrow available, schema should work
        schema = sd.schema(sasattrs=True, xattrs=True, results='dict')
        # Should be Schema or dict
        self.assertIsInstance(schema, dict)


@unittest.skipIf(not PYARROW_AVAILABLE, "pyarrow is not installed")
class TestArrowSupport(unittest.TestCase):
    """Test Arrow-related features"""

    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession()
        cls.sas.set_batch(True)
        
        # Create test dataset
        cls.sas.submit("""
            data work.test_data;
                input id name $ age height;
                datalines;
            1 Alice 25 165.5
            2 Bob 30 175.2
            3 Carol 28 168.0
            ;
            run;
        """)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'sas'):
            cls.sas._endsas()

    def test_arrow_basic_features(self):
        """Test arrow_char_lengths, sasdata2arrow, and arrow2sasdata with basic and timestamp types"""
        import datetime
        
        # 1. Test arrow_char_lengths
        data_lengths = {
            'short_str': ['a', 'bb', 'ccc'],
            'long_str': ['x' * 100, 'y' * 200, 'z' * 150]
        }
        arrow_table_lengths = pa.Table.from_pydict(data_lengths)
        char_lengths = self.sas.arrow_char_lengths(arrow_table_lengths)
        
        self.assertIsInstance(char_lengths, dict)
        self.assertEqual(char_lengths['short_str'], 3)
        self.assertEqual(char_lengths['long_str'], 200)
        
        # 2. Test sasdata2arrow
        arrow_table = self.sas.sasdata2arrow(table='test_data', libref='work')
        
        self.assertIsInstance(arrow_table, pa.Table)
        self.assertEqual(arrow_table.num_rows, 3)
        column_names = arrow_table.column_names
        self.assertIn('id', column_names)
        self.assertIn('name', column_names)
        self.assertEqual('work', arrow_table.schema.metadata.get(b'libref').decode('utf-8'))
        
        # 3. Test arrow2sasdata with basic types and timestamps
        data = {
            'int_col': [1, 2, 3],
            'float_col': [1.1, 2.2, 3.3],
            'str_col': ['a', 'b', 'c'],
            'bool_col': [True, False, True],
            'timestamp_col': [
                datetime.datetime(2020, 1, 1, 9, 0, 0),
                datetime.datetime(2021, 6, 15, 14, 30, 0),
                datetime.datetime(2022, 12, 31, 23, 59, 59)
            ]
        }
        arrow_table_basic = pa.Table.from_pydict(data)
        result = self.sas.arrow2sasdata(arrow_table_basic, table='test_arrow2sd', libref='work')
        
        self.assertIsInstance(result, saspy.SASdata)
        df = result.to_df()
        self.assertEqual(len(df), 3)

    def test_sd2arrow_format_inference(self):
        """Test sd2arrow(include_attrs=True) resolves SAS date/time/datetime formats correctly.

        Covers: a format missing an explicit width (date9), formats that were previously missing
        from the canonical format lists and crashed with ArrowNotImplementedError (e8601da,
        mdyampm, pdjulg, b8601tx), the NLSTRQTR collision (a numeric format whose name contains
        'QTR' as a substring, which must stay numeric), and a character column with date-like
        content (which must stay string rather than being swept into date detection).
        """
        import datetime

        self.sas.submit("""
            data work.test_fmt_inference;
                _d   = '15SEP2026'd;
                _dt  = dhms(_d, 13, 4, 22.5);
                _tod = hms(13, 4, 22.5);

                date_date9   = _d;   format date_date9   date9.;
                date_iso     = _d;   format date_iso     e8601da.;
                date_pdjulg  = _d;   format date_pdjulg  pdjulg.;
                dt_datetime  = _dt;  format dt_datetime  datetime.;
                dt_mdyampm   = _dt;  format dt_mdyampm   mdyampm.;
                time_b8601tx = _tod; format time_b8601tx b8601tx.;
                num_nlstrqtr = 2;    format num_nlstrqtr nlstrqtr5.;
                char_date9   = put(_d, date9.);

                drop _d _dt _tod;
            run;
        """)

        arrow_table = self.sas.sd2arrow(table='test_fmt_inference', libref='work', include_attrs=True)
        self.assertIsInstance(arrow_table, pa.Table)
        s = arrow_table.schema

        self.assertEqual(s.field('date_date9').type, pa.date32())
        self.assertEqual(s.field('date_iso').type, pa.date32())
        self.assertEqual(s.field('date_pdjulg').type, pa.date32())
        self.assertEqual(s.field('dt_datetime').type, pa.timestamp('us'))
        self.assertEqual(s.field('dt_mdyampm').type, pa.timestamp('us'))
        self.assertEqual(s.field('time_b8601tx').type, pa.time64('us'))
        self.assertEqual(s.field('num_nlstrqtr').type, pa.float64())
        self.assertEqual(s.field('char_date9').type, pa.string())

        # Type alone isn't enough: pc.strptime doesn't support the %f directive, which
        # previously made every datetime/time value (they always carry fractional seconds
        # on the wire) come back as a silent null despite the column reporting the correct
        # type. Check the actual values, including the fractional-second component.
        for col in ('dt_datetime', 'dt_mdyampm', 'time_b8601tx'):
            self.assertEqual(arrow_table.column(col).null_count, 0, "%s came back null" % col)
        df = arrow_table.to_pandas()
        self.assertEqual(df['dt_datetime'][0], datetime.datetime(2026, 9, 15, 13, 4, 22, 500000))
        self.assertEqual(df['time_b8601tx'][0], datetime.time(13, 4, 22, 500000))

    def test_sas_dataset_with_no_rows(self):
        """Test sasdata2arrow with sas dataset containing no rows"""
        self.sas.submit("""proc sql; create table work.empty as select * from work.test_data where 1=0; quit;""")
        arrow_table_empty = self.sas.sasdata2arrow(table='empty', libref='work')
        #print("Arrow_table_empty = %s\n" % arrow_table_empty)
        #print("Arrow_table_empty schema = %s \n" % arrow_table_empty.schema)
        #print("Arrow_table_empty num_rows = %d\n" % arrow_table_empty.num_rows)
        self.assertIsInstance(arrow_table_empty, pa.Table, "arrow_table_empty should be a pyarrow.Table but was %s" % type(arrow_table_empty))
        self.assertEqual(arrow_table_empty.num_rows, 0, "The number of rows should have been 0 but was %d" % arrow_table_empty.num_rows)
        self.assertEqual(arrow_table_empty.num_columns, 4, "The number of columns should have been 4 but was %d" % arrow_table_empty.num_columns)  # id, name, age, height

        s1 = arrow_table_empty.schema

        self.assertIn('id', s1.names, "The column names should have included 'id' but were %s" % arrow_table_empty.schema.names)
        self.assertIn('name', s1.names, "The column names should have included 'id' but were %s" % arrow_table_empty.schema.names)
        self.assertIn('age', s1.names, "The column names should have included 'id' but were %s" % arrow_table_empty.schema.names)
        self.assertIn('height', s1.names, "The column names should have included 'id' but were %s" % arrow_table_empty.schema.names)

        f1 = s1.field("id")
        f2 = s1.field("name")
        f3 = s1.field("age")
        f4 = s1.field("height")

        self.assertEqual(f1.type, pa.float64(), "The column type for 'id' should have been double but was %s" % f1.type)
        self.assertEqual(f2.type, pa.string(), "The column type for 'name' should have been string but was %s" % f2.type)
        self.assertEqual(f3.type, pa.float64(), "The column type for 'age' should have been double but was %s" % f3.type)
        self.assertEqual(f4.type, pa.float64(), "The column type for 'height' should have been double but was %s" % f4.type)

@unittest.skipIf(not PYARROW_AVAILABLE, "pyarrow is not installed")
class TestArrowSpecialTypes(unittest.TestCase):
    """Test Arrow special data types support"""

    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession()
        cls.sas.set_batch(True)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'sas'):
            cls.sas._endsas()

    def test_all_special_types(self):
        """Test arrow2sasdata with comprehensive set of special Arrow types in a single dataset"""
        
        # Dictionary type (categorical)
        indices = pa.array([0, 1, 0, 2])
        dictionary = pa.array(['A', 'B', 'C'])
        dict_array = pa.DictionaryArray.from_arrays(indices, dictionary)
        
        # Struct type (nested)
        struct_array = pa.StructArray.from_arrays(
            [pa.array([1, 2, 3, 4]), pa.array(['a', 'b', 'c', 'd'])],
            names=['field1', 'field2']
        )
        
        # Decimal type
        decimal_array = pa.array([Decimal('1.1'), Decimal('2.2'), Decimal('3.3'), Decimal('4.4')],
                                type=pa.decimal128(10, 2))
        
        # List type
        list_data = [[1, 2], [3], [4, 5], [6, 7, 8]]
        
        # Large string type
        large_str = pa.array(['text1', 'text2', 'text3', 'text4'], type=pa.large_string())
        
        # Map type
        map_data = pa.array(
            [[{'key': 'a', 'value': 1}], [{'key': 'b', 'value': 2}], 
             [{'key': 'c', 'value': 3}], [{'key': 'd', 'value': 4}]], 
            type=pa.map_(pa.string(), pa.int32())
        )
        
        # Binary type - should be converted to base64 string
        binary_array = pa.array([b'bin1', b'bin2', b'bin3', b'bin4'], type=pa.binary())
        
        # Null type - column with all nulls
        null_array = pa.array([None, None, None, None], type=pa.null())
        
        # Date64 type (milliseconds since epoch)
        date64_array = pa.array([0, 86400000, 172800000, 259200000], type=pa.date64())
        
        # Time32 type (seconds since midnight)
        time32_array = pa.array([0, 3600, 7200, 10800], type=pa.time32('s'))
        
        # Time64 type (microseconds since midnight)
        time64_array = pa.array([0, 3600000000, 7200000000, 10800000000], type=pa.time64('us'))
        
        # Duration type
        duration_array = pa.array([1000000, 2000000, 3000000, 4000000], type=pa.duration('us'))
        
        # Interval type (month_day_nano)
        interval_array = pa.array([
            pa.scalar((1, 0, 0), type=pa.month_day_nano_interval()),
            pa.scalar((2, 0, 0), type=pa.month_day_nano_interval()),
            pa.scalar((3, 0, 0), type=pa.month_day_nano_interval()),
            pa.scalar((4, 0, 0), type=pa.month_day_nano_interval())
        ])
        
        # Union types
        dense_union = pa.UnionArray.from_dense(
            pa.array([0, 1, 0, 1], type=pa.int8()),
            pa.array([0, 0, 1, 1], type=pa.int32()),
            [pa.array([100, 200]), pa.array(['a', 'b'])]
        )
        
        sparse_union = pa.UnionArray.from_sparse(
            pa.array([0, 1, 0, 1], type=pa.int8()),
            [pa.array([100, None, 200, None]), pa.array([None, 'a', None, 'b'])]
        )
        
        # Build table with all types
        table_dict = {
            'id': [1, 2, 3, 4],
            'dict_col': dict_array,
            'struct_col': struct_array,
            'decimal_col': decimal_array,
            'list_col': list_data,
            'large_str': large_str,
            'map_col': map_data,
            'binary_col': binary_array,
            'null_col': null_array,
            'date64_col': date64_array,
            'time32_col': time32_array,
            'time64_col': time64_array,
            'duration_col': duration_array,
            'interval_col': interval_array,
            'dense_union_col': dense_union,
            'sparse_union_col': sparse_union
        }
        
        arrow_table = pa.table(table_dict)
        
        result = self.sas.arrow2sasdata(arrow_table, table='test_all_special', libref='work')
        
        self.assertIsInstance(result, saspy.SASdata)        
        df = result.to_df()        
        # print(arrow_table)
        # print(df)
        self.assertEqual(len(df), 4)

if __name__ == '__main__':
    unittest.main()
