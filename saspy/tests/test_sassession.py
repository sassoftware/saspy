import unittest
import saspy
import os
from IPython.utils.tempdir import TemporaryDirectory

class TestSASsessionObject(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession()
        cls.sas.set_batch(True)

    @classmethod
    def tearDownClass(cls):
        cls.sas._endsas()

    def test_sassession(self):
        self.assertIsInstance(self.sas, saspy.SASsession)

    def test_sassession_exist_true(self):
        """
        Test method exist returns True for a dataset that exists
        """
        exists = self.sas.exist('cars', libref='sashelp')
        self.assertTrue(exists)

    def test_sassession_exist_false(self):
        """
        Test method exist returns False for a dataset that does not exist
        """
        exists = self.sas.exist('notable', libref='sashelp')
        self.assertFalse(exists)

    def test_SASsession_csv_read(self):
        """
        Test method read_csv properly imports a csv file
        """
        EXPECTED = ['1', 'Acura', 'MDX', 'SUV', 'Asia', 'All', '$36,945', '$33,337', '3.5']

        with TemporaryDirectory() as temppath:
            fname = os.path.join(temppath, 'sas_csv_test.csv')
            self.sas.write_csv(fname, 'cars', libref='sashelp')

            csvdata = self.sas.read_csv(fname, 'csvcars', results='text')

        ll = csvdata.head()

        rows = ll['LST'].splitlines()
        retrieved = [x.split() for x in rows]

        self.assertIn(EXPECTED, retrieved, msg="csvcars.head() result didn't contain row 1")

    def test_sassession_csv_write(self):
        """
        Test method write_csv properly exports a csv file
        """
        with TemporaryDirectory() as temppath:
            fname = os.path.join(temppath, 'sas_csv_test.csv')
            log = self.sas.write_csv(fname, 'cars', libref='sashelp')

        self.assertNotIn("ERROR", log, msg="sas.write_csv() failed")

    def test_sassession_datasets_work(self):
        """
        Test method datasets can identify that the WORK library exists
        """
        EXPECTED = ['Libref', 'WORK']

        log = self.sas.datasets()
        rows = log.splitlines()
        retrieved = [x.split() for x in rows]

        self.assertIn(EXPECTED, retrieved)

    def test_sassession_datasets_sashelp(self):
        """
        Test method datasets can identify that the SASHELP library exists
        """
        EXPECTED = ['Libref', 'SASHELP']

        log = self.sas.datasets('sashelp')
        rows = log.splitlines()
        retrieved = [x.split() for x in rows]

        self.assertIn(EXPECTED, retrieved)

    def test_sassession_hasstat(self):
        """
        Test method sasstat() returns a SASstat object.
        """
        stat = self.sas.sasstat()

        self.assertIsInstance(stat, saspy.sasstat.SASstat, msg="stat = self.sas.sasstat() failed")

    def test_sassession_hasets(self):
        """
        Test method sasets() returns a SASets object.
        """
        ets = self.sas.sasets()

        self.assertIsInstance(ets, saspy.sasets.SASets, msg="ets = self.sas.sasets() failed")

    def test_sassession_hasqc(self):
        """
        Test method sasqc() returns a SASqc object.
        """
        qc = self.sas.sasqc()

        self.assertIsInstance(qc, saspy.sasqc.SASqc, msg="qc = self.sas.sasqc() failed")

    def test_sassession_hasml(self):
        """
        Test method sasml() returns a SASml object.
        """
        ml = self.sas.sasml()

        self.assertIsInstance(ml, saspy.sasml.SASml, msg="ml = self.sas.sasml() failed")

    def test_sassession_hasutil(self):
        """
        Test method sasutil() returns a SASutil object.
        """
        util = self.sas.sasutil()

        self.assertIsInstance(util, saspy.sasutil.SASutil, msg="util = self.sas.sasutil() failed")
