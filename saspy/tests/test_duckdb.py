"""
Test suite for DuckDB-to-SAS integration.

Tests the duckdb_to_sas() method which exports DuckDB query results
to SAS datasets via CSV, bypassing pandas serialization.

Requires: duckdb, saspy with an accessible SAS session.
"""

import unittest
import tempfile
import os

import saspy

try:
    import duckdb
    DUCKDB_AVAILABLE = True
except ImportError:
    DUCKDB_AVAILABLE = False


@unittest.skipIf(not DUCKDB_AVAILABLE, "duckdb is not installed")
class TestDuckDBToSAS(unittest.TestCase):
    """Test duckdb_to_sas method on SASsession."""

    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession()
        cls.sas.set_batch(True)
        cls.ddb = duckdb.connect()

        # Create test tables in DuckDB
        cls.ddb.execute("""
            create table test_mixed as select * from (values
                (1,  'Alice',   date '1990-01-15', 25.5,  true,  timestamp '2020-06-15 14:30:00'),
                (2,  'Bob',     date '1985-06-30', 30.0,  false, timestamp '2020-07-20 09:15:30'),
                (3,  'Carol',   null,              28.7,  true,  null)
            ) t(id, name, birth_dt, score, active, created_ts)
        """)

        cls.ddb.execute("""
            create table test_chars as select * from (values
                ('00069015001', 'NY', 'paid'),
                ('35356077330', 'CA', 'denied'),
                ('68382050010', 'TX', null)
            ) t(ndc, state_cd, status)
        """)

        cls.ddb.execute("""
            create table test_large as
            select
                i as id,
                'member_' || i::varchar as name,
                date '2020-01-01' + (i % 365)::int as svc_date,
                (i % 100)::double / 3.0 as amount
            from generate_series(1, 10000) t(i)
        """)

    @classmethod
    def tearDownClass(cls):
        cls.ddb.close()
        cls.sas._endsas()

    def test_duckdb_to_sas_instance(self):
        """duckdb_to_sas returns a SASdata object."""
        sd = self.sas.duckdb_to_sas(self.ddb, query='test_mixed', table='ddb_inst')
        self.assertIsInstance(sd, saspy.sasdata.SASdata)

    def test_duckdb_to_sas_row_count(self):
        """Correct number of rows transferred."""
        sd = self.sas.duckdb_to_sas(self.ddb, query='test_mixed', table='ddb_rows')
        ll = self.sas.submit("proc sql noprint; select count(*) into :n from work.ddb_rows; quit;", results='text')
        n = int(self.sas.symget('n'))
        self.assertEqual(n, 3)

    def test_duckdb_to_sas_types(self):
        """Char, date, numeric, and timestamp columns typed correctly in SAS."""
        sd = self.sas.duckdb_to_sas(self.ddb, query='test_mixed', table='ddb_types')
        # Read back via sd2df to check types survived the round trip
        df = self.sas.sd2df('ddb_types')
        df.columns = df.columns.str.lower()

        # name should be character (object dtype in pandas)
        self.assertEqual(df['name'].dtype.kind, 'O')
        # id should be numeric
        self.assertIn(df['id'].dtype.kind, ('i', 'f'))
        # birth_dt should be datetime-like
        self.assertEqual(df['birth_dt'].dtype.kind, 'M')

    def test_duckdb_to_sas_null_handling(self):
        """NULL values become SAS missing (NaN/NaT in round-trip)."""
        sd = self.sas.duckdb_to_sas(self.ddb, query='test_mixed', table='ddb_null')
        df = self.sas.sd2df('ddb_null')
        df.columns = df.columns.str.lower()

        # Carol (row 3) has null birth_dt and null created_ts
        import pandas as pd
        self.assertTrue(pd.isna(df.loc[2, 'birth_dt']))

    def test_duckdb_to_sas_labels(self):
        """Labels applied correctly to SAS dataset."""
        sd = self.sas.duckdb_to_sas(
            self.ddb, query='test_chars', table='ddb_labels',
            labels={'ndc': 'National Drug Code', 'state_cd': 'State'},
        )
        # Check via proc contents
        ll = self.sas.submit(
            "ods listing;\nproc contents data=work.ddb_labels; run;\nods listing close;\n",
            results='TEXT'
        )
        output = ll['LST']
        self.assertIn('National Drug Code', output)
        self.assertIn('State', output)

    def test_duckdb_to_sas_formats(self):
        """Formats applied correctly to SAS dataset."""
        sd = self.sas.duckdb_to_sas(
            self.ddb, query='test_chars', table='ddb_fmts',
            outfmts={'ndc': '$11.', 'state_cd': '$2.'},
        )
        ll = self.sas.submit(
            "ods listing;\nproc contents data=work.ddb_fmts; run;\nods listing close;\n",
            results='TEXT'
        )
        output = ll['LST']
        self.assertIn('$11', output)
        self.assertIn('$2', output)

    def test_duckdb_to_sas_char_lengths(self):
        """Explicit character lengths honoured."""
        sd = self.sas.duckdb_to_sas(
            self.ddb, query='test_chars', table='ddb_clen',
            char_lengths={'ndc': 11, 'state_cd': 2, 'status': 10},
        )
        df = self.sas.sd2df('ddb_clen')
        df.columns = df.columns.str.lower()
        # NDC with leading zeros should be preserved
        ndc_vals = df['ndc'].str.strip()
        self.assertTrue(ndc_vals.iloc[0].startswith('0'), "NDC leading zeros lost")

    def test_duckdb_to_sas_large_query(self):
        """Works with a subquery, not just a bare table name."""
        sd = self.sas.duckdb_to_sas(
            self.ddb,
            query="select * from test_large where id <= 500",
            table='ddb_sub',
        )
        self.assertIsInstance(sd, saspy.sasdata.SASdata)
        ll = self.sas.submit("proc sql noprint; select count(*) into :n from work.ddb_sub; quit;", results='text')
        n = int(self.sas.symget('n'))
        self.assertEqual(n, 500)

    def test_duckdb_to_sas_tempkeep(self):
        """CSV preserved when tempkeep=True, cleaned when False."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # tempkeep=True: CSV should remain
            sd = self.sas.duckdb_to_sas(
                self.ddb, query='test_chars', table='ddb_tk',
                tempdir=tmpdir, tempkeep=True,
            )
            csv_path = os.path.join(tmpdir, 'ddb_tk.csv')
            self.assertTrue(os.path.exists(csv_path), "CSV should be kept")

        with tempfile.TemporaryDirectory() as tmpdir:
            # tempkeep=False (default): CSV should be deleted
            sd = self.sas.duckdb_to_sas(
                self.ddb, query='test_chars', table='ddb_rm',
                tempdir=tmpdir, tempkeep=False,
            )
            csv_path = os.path.join(tmpdir, 'ddb_rm.csv')
            self.assertFalse(os.path.exists(csv_path), "CSV should be removed")

    def test_duckdb_to_sas_empty_query(self):
        """Empty query returns None with error."""
        sd = self.sas.duckdb_to_sas(self.ddb, query='', table='ddb_empty')
        self.assertIsNone(sd)

    def test_duckdb_to_sas_computed_char_lengths(self):
        """VARCHAR columns without explicit lengths get computed lengths."""
        sd = self.sas.duckdb_to_sas(
            self.ddb, query='test_chars', table='ddb_auto',
        )
        self.assertIsInstance(sd, saspy.sasdata.SASdata)
        df = self.sas.sd2df('ddb_auto')
        df.columns = df.columns.str.lower()
        # NDC values should be intact (11 chars)
        ndc_vals = df['ndc'].str.strip()
        self.assertTrue(all(len(v) == 11 for v in ndc_vals.dropna()))


if __name__ == '__main__':
    unittest.main()
