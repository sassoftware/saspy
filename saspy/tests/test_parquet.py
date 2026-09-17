import unittest
import saspy
import pyarrow.parquet as pq
import os
#import debugpy
#debugpy.listen(5678)
#print("Waiting for debugger attach")
#debugpy.wait_for_client()
#debugpy.breakpoint()

class TestPandasDataFrameIntegration(unittest.TestCase):
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