import unittest
import saspy
import datetime

try:
    import pyarrow.parquet as pq
except ImportError:
    pq = None

import os
#import debugpy
#debugpy.listen(5678)
#print("Waiting for debugger attach")
#debugpy.wait_for_client()
#debugpy.breakpoint()

class TestParquetIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession()
        cls.sas.set_batch(True)

    @classmethod
    def tearDownClass(cls):
        cls.sas._endsas()

    @unittest.skipIf(not pq, "pyarrow.parquet is not installed")
    def test_sas_dataset_with_no_rows(self):
        """Test sasdata2parquet with sas dataset containing no rows"""
        self.sas.submit("""proc sql; CREATE TABLE work.empty(c1 CHAR(10), n1 NUMERIC, d1 DATE, i1 INT, f1 FLOAT); quit;""")

        # this should create a parquet file with the correct schema but there are no rows in the dataset, so the parquet file should have no rows as well
        self.sas.sasdata2parquet('empty.parquet', table='empty', libref='work')

        # now use python to read the parquet file and check that it has the correct schema and no rows
        pq_empty = pq.ParquetFile('empty.parquet')

        #print("pq_empty = %s\n" % pq_empty)
        #print("pq_empty schema = %s \n" % pq_empty.schema)
        #print("pq_empty columns = %s \n" % pq_empty.schema.names)
        #print("pq_empty a_columns = %s \n" % pq_empty.schema_arrow.names)
        #print("pq_empty a_types = %s \n" % pq_empty.schema_arrow.types)
        #print("pq_empty column_c1_type= %s \n" % pq_empty.schema_arrow.field('c1').type)
        #print("pq_empty num_rows = %d\n" % pq_empty.metadata.num_rows)

        self.assertEqual(pq_empty.metadata.num_rows, 0, "The number of rows should have been 0 but was %d" % pq_empty.metadata.num_rows)
        self.assertEqual(pq_empty.metadata.num_columns, 5, "The number of columns should have been 5 but was %d" % pq_empty.metadata.num_columns)  # c1, n1, d1, i1, f1

        self.assertIn('c1', pq_empty.schema.names, "The column names should have included 'c1' but were %s" % pq_empty.schema.names)
        self.assertIn('n1', pq_empty.schema.names, "The column names should have included 'n1' but were %s" % pq_empty.schema.names)
        self.assertIn('d1', pq_empty.schema.names, "The column names should have included 'd1' but were %s" % pq_empty.schema.names)
        self.assertIn('i1', pq_empty.schema.names, "The column names should have included 'i1' but were %s" % pq_empty.schema.names)
        self.assertIn('f1', pq_empty.schema.names, "The column names should have included 'f1' but were %s" % pq_empty.schema.names)
        
        self.assertEqual(pq_empty.schema_arrow.field('c1').type, 'string', "The column type for 'c1' should have been string but was %s" % pq_empty.schema_arrow.field('c1').type)
        self.assertEqual(pq_empty.schema_arrow.field('n1').type, 'double', "The column type for 'n1' should have been double but was %s" % pq_empty.schema_arrow.field('n1').type)
        self.assertEqual(pq_empty.schema_arrow.field('d1').type, 'date32[day]', "The column type for 'd1' should have been date32[day] but was %s" % pq_empty.schema_arrow.field('d1').type)
        self.assertEqual(pq_empty.schema_arrow.field('i1').type, 'double', "The column type for 'i1' should have been double but was %s" % pq_empty.schema_arrow.field('i1').type)
        self.assertEqual(pq_empty.schema_arrow.field('f1').type, 'double', "The column type for 'f1' should have been double but was %s" % pq_empty.schema_arrow.field('f1').type)

        os.remove('empty.parquet')  # clean up the parquet file after the test

    @unittest.skipIf(not pq, "pyarrow.parquet is not installed")
    def test_sas_dataset_containing_date_types(self):
        """Test sasdata2parquet with sas dataset containing date types"""
        self.sas.submit("""\
proc sql; 
    CREATE TABLE work.date_types(d1 NUM format=date., t1 NUM format=time., ts1 NUM format=datetime.); 
    INSERT INTO work.date_types VALUES(1,2,3); 
quit;
""")

        # this should create a parquet file with the correct schema and one row
        self.sas.sasdata2parquet('date_types1.parquet', table='date_types', libref='work')
        self.sas.sasdata2parquet('date_types2.parquet', table='date_types', libref='work', include_attrs=True)  # include_attrs=True should be default now
        self.sas.sasdata2parquet('date_types3.parquet', table='date_types', libref='work', include_attrs=False)

        # now use python to read the parquet file and check that it has the correct schema and one row
        pq_dt1 = pq.ParquetFile('date_types1.parquet')
        pq_dt2 = pq.ParquetFile('date_types2.parquet')
        pq_dt3 = pq.ParquetFile('date_types3.parquet')

        #Check that the number of rows and columns are correct
        self.assertEqual(pq_dt1.metadata.num_rows, 1, "The number of rows in pq_dt1 should have been 1 but was %d" % pq_dt1.metadata.num_rows)
        self.assertEqual(pq_dt1.metadata.num_columns, 3, "The number of columns in pq_dt1 should have been 3 but was %d" % pq_dt1.metadata.num_columns)

        self.assertEqual(pq_dt2.metadata.num_rows, 1, "The number of rows in pq_dt2 should have been 1 but was %d" % pq_dt2.metadata.num_rows)
        self.assertEqual(pq_dt2.metadata.num_columns, 3, "The number of columns in pq_dt2 should have been 3 but was %d" % pq_dt2.metadata.num_columns)

        self.assertEqual(pq_dt3.metadata.num_rows, 1, "The number of rows in pq_dt3 should have been 1 but was %d" % pq_dt3.metadata.num_rows)
        self.assertEqual(pq_dt3.metadata.num_columns, 3, "The number of columns in pq_dt3 should have been 3 but was %d" % pq_dt3.metadata.num_columns)

        #Check that the column names are correct
        self.assertIn('d1', pq_dt1.schema.names, "The column names in pq_dt1 should have included 'd1' but were %s" % pq_dt1.schema.names)
        self.assertIn('t1', pq_dt1.schema.names, "The column names in pq_dt1 should have included 't1' but were %s" % pq_dt1.schema.names)
        self.assertIn('ts1', pq_dt1.schema.names, "The column names in pq_dt1 should have included 'ts1' but were %s" % pq_dt1.schema.names)

        self.assertIn('d1', pq_dt2.schema.names, "The column names in pq_dt2 should have included 'd1' but were %s" % pq_dt2.schema.names)
        self.assertIn('t1', pq_dt2.schema.names, "The column names in pq_dt2 should have included 't1' but were %s" % pq_dt2.schema.names)
        self.assertIn('ts1', pq_dt2.schema.names, "The column names in pq_dt2 should have included 'ts1' but were %s" % pq_dt2.schema.names)
        
        self.assertIn('d1', pq_dt3.schema.names, "The column names in pq_dt3 should have included 'd1' but were %s" % pq_dt3.schema.names)
        self.assertIn('t1', pq_dt3.schema.names, "The column names in pq_dt3 should have included 't1' but were %s" % pq_dt3.schema.names)
        self.assertIn('ts1', pq_dt3.schema.names, "The column names in pq_dt3 should have included 'ts1' but were %s" % pq_dt3.schema.names)

        #Check the datatypes are correct
        self.assertEqual(pq_dt1.schema_arrow.field('d1').type, 'date32[day]', "The column type for 'd1' in pq_dt1 should have been date32[day] but was %s" % pq_dt1.schema_arrow.field('d1').type)
        self.assertEqual(pq_dt1.schema_arrow.field('t1').type, 'time64[us]', "The column type for 't1' in pq_dt1 should have been time64[us] but was %s" % pq_dt1.schema_arrow.field('t1').type)
        self.assertEqual(pq_dt1.schema_arrow.field('ts1').type, 'timestamp[ns]', "The column type for 'ts1' in pq_dt1 should have been timestamp[ns] but was %s" % pq_dt1.schema_arrow.field('ts1').type)

        self.assertEqual(pq_dt2.schema_arrow.field('d1').type, 'date32[day]', "The column type for 'd1' in pq_dt2 should have been date32[day] but was %s" % pq_dt2.schema_arrow.field('d1').type)
        self.assertEqual(pq_dt2.schema_arrow.field('t1').type, 'time64[us]', "The column type for 't1' in pq_dt2 should have been time64[us] but was %s" % pq_dt2.schema_arrow.field('t1').type)
        self.assertEqual(pq_dt2.schema_arrow.field('ts1').type, 'timestamp[ns]', "The column type for 'ts1' in pq_dt2 should have been timestamp[ns] but was %s" % pq_dt2.schema_arrow.field('ts1').type)

        # dt3 will have different types because include_attrs=False means the date/time/datetime formats are not included in the parquet file
        self.assertEqual(pq_dt3.schema_arrow.field('d1').type, 'timestamp[ns]', "The column type for 'd1' in pq_dt3 should have been timestamp[ns] but was %s" % pq_dt3.schema_arrow.field('d1').type)
        self.assertEqual(pq_dt3.schema_arrow.field('t1').type, 'timestamp[ns]', "The column type for 't1' in pq_dt3 should have been timestamp[ns] but was %s" % pq_dt3.schema_arrow.field('t1').type)
        self.assertEqual(pq_dt3.schema_arrow.field('ts1').type, 'timestamp[ns]', "The column type for 'ts1' in pq_dt3 should have been timestamp[ns] but was %s" % pq_dt3.schema_arrow.field('ts1').type)

        #Check that the values are correct
        row_dt1 = pq_dt1.read_row_group(0)
        row_dt2 = pq_dt2.read_row_group(0)
        row_dt3 = pq_dt3.read_row_group(0)

        self.assertEqual(row_dt1.column('d1')[0].as_py(), datetime.date(1960,1,2), "The value for 'd1' in pq_dt1 should have been date(1960,1,2) but was %s" % row_dt1.column('d1')[0].as_py())
        self.assertEqual(row_dt1.column('t1')[0].as_py(), datetime.time(0,0,2), "The value for 'd1' in pq_dt1 should have been time(0,0,2) but was %s" % row_dt1.column('t1')[0].as_py())
        self.assertEqual(row_dt1.column('ts1')[0].as_py(), datetime.datetime(1960,1,1,0,0,3), "The value for 'd1' in pq_dt1 should have been datetime(1960,1,1,0,0,3) but was %s" % row_dt1.column('ts1')[0].as_py())

        self.assertEqual(row_dt2.column('d1')[0].as_py(), datetime.date(1960,1,2), "The value for 'd1' in pq_dt2 should have been date(1960,1,2) but was %s" % row_dt2.column('d1')[0].as_py())
        self.assertEqual(row_dt2.column('t1')[0].as_py(), datetime.time(0,0,2), "The value for 'd1' in pq_dt2 should have been time(0,0,2) but was %s" % row_dt2.column('t1')[0].as_py())
        self.assertEqual(row_dt2.column('ts1')[0].as_py(), datetime.datetime(1960,1,1,0,0,3), "The value for 'd1' in pq_dt2 should have been datetime(1960,1,1,0,0,3) but was %s" % row_dt2.column('ts1')[0].as_py())

        # dt3 will have different values because include_attrs=False means the date/time/datetime formats are not included in the parquet file, so the values will be interpreted as timestamps instead of dates/times/datetimes
        self.assertEqual(row_dt3.column('d1')[0].as_py(), datetime.datetime(1960,1,2,0,0,0), "The value for 'd1' in pq_dt3 should have been datetime(1960,1,2,0,0,0) but was %s" % row_dt3.column('d1')[0].as_py())
        self.assertEqual(row_dt3.column('t1')[0].as_py(), None, "The value for 'd1' in pq_dt3 should have been None but was %s" % row_dt3.column('t1')[0].as_py()) #empty date portion of timestamp is invalid, so it will be None
        self.assertEqual(row_dt3.column('ts1')[0].as_py(), datetime.datetime(1960,1,1,0,0,3), "The value for 'd1' in pq_dt3 should have been datetime(1960,1,1,0,0,3) but was %s" % row_dt3.column('ts1')[0].as_py())

        os.remove('date_types1.parquet')  # clean up the parquet file after the test
        os.remove('date_types2.parquet')  # clean up the parquet file after the test
        os.remove('date_types3.parquet')  # clean up the parquet file after the test